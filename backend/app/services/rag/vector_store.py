"""
MediSense AI - Production Vector Store & Semantic Index
Implements semantic vector embeddings, metadata filtering, similarity thresholding,
and document-based vector retrieval.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from app.services.rag.chunker import DocumentChunker
from app.services.rag.embeddings import embedding_service_instance

logger = logging.getLogger("uvicorn.error")

class ProductionVectorStore:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.doc_embeddings: List[List[float]] = []
        self._is_indexed = False

    def initialize_and_index(self):
        """Indexes all clinical markdown documents from the documents directory."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        docs_dir = os.path.join(base_dir, "documents")

        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir, exist_ok=True)

        chunks = DocumentChunker.load_all_document_chunks(docs_dir)
        self.documents = chunks
        
        # Build dense embeddings for all chunks
        self.doc_embeddings = [
            embedding_service_instance.generate_embedding(chunk["text"])
            for chunk in chunks
        ]
        self._is_indexed = True
        logger.info(f"[VECTOR STORE] Successfully indexed {len(chunks)} document chunks from '{docs_dir}'.")

    def similarity_search(
        self,
        query: str,
        metadata_filter: Optional[Dict[str, Any]] = None,
        top_k: int = 3,
        min_score: float = 0.50
    ) -> List[Dict[str, Any]]:
        """
        Executes semantic vector similarity search.
        Applies metadata filtering (e.g. biomarker=='hemoglobin') and min_score thresholding.
        """
        if not self._is_indexed:
            self.initialize_and_index()

        query_vec = embedding_service_instance.generate_embedding(query)
        results = []

        for idx, doc_vec in enumerate(self.doc_embeddings):
            doc = self.documents[idx]
            meta = doc.get("metadata", {})

            # 1. Metadata Filter Check
            if metadata_filter:
                match_filter = True
                for f_key, f_val in metadata_filter.items():
                    if meta.get(f_key) != f_val:
                        match_filter = False
                        break
                if not match_filter:
                    continue

            # 2. Cosine Similarity Calculation
            score = embedding_service_instance.cosine_similarity(query_vec, doc_vec)
            if score >= min_score:
                doc_copy = doc.copy()
                doc_copy["similarity_score"] = round(score, 4)
                results.append((score, doc_copy))

        # Sort descending by score
        results.sort(key=lambda x: x[0], reverse=True)

        return [doc for _, doc in results[:top_k]]

# Global Singleton Instance
vector_store_instance = ProductionVectorStore()

# Backward Compatibility Alias
VectorStore = ProductionVectorStore
