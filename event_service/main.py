import os
import glob
import logging
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from event_service.enums import models
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from tavily import TavilyClient
from event_service.models import ListEventOptional
from event_service.classification_utils import classify_llm
from event_service.db_utils import check_db_consistency, save_to_vector_and_relational
from event_service.repository import CONNECTION_STRING, init_db
from event_service.deduplication_utils import deduplicate_events
from event_service.enrichment_utils import enrich_events
from pathlib import Path
from event_service.crawler import crawl

load_dotenv()

tavily_api_key = os.environ.get("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def main():
    init_db()
    
    current_file_parent = Path(__file__).resolve().parent

    (current_file_parent / "results").mkdir(parents=True, exist_ok=True)

    # Read the sites from the file
    with open(current_file_parent / "sites.txt", "r") as file:
        initial_urls = file.readlines()

    initial_urls = set([site.strip() for site in initial_urls if site.strip()])
    initial_urls = set([site for site in initial_urls if not site.startswith("#")])

    skip = {"youtube.com", "youtu.be", "facebook.com", "instagram.com", "x.com"}

    rpm = 15
    rps = rpm / 60
    rate_limiter = InMemoryRateLimiter(
        requests_per_second=rps, check_every_n_seconds=0.5, max_bucket_size=1
    )

    model_classification = ChatGoogleGenerativeAI(
        model=models.GeminiModels.GEMINI_2_5_FLASH_LITE_PREVIEW_06_17.value,
        rate_limiter=rate_limiter,
    ).with_structured_output(ListEventOptional)



    embedding_model = HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        model_kwargs={"trust_remote_code": True}
    )

    # Connect to pgVector (adjust connection string as needed)
    vectorstore = PGVector(
        embeddings=embedding_model,
        collection_name="events",
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )



    logging.info("Starting database consistency check...")
    consistency = check_db_consistency()
    logging.info(
        f"Database consistency check result: {'PASSED' if consistency else 'FAILED'}."
    )

    for url, text in crawl(initial_urls, skip=skip, max_depth=5, num_results=10):
        logging.info(f"================================= Processing URL: {url} =================================")

        # with open(file, "r") as f:
        #     text = f.read().strip()

        events = classify_llm(model_classification, text)
        logging.info(f"Extracted {len(events)} events from the text.")
        events = deduplicate_events(
            events, embedding_model, vectorstore
        )
        logging.info(f"Deduplicated to {len(events)} unique events.")
        events = enrich_events(events, tavily_client)
        logging.info(f"Enriched events. Final count: {len(events)}.")
        save_to_vector_and_relational(events, vectorstore=vectorstore)
        logging.info(f"Saved {len(events)} events to vector and relational databases.")

