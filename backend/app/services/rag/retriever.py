"""
MediSense AI - Targeted Per-Biomarker Retriever with Metadata Filtering & Audit Logging
Retrieves clinical knowledge chunks separately for EVERY abnormal biomarker,
filters by metadata, applies similarity thresholds, and logs full audit traces.
"""

import logging
from typing import List, Dict, Any
from app.services.rag.vector_store import vector_store_instance

logger = logging.getLogger("uvicorn.error")

class TargetedBiomarkerRetriever:
    @staticmethod
    def retrieve_per_abnormal_biomarker(
        abnormal_findings: List[Dict[str, Any]],
        top_k_per_biomarker: int = 2,
        min_score: float = 0.20
    ) -> List[Dict[str, Any]]:
        """
        Executes targeted vector search separately for EACH abnormal biomarker.
        Applies metadata filters (biomarker key), deduplicates chunks, and ranks by similarity score.
        """
        if not abnormal_findings:
            logger.info("[VECTOR RAG] No abnormal biomarkers detected. Executing fallback general health search.")
            return vector_store_instance.similarity_search("optimal health biomarkers", top_k=2, min_score=0.15)

        merged_evidence: List[Dict[str, Any]] = []
        seen_chunk_ids = set()

        for finding in abnormal_findings:
            biomarker_key = finding.get("biomarker") or finding.get("key")
            status = finding.get("status", "")
            val = finding.get("value", "")
            unit = finding.get("unit", "")
            name = finding.get("name", "")

            # 1. Construct Biomarker Specific Query
            query = f"{name} {val} {unit} {status} clinical interpretation lifestyle guidance"
            logger.info(f"[VECTOR RAG SEARCH] Biomarker: '{biomarker_key}' | Query: '{query}'")

            # 2. Metadata Filtered Vector Search
            chunks = vector_store_instance.similarity_search(
                query=query,
                metadata_filter={"biomarker": biomarker_key} if biomarker_key else None,
                top_k=top_k_per_biomarker,
                min_score=min_score
            )

            # Fallback search without strict biomarker filter if specific chunk not found
            if not chunks:
                chunks = vector_store_instance.similarity_search(
                    query=query,
                    top_k=top_k_per_biomarker,
                    min_score=0.15
                )

            # 3. Merge & Deduplicate
            for chunk in chunks:
                chunk_id = chunk.get("id")
                if chunk_id not in seen_chunk_ids:
                    seen_chunk_ids.add(chunk_id)
                    merged_evidence.append(chunk)
                    
                    logger.info(
                        f"  └─ Retrieved Chunk [{chunk_id}] | Score: {chunk.get('similarity_score', 0):.4f} "
                        f"| Metadata: {chunk.get('metadata', {})}"
                    )

        # Sort merged evidence descending by similarity score
        merged_evidence.sort(key=lambda x: x.get("similarity_score", 0.0), reverse=True)

        return merged_evidence

    @staticmethod
    def retrieve_medical_evidence(search_query: str, top_k: int = 3, min_score: float = 0.20) -> List[Dict[str, Any]]:
        """Fallback vector retrieval by raw search query."""
        logger.info(f"[VECTOR RAG] Query: '{search_query[:120]}...'")
        return vector_store_instance.similarity_search(query=search_query, top_k=top_k, min_score=min_score)

# Backward Compatibility Aliases
ClinicalVectorRetriever = TargetedBiomarkerRetriever
ClinicalRetriever = TargetedBiomarkerRetriever
