from yt_rag.llm_service.gemini_client import get_gemini_client
import json

def ChatGemini(prompt, system_prompt, images=None, use_memory=True, conversation_memory=None):
    client = get_gemini_client()
    
    if use_memory and conversation_memory:
        contents = conversation_memory + [prompt]
    else:
        contents = [prompt]
    
    if images:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[images, prompt]  
        )
    else:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={
                "system_instruction": system_prompt
            }
        )
    
    if use_memory and conversation_memory is not None:
        conversation_memory.append(prompt)
        conversation_memory.append(response.text)
        
        max_memory_entries = 20 
        if len(conversation_memory) > max_memory_entries:
            conversation_memory[:] = conversation_memory[-max_memory_entries:]
    
    return response

def clear_memory(conversation_memory):
    """Clear all conversation history"""
    conversation_memory.clear()

def get_memory_size(conversation_memory):
    """Get current number of messages in memory"""
    return len(conversation_memory)

def save_memory_to_file(filename, conversation_memory):
    """Save conversation memory to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(conversation_memory, f, indent=2)

def load_memory_from_file(filename, conversation_memory):
    """Load conversation memory from a JSON file"""
    try:
        with open(filename, 'r') as f:
            loaded = json.load(f)
            conversation_memory[:] = loaded
        print(f"Loaded {len(conversation_memory)} messages from {filename}")
    except FileNotFoundError:
        print(f"File {filename} not found. Starting with empty memory.")
        conversation_memory.clear()
    except json.JSONDecodeError:
        print(f"Error reading {filename}. Starting with empty memory.")
        conversation_memory.clear()