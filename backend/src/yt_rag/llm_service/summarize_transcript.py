from yt_rag.llm_service.get_groq_client import get_gemma_client
from yt_rag.rag_prompts.prompts import summary_prompt
import logging
import traceback
logger = logging.getLogger(__name__)
def summarize_transcript(transcript):
    try:
        # Handle None or empty transcript
        if transcript is None or transcript == "":
            logger.warning("Transcript is None or empty, skipping summarization")
            return "No transcript available for summarization"

        # Convert list to string if needed (for robustness)
        if isinstance(transcript, list):
            logger.warning("Transcript is a list, converting to string")
            # If it's a list of dicts with 'page_content', extract that
            if len(transcript) > 0 and isinstance(transcript[0], dict) and 'page_content' in transcript[0]:
                transcript = " ".join([chunk.get('page_content', '') for chunk in transcript])
            else:
                transcript = str(transcript)

        client = get_gemma_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": summary_prompt,
                },
                {
                    "role": "user",
                    "content": "Please summarize this transcript:\n\n" + transcript,
                }
            ],
            model="openai/gpt-oss-safeguard-20b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in summarize_transcript: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

