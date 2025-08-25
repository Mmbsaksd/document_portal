import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("Checking environment variables...")

print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
print("LLM_PROVIDER:", os.getenv("LLM_PROVIDER"))
