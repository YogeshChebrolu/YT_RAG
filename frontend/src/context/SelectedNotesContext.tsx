import { Notes } from "@/components/notes/NotesPage"
import { ReactNode, createContext, useContext, useState } from "react" 

export interface SelectedNotesContextInterface{
  selectedNotes: Notes[]
  setSelectedNotes: (notes: Notes[]) => void
}

const SelectedNotesContext = createContext<SelectedNotesContextInterface | null>(null);

interface selectedNotesContextProvidetProps{
  children: ReactNode
}

export const SelectedNotesContextProvider = ({children}: selectedNotesContextProvidetProps) => {
  const [selectedNotes, setSelectedNotes] = useState<Notes[]>([])
  return (
    <SelectedNotesContext.Provider value={{selectedNotes, setSelectedNotes}}>
      {children}
    </SelectedNotesContext.Provider>
  )
}

export function useSelecteNotes(){
  const context = useContext(SelectedNotesContext)
  if (!context) throw new Error(`useSelectedNotes can be only within a SelectedNotesContextProvider`)
  return context;
}