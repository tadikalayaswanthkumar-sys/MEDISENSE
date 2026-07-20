"""
MediSense AI - Targeted Semantic Retriever with Metadata Filtering & Audit Logging
Executes targeted vector search independently for EACH abnormal biomarker,
applies metadata filters, deduplicates chunks, and logs complete audit traces.
"""

import logging
from typing import List, Dict, Any
from app.rag.vector_db import vector_db

logger = logging.getLogger("uvicorn.error")

class MedicalRetriever:
    @staticmethod
    def retrieve_medical_evidence(
        abnormal_findings: List[Dict[str, Any]],
        top_k_per_biomarker: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Executes vector similarity search independently for EACH abnormal biomarker.
        Filters by category metadata, merges evidence, and ranks by similarity score.
        """
        if not abnormal_findings:
            logger.info("[RETRIEVER LOG] No abnormal findings. Executing baseline wellness retrieval.")
            return vector_db.query("optimal blood wellness baseline", top_k=2)

        category_map = {
            "hemoglobin": "cbc", "wbc": "cbc", "rbc": "cbc", "platelets": "cbc", "mcv": "cbc", "mch": "cbc",
            "glucose": "diabetes", "hba1c": "diabetes", "insulin": "diabetes",
            "creatinine": "kidney", "bun": "kidney", "egfr": "kidney",
            "alt": "liver", "ast": "liver", "bilirubin": "liver",
            "tsh": "thyroid", "t3": "thyroid", "t4": "thyroid",
            "cholesterol": "lipid", "hdl": "lipid", "ldl": "lipid", "triglycerides": "lipid",
            "vitamin_d": "vitamins", "vitamin_b12": "vitamins", "ferritin": "vitamins"
        }

        merged_chunks = []
        seen_ids = set()

        for finding in abnormal_findings:
            biomarker = finding.get("biomarker") or finding.get("key", "").lower()
            name = finding.get("name", biomarker.capitalize())
            status = finding.get("status", "Abnormal")
            category = category_map.get(biomarker, "")

            # 1. Structured Targeted Query Construction
            structured_query = (
                f"Biomarker: {name}\n"
                f"Status: {status}\n"
                f"Clinical Context: {finding.get('description', '')}\n"
                f"Need: Interpretation, Lifestyle recommendations, Clinical significance, Risk explanation"
            )

            logger.info(f"[RETRIEVER QUERY] Biomarker: '{biomarker}' ({category}) | Query:\n{structured_query}")

            # 2. Metadata Filtered Search
            metadata_filter = {"category": category} if category else None
            chunks = vector_db.query(
                query_text=structured_query,
                metadata_filter=metadata_filter,
                top_k=top_k_per_biomarker
            )

            # Fallback search without category filter if specific chunk empty
            if not chunks:
                chunks = vector_db.query(query_text=structured_query, top_k=top_k_per_biomarker)

            # 3. Merge & Deduplicate
            for chunk in chunks:
                c_id = chunk.get("id") or chunk.get("metadata", {}).get("chunk_id")
                if c_id not in seen_ids:
                    seen_ids.add(c_id)
                    merged_chunks.append(chunk)
                    logger.info(
                        f"  └─ Retrieved Chunk [{c_id}] | Score: {chunk.get('similarity_score', 0):.4f} "
                        f"| Metadata: {chunk.get('metadata', {})}"
                    )

        # Sort merged evidence descending by similarity score
        merged_chunks.sort(key=lambda x: x.get("similarity_score", 0.0), reverse=True)
        return merged_chunks

# Backward Compatibility Aliases
ClinicalVectorRetriever = MedicalRetriever
TargetedBiomarkerRetriever = MedicalRetriever
