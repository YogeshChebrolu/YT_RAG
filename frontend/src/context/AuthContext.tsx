import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { Session } from "@supabase/supabase-js"
import { supabase } from "@/lib/supabase";

export interface SessionContextInterface {
  session: Session | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setSession: (session: Session | null) => void;
  logout: () => Promise<void>;
}

const SessionContext = createContext<SessionContextInterface | null>(null)

interface sessionContextProviderProps {
  children: ReactNode
}

export const SessionContextProvider = ({children}: sessionContextProviderProps)=>{
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const isAuthenticated = !!session;

  const logout = async () => {
    try {
      await supabase.auth.signOut();
      setSession(null);
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  useEffect(()=>{
    const getSession = async () => {
      try {
        const sessionData = await supabase.auth.getSession();
        setSession(sessionData?.data?.session);
      } catch (error) {
        console.error("Error getting session:", error);
        setSession(null);
      } finally {
        setIsLoading(false);
      }
    };

    void getSession();

    // Listen for auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      console.log("Auth state changed:", event, session);
      
      if (event === 'SIGNED_OUT' || event === 'TOKEN_REFRESHED') {
        setSession(session);
      } else if (event === 'SIGNED_IN') {
        setSession(session);
      } else if (event === 'USER_UPDATED') {
        setSession(session);
      }
      
      // Handle session expiry
      if (!session && event !== 'SIGNED_OUT') {
        console.log("Session expired, logging out");
        setSession(null);
      }
      
      setIsLoading(false);
    });

    return () => {
      subscription.unsubscribe();
    };
  }, [])
  
  return (
    <SessionContext.Provider value={{session, isAuthenticated, isLoading, setSession, logout}}>
      {children}
    </SessionContext.Provider>
  )
}


function useSession() {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error("useSession must be used within a SessionProvider")
  }
  return context;
}

export { SessionContext, useSession};