from yt_rag.llm_service.get_groq_client import get_gemma_client
from yt_rag.rag_prompts.prompts import summary_prompt
import logging
import traceback
logger = logging.getLogger(__name__)
def summarize_transcript(transcript):
    try:
        client = get_gemma_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                "content": summary_prompt,
            },
            {
                "role": "user",
                "content": "Please summarize this transcript /n"+transcript,
            }
        ],
        model="gemma2-9b-it",
    )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in summarize_transcript: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

