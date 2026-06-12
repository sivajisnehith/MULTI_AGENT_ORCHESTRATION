# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter — one key, all models
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Models
MAIN_MODEL = "anthropic/claude-3.5-sonnet"  # supervisor + report
FAST_MODEL = "openai/gpt-4o-mini"           # simple tasks
CODE_MODEL = "openai/gpt-4o"               # code generation

# RAG settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5
PERSIST_DIR = "./knowledge_base"
CACHE_DIR = "./embedding_cache"

# Agent settings
MAX_ITERATIONS = 6