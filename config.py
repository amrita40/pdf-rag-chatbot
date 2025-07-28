from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Just read the values — don't set them again
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Check for missing API keys and raise clear error
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file.")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file.")

CHROMA_DIR = "vectorstore_db"
PDF_DIR = "pdfs"
