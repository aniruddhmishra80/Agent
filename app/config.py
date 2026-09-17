import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory: root of the repository
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Path configuration
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "source_data.json"
CHROMA_DIR = DATA_DIR / "chroma"
DB_PATH = DATA_DIR / "agent_audit.db"

# LLM & Embedding configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# API Server configuration
API_PORT = int(os.getenv("API_PORT", "8000"))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

# Candidate & Project Metadata
AUTHOR_NAME = "Aniruddh Mishra"
INSTITUTION = "Bennett University"
COHORT = "AIONOS Batch 2027"
ASSIGNMENT_TITLE = "Executive Productivity Agent (Assignment 1)"
TARGET_USER = "Arjun Malhotra (VP Sales)"
SCENARIO_WEEK = "21-25 September 2026"
