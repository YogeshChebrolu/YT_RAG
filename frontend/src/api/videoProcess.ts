import { getJWTHeaders } from "./auth";
import { API_URL } from "./constants";

export interface VideoStatusRequest{
  videoId: string
}

export async function checkVideoStatus(videoId: string){
  try {
    const JWTheader = await getJWTHeaders();
    const response = await fetch(`${API_URL}/video/${videoId}/video_status`, {
      method: "GET",
      headers: {
        ...JWTheader,
        "Content-Type": "application/json"
      }
    });
  
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to check video status', error);
  }
}

export async function processVideo(videoId: string) {
  try {
    const JWTheader = await getJWTHeaders();
    const response = await fetch(`${API_URL}/video/${videoId}/process_video`, {
      method: "POST",
      headers: {
        ...JWTheader,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error sending request for processing video");
    }

    const data = await response.json()
    return data;
  } catch (error) {
    console.error("Failed during sending request to process video")
  }
}