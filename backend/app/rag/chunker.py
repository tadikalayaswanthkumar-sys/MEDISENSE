"""
MediSense AI - Word-Based Document Chunker
Chunks markdown clinical documents into 300-500 word windows with 50-word overlap.
Attaches biomarker, category, source_file, and chunk_id metadata.
"""

import os
import glob
from typing import List, Dict, Any

class DocumentChunker:
    @staticmethod
    def chunk_markdown_file(file_path: str, chunk_words: int = 350, overlap_words: int = 50) -> List[Dict[str, Any]]:
        """
        Reads a markdown document and chunks it into 300-500 word windows with 50-word overlap.
        """
        if not os.path.exists(file_path):
            return []

        source_file = os.path.basename(file_path)
        biomarker_key = source_file.replace('.md', '').lower()
        category_folder = os.path.basename(os.path.dirname(file_path)).lower()

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        words = content.split()
        total_words = len(words)
        chunks = []
        start = 0
        chunk_index = 0

        while start < total_words:
            end = min(start + chunk_words, total_words)
            chunk_text = " ".join(words[start:end]).strip()

            if chunk_text:
                chunk_id = f"{category_folder}_{biomarker_key}_{chunk_index}"
                chunks.append({
                    "id": chunk_id,
                    "text": chunk_text,
                    "metadata": {
                        "biomarker": biomarker_key,
                        "category": category_folder,
                        "source_file": source_file,
                        "chunk_id": chunk_id,
                        "word_count": len(words[start:end])
                    }
                })
                chunk_index += 1

            if end >= total_words:
                break

            start = max(end - overlap_words, start + 1)

        return chunks

    @staticmethod
    def load_and_chunk_knowledge_directory(knowledge_dir: str) -> List[Dict[str, Any]]:
        """
        Recursively scans and chunks all markdown files across knowledge subdirectories.
        """
        all_chunks = []
        md_pattern = os.path.join(knowledge_dir, "**", "*.md")
        md_files = glob.glob(md_pattern, recursive=True)

        for file_path in md_files:
            file_chunks = DocumentChunker.chunk_markdown_file(file_path)
            all_chunks.extend(file_chunks)

        return all_chunks
