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
from event_service.main import main 


if __name__ == "__main__":
    main()
