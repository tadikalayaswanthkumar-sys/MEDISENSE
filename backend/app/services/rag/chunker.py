"""
MediSense AI - Document Chunker with Rich Metadata
Chunks markdown clinical reference documents into 300-500 token windows with 50-token overlap.
"""

import os
import glob
from typing import List, Dict, Any

class DocumentChunker:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1400, overlap: int = 200, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Splits text into chunks of 300-500 tokens with overlap window and metadata.
        """
        if not text:
            return []

        chunks = []
        text_length = len(text)
        start = 0
        chunk_id = 0

        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            if end < text_length:
                last_period = text.rfind('.', start, end)
                if last_period > start + (chunk_size // 2):
                    end = last_period + 1

            chunk_content = text[start:end].strip()

            if chunk_content:
                chunk_meta = (metadata or {}).copy()
                chunk_meta.update({
                    "chunk_id": chunk_id,
                    "token_estimate": len(chunk_content.split())
                })
                
                chunks.append({
                    "id": f"chunk_{chunk_id}",
                    "text": chunk_content,
                    "metadata": chunk_meta
                })
                chunk_id += 1

            if end >= text_length:
                break

            start = max(end - overlap, start + 1)

        return chunks

    @staticmethod
    def chunk_markdown_file(file_path: str, chunk_size: int = 1400, overlap: int = 200) -> List[Dict[str, Any]]:
        """
        Reads a markdown document and chunks it into 300-500 token sections with overlap and metadata.
        """
        if not os.path.exists(file_path):
            return []

        filename = os.path.basename(file_path)
        biomarker_key = filename.replace('.md', '').lower()

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        category = "General Medical"
        for line in content.split('\n'):
            if "Category:" in line:
                category = line.split("Category:")[-1].strip()
                break

        chunks = []
        text_length = len(content)
        start = 0
        chunk_id = 0

        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            if end < text_length:
                last_period = content.rfind('.', start, end)
                if last_period > start + (chunk_size // 2):
                    end = last_period + 1

            chunk_text = content[start:end].strip()

            if chunk_text:
                chunks.append({
                    "id": f"{biomarker_key}_chunk_{chunk_id}",
                    "text": chunk_text,
                    "metadata": {
                        "biomarker": biomarker_key,
                        "biomarker_key": biomarker_key,
                        "category": category,
                        "source_file": filename,
                        "chunk_index": chunk_id,
                        "token_estimate": len(chunk_text.split())
                    }
                })
                chunk_id += 1

            if end >= text_length:
                break

            start = max(end - overlap, start + 1)

        return chunks

    @staticmethod
    def load_all_document_chunks(documents_dir: str) -> List[Dict[str, Any]]:
        """
        Loads and chunks all markdown medical documents in the documents repository.
        """
        all_chunks = []
        md_files = glob.glob(os.path.join(documents_dir, "*.md"))

        for file_path in md_files:
            file_chunks = DocumentChunker.chunk_markdown_file(file_path)
            all_chunks.extend(file_chunks)

        return all_chunks
