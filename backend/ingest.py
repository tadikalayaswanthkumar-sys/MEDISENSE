"""
MediSense AI - Root Vector Database Ingestion Script
Execute: python ingest.py
"""

import sys
import os

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.rag.ingest import run_ingestion

if __name__ == "__main__":
    print("==================================================")
    print("      MediSense AI - Vector DB Ingestion         ")
    print("==================================================")
    run_ingestion()
    print("==================================================")
    print(" Ingestion complete. Vector database ready.      ")
    print("==================================================")
