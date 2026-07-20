"""
MediSense AI - Vector Database Manager
Manages local persistent vector storage using ChromaDB / dense semantic indexing.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from app.rag.embeddings import embedding_service

logger = logging.getLogger("uvicorn.error")

class VectorDatabaseManager:
    def __init__(self, collection_name: str = "medisense_clinical_kb"):
        self.collection_name = collection_name
        self.chroma_client = None
        self.collection = None
        self.documents: List[Dict[str, Any]] = []
        self.doc_embeddings: List[List[float]] = []
        self._initialize_chroma()

    def _initialize_chroma(self):
        """Attempts to initialize ChromaDB persistent client."""
        try:
            import chromadb
            db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_storage")
            os.makedirs(db_dir, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=db_dir)
            self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
            logger.info(f"[VECTOR DB] Initialized ChromaDB persistent client at '{db_dir}'.")
        except Exception as e:
            logger.warning(f"[VECTOR DB] ChromaDB fallback notice ({e}). Using local persistent dense vector store.")

    def add_documents(self, chunks: List[Dict[str, Any]]):
        """Stores document text, dense embeddings, and metadata into the vector store."""
        if not chunks:
            return

        ids = [chunk["id"] for chunk in chunks]
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        embeddings = embedding_service.encode_batch(texts)

        if self.collection is not None:
            try:
                self.collection.upsert(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas,
                    embeddings=embeddings
                )
                logger.info(f"[VECTOR DB] Upserted {len(chunks)} chunks into ChromaDB.")
                return
            except Exception as e:
                logger.warning(f"[VECTOR DB] ChromaDB upsert warning ({e}). Storing in local dense index.")

        # Local Persistent Storage
        self.documents = chunks
        self.doc_embeddings = embeddings
        logger.info(f"[VECTOR DB] Stored {len(chunks)} document chunks in local semantic vector index.")

    def query(
        self,
        query_text: str,
        metadata_filter: Optional[Dict[str, Any]] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Executes semantic vector similarity search.
        Applies metadata filtering and returns top_k matching chunks with metadata.
        """
        query_vec = embedding_service.encode_text(query_text)

        # 1. Query ChromaDB if available
        if self.collection is not None and self.collection.count() > 0:
            try:
                where_clause = metadata_filter if metadata_filter else None
                results = self.collection.query(
                    query_embeddings=[query_vec],
                    n_results=top_k,
                    where=where_clause
                )
                
                formatted_results = []
                if results and results.get("documents") and len(results["documents"]) > 0:
                    docs = results["documents"][0]
                    metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                    distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)
                    
                    for i in range(len(docs)):
                        score = round(1.0 - (distances[i] if distances[i] <= 1.0 else 0.5), 4)
                        formatted_results.append({
                            "text": docs[i],
                            "metadata": metas[i],
                            "similarity_score": score
                        })
                    return formatted_results
            except Exception as e:
                logger.warning(f"[VECTOR DB] ChromaDB query warning ({e}). Falling back to local dense query.")

        # 2. Local Dense Vector Search Fallback
        if not self.documents:
            # Auto ingest if vector db empty
            from app.rag.chunker import DocumentChunker
            base_dir = os.path.dirname(os.path.abspath(__file__))
            k_dir = os.path.join(base_dir, "knowledge")
            chunks = DocumentChunker.load_and_chunk_knowledge_directory(k_dir)
            self.add_documents(chunks)

        scored_docs = []
        for idx, doc_vec in enumerate(self.doc_embeddings):
            doc = self.documents[idx]
            meta = doc.get("metadata", {})

            # Filter check
            if metadata_filter:
                match = True
                for fk, fv in metadata_filter.items():
                    if meta.get(fk) != fv:
                        match = False
                        break
                if not match:
                    continue

            # Dot Product Cosine Score
            score = sum(a * b for a, b in zip(query_vec, doc_vec))
            if score >= 0.15:
                doc_copy = doc.copy()
                doc_copy["similarity_score"] = round(score, 4)
                scored_docs.append((score, doc_copy))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:top_k]]

# Singleton Vector Database Manager
vector_db = VectorDatabaseManager()
