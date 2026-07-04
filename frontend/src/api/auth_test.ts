import { getJWTHeaders } from "./auth"
const API_URL = "http://localhost:8000/core/v1"

export const checkAuthWorking = async () =>{
  try{
    const JWTHeaders = await getJWTHeaders()
    console.log(`Checking JWT headers: ${JSON.stringify(JWTHeaders)}`)
    const response = await fetch(`${API_URL}/check_auth`, {
      method: "GET",
      headers: {
        ...JWTHeaders,
        "Content-Type": "application/json"
      }
    })
    const data = await response.json()
    console.log(data.content)
    return data.content
  } catch (error) {
    console.error("Error checking auth correct")
  }
}
