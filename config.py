"""
Central configuration for the Multi-Document RAG Chatbot.

All modules (auth, ingestion, chunking, retrieval, qa, services) should
import settings from here rather than reading environment variables
directly. This keeps configuration changes (e.g. swapping LLM providers)
to a single file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------
# LLM provider: Groq
# --------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Groq-hosted model used for answer generation.
# llama-3.3-70b-versatile is a strong general-purpose choice on Groq;
# swap to a smaller model (e.g. llama-3.1-8b-instant) for lower latency/cost.
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "1024"))
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.2"))

# --------------------------------------------------------------------------
# Document parsing
# --------------------------------------------------------------------------
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY", "")

# --------------------------------------------------------------------------
# Web search fallback
# --------------------------------------------------------------------------
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# --------------------------------------------------------------------------
# Storage paths
# --------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
CHUNKS_DIR = os.path.join(DATA_DIR, "chunks")
CHAT_LOGS_DIR = os.path.join(DATA_DIR, "chat_logs")
VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_store")
SQLITE_DB_PATH = os.path.join(DATA_DIR, "app.db")

for _dir in (DATA_DIR, UPLOADS_DIR, CHUNKS_DIR, CHAT_LOGS_DIR, VECTOR_DB_DIR):
    os.makedirs(_dir, exist_ok=True)

# --------------------------------------------------------------------------
# Chunking
# --------------------------------------------------------------------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))       # tokens
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))  # tokens

# --------------------------------------------------------------------------
# Retrieval
# --------------------------------------------------------------------------
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
RELEVANCE_SCORE_THRESHOLD = float(os.getenv("RELEVANCE_SCORE_THRESHOLD", "0.35"))

# --------------------------------------------------------------------------
# Supported document types
# --------------------------------------------------------------------------
SUPPORTED_EXTENSIONS = {".pdf", ".json", ".md", ".txt"}
