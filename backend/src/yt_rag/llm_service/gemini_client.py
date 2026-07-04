from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

def get_gemini_client():
  gemini_client=genai.Client(
    api_key=os.getenv('GOOGLE_API_KEY')
  )
  return gemini_client