import { createClient } from "@supabase/supabase-js"

// Get environment variables from Vite's import.meta.env
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// Validate that environment variables are set
if (!supabaseUrl) {
  throw new Error("Missing VITE_SUPABASE_URL environment variable")
}

if (!supabaseKey) {
  throw new Error("Missing VITE_SUPABASE_ANON_KEY environment variable")
}

export const supabase = createClient(supabaseUrl, supabaseKey)