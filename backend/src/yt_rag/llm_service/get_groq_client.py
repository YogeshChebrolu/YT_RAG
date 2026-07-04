import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

def get_gemma_client():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    return client
