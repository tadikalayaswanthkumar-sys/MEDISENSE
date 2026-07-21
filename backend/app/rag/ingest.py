"""
MediSense AI - Ingestion Pipeline
Reads all clinical markdown documents under backend/app/rag/knowledge/,
chunks them, generates embeddings, and populates the vector database.
"""

import os
import logging
from app.rag.chunker import DocumentChunker
from app.rag.vector_db import vector_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest")

def run_ingestion():
    """Builds and populates the vector database from the knowledge repository."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_dir = os.path.join(base_dir, "knowledge")

    logger.info(f"[INGEST] Starting clinical document ingestion from '{knowledge_dir}'...")

    if not os.path.exists(knowledge_dir):
        logger.error(f"[INGEST ERROR] Knowledge directory '{knowledge_dir}' does not exist.")
        return

    # 1. Chunk all markdown documents
    chunks = DocumentChunker.load_and_chunk_knowledge_directory(knowledge_dir)
    logger.info(f"[INGEST] Processed {len(chunks)} document chunks across knowledge categories.")

    # 2. Add chunks and embeddings to Vector DB
    vector_db.add_documents(chunks)
    logger.info("[INGEST SUCCESS] Successfully built and indexed the clinical vector database.")

if __name__ == "__main__":
    run_ingestion()
