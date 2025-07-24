from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env from the current file's directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure GEMINI_API_KEY is set in .env")

genai.configure(api_key=api_key)

def ask_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
