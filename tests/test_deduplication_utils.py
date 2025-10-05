
import os
import sys
import pytest
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from event_service.deduplication_utils import inter_batch_deduplication

def test_inter_batch_deduplication_all_unique():
    # Each embedding is orthogonal (cosine similarity = 0)
    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    threshold = 0.1
    result = inter_batch_deduplication(embeddings, threshold)
    assert result == {0, 1, 2}

def test_inter_batch_deduplication_all_duplicates():
    # All embeddings are the same (cosine similarity = 1)
    embeddings = [
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ]
    threshold = 0.1
    result = inter_batch_deduplication(embeddings, threshold)
    assert result == {0}

def test_inter_batch_deduplication_some_duplicates():
    # First and second are the same, third is unique
    embeddings = [
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
    threshold = 0.1
    result = inter_batch_deduplication(embeddings, threshold)
    # Only the first and third should be unique
    assert result == {0, 2}
    def test_inter_batch_deduplication_threshold():
        # Two vectors with cosine similarity just below threshold
        embeddings = [
            [1.0, 0.0],
            [math.cos(math.radians(5)), math.sin(math.radians(5))],
        ]
        threshold = 0.1  # 1 - threshold = 0.9
        result = inter_batch_deduplication(embeddings, threshold)
        # The cosine similarity between the two vectors is ~0.996, which is greater than 1 - threshold (0.9).
        # So, the second vector should be considered a duplicate.
        assert result == {0}

def test_inter_batch_deduplication_multiple_duplicates():
    # First and second are the same, third and fourth are the same as each other but different from the first
    embeddings = [
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
    threshold = 0.1
    result = inter_batch_deduplication(embeddings, threshold)
    # Only the first and third should be unique
    assert result == {0, 2}
