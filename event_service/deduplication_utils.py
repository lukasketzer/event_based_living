
import uuid
import logging
from typing import List, Set
from .models import EventOptional
from .db_utils import save_to_db
from .embedding_utils import create_documents, cosine_similarity

def inter_batch_deduplication(embeddings: List[List[float]], threshold: float) -> List[int]:
    """
    Identifies unique embeddings within a batch by removing near-duplicates based on cosine similarity.

    Args:
        embeddings (List[List[float]]): List of embedding vectors.
        threshold (float): Similarity threshold for considering embeddings as duplicates.

    Returns:
        List[int]: Indices of unique embeddings in the batch.
    """
    unique_indices = set()
    for idx, emb in enumerate(embeddings):
        is_duplicate = False
        for uidx in unique_indices:
            sim = cosine_similarity(emb, embeddings[uidx])
            if sim < threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_indices.add(idx)
    return unique_indices



# TODO: split up saving and deduplication logic into separate function
def deduplicate_events(events: List[EventOptional], embedding_model, vectorstore, threshold_db: float = 0.05, threshold_inter: float = 0.05) -> List[EventOptional]:

    # TODO: maybe imporve this part, i dont need documentes every time
    events_documents = create_documents(events)
    embeddings = embedding_model.embed_documents(
        [doc.page_content for doc in events_documents]
    )

    unique_embedding_indices = inter_batch_deduplication(embeddings, threshold_inter)
    logging.info(f"Found {len(events) - len(unique_embedding_indices)} duplicate events in the current batch.")

    embeddings = [embeddings[i] for i in unique_embedding_indices]
    events = [events[i] for i in unique_embedding_indices]

    unique_indices = []
    for idx in range(len(events)):
        emb = embeddings[idx]
        results = vectorstore.similarity_search_with_score_by_vector(emb, k=1)
        if results:
            _, score = results[0]
        else:
            score = 1.0
        if score < threshold_db:
            logging.info(
                f"Event at index {idx} identified as duplicate in database. Skipping entry."
            )
        else:
            logging.info(f"Event at index {idx} is unique. Adding to batch for saving.")
            unique_indices.append(idx)

    if unique_indices:
        unique_events = [events[i] for i in unique_indices]
        
        return unique_events
    else:
        return []
