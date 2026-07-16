import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
for m in client.models.list_models():
    print(m.name, getattr(m, 'supported_generation_methods', []))
