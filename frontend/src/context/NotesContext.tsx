import { createContext, useContext, useState, ReactNode, useEffect } from "react";
import { Notes } from "@/components/notes/NotesPage";
import { supabase } from "@/lib/supabase";
import { useSession } from "./AuthContext";


interface NotesContextInterface {
  notes: Notes[];
  setNotes: (notes: Notes[]) => void;
  sortOrder: "newest" | "oldest";
  setSortOrder: (order: "newest" | "oldest") => void;
}

const NotesContext = createContext<NotesContextInterface | null>(null);

interface NotesContextProviderProps {
  children: ReactNode;
}

export const NotesContextProvider = ({children} : NotesContextProviderProps) => {
  const [ notes, setNotes ] = useState<Notes[]>([]);
  const [ sortOrder, setSortOrder ] = useState<"newest" | "oldest">("newest");
  const { session } = useSession();

  const userId = session?.user?.id

  const fetchNotes = async () => {
    const { data, error } = await supabase
      .from('notes')
      .select("notes_id, user_id, video_id, notes, heading_text, created_at")
      .eq("user_id", userId)
      .order("created_at", { ascending: sortOrder === "oldest" })

      if (error) console.error("Error fetching notes: ", error)
      else setNotes(data);
  }

  useEffect(() => {
    if (!userId) return;
    fetchNotes();

    const channel = supabase
    .channel("realtime-notes")
    .on(
      'postgres_changes',
      {
        event: "*",
        schema: 'public',
        table: "notes",
        filter: `user_id=eq.${userId}`
      },
      (payload) => {
        console.log(`Realtime change received!`, payload)
        setNotes((prevNotes) => {
          switch(payload.eventType){
            case "INSERT":
              return [payload.new as Notes, ...prevNotes];
            case "UPDATE":
              return prevNotes.map((n) => 
                n.notes_id === (payload.new as Notes).notes_id ? payload.new as Notes : n
              )
            case "DELETE":
              return prevNotes.filter((n) => n.notes_id !== (payload.old as Notes).notes_id);
            default:
              return prevNotes
          }

        })
      }
    ).subscribe();

    //clean up on unmount
    return () => {
      supabase.removeChannel(channel);
    }
  }, [userId, ]);

  useEffect (() => {
    if (userId) {
      fetchNotes();
    }
  }, [sortOrder]);

  return <NotesContext.Provider value={{notes, setNotes, sortOrder, setSortOrder}}>
    {children}
  </NotesContext.Provider>
}

function useNotes() {
  const context = useContext(NotesContext);
  if (!context) {
    throw new Error("useNotes must be used inside a NotesContextProvider");
  }
  return context;
}

export {useNotes, NotesContext}