import { supabase } from "@/lib/supabase";

export async  function getJWTHeaders(){
    try{
        const {data, error} = await supabase.auth.getSession()
        if (error) {
            return {
                "Authorization" : "",
            }
        }
        const jwtToken = data?.session?.access_token

        if (!jwtToken) {
            console.warn("No JWT token available");
            return {
                "Authorization": ""
            }
        }
        return {
            "Authorization": `Bearer ${jwtToken}`
        }

    } catch(error) {
        console.error("Failed to get jwt token")
        return {
            "Authorization": ""
        }
    }
}