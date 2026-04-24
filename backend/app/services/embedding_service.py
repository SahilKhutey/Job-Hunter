import numpy as np
from typing import List

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.use_mock = False
        except ImportError:
            print("SentenceTransformers not found. Using mock embeddings.")
            self.use_mock = True

    def get_embedding(self, text: str) -> np.ndarray:
        if self.use_mock or not text:
            return np.random.rand(384)
        return self.model.encode(text)

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        if self.use_mock:
            return np.random.rand(len(texts), 384)
        return self.model.encode(texts)

embedding_service = EmbeddingService()
