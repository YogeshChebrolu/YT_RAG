summary_prompt="""
**Instruction to LLM:**
You are given the full transcript of a YouTube video. Your task is to generate a structured, high-quality summary that captures the key points, arguments, and insights from the video in a way that will help an AI assistant answer questions about it.

**Requirements for the summary:**

* Be concise but comprehensive: cover the main themes, arguments, and conclusions.
* Preserve important details, facts, numbers, names, and examples if they are central to understanding.
* Organize information clearly (e.g., sections, bullet points, or thematic grouping).
* Avoid filler words, tangents, and irrelevant details from the transcript.
* Write it in neutral, factual language (don’t add opinions or interpretations).
* Ensure the summary could stand alone as a reliable reference for answering questions about the video.

**Output format:**
Provide the summary as a structured text (with headings or bullets where helpful).
"""
