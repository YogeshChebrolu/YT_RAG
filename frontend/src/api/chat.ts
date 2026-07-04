import { getJWTHeaders } from "./auth";

const API_URL = "http://localhost:8000/core/v1"

export interface ChatRequest{
    video_id: string
    query: string
    notes_ids?: string[]
    // user_id: string
}

export async function sendChatMessage(request: ChatRequest ){
  const JWTheaders = await getJWTHeaders();
  try{
    const response = await fetch(`${API_URL}/chat/generate`, {
      method: "POST",
      headers: {
        ...JWTheaders,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.statusText}`)
    }

    const data = await response.json();
    console.log(data)
    return data.content;
  } catch (error) {
    console.log("Failed to send chat messages", error);
    return 'Error: could not reach backend';
  }
}

export interface HistoryRequest{
  video_id: string
}
export async function getChatHistory( request: HistoryRequest ){
  const JWTheaders = await getJWTHeaders();
  try{
    const response = await fetch(`${API_URL}/chat/chat_history`, {
      method: "POST",
      headers: {
        ...JWTheaders,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request)
    });

    const data = await response.json()
    return data;
  } catch (error) {
    console.error(`Failed to get chat history: ${error}`)
    return 'Error: could not retrieve history'
  }
}

