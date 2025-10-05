import numpy as np
from typing import List
from langchain.schema import Document
from .models import EventOptional

def create_documents(events: List[EventOptional]) -> List[Document]:
    event_documents = [
        Document(
            page_content="\n".join(f"{key}: {value}" for key, value in event.model_dump().items()),
            metadata=event.model_dump(mode="json")
        )
        for event in events
    ]
    return event_documents

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return np.dot(vec1, vec2) / (norm1 * norm2)
