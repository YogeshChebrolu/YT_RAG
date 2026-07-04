import { useSelecteNotes } from "@/context/SelectedNotesContext";
import { Button } from "../ui/button";
import { X, FileText } from "lucide-react";

interface AttachedNotesCardProps {
  inputMode: "notes" | "normal" | "attach";
}

export function AttachedNotesCard({ inputMode }: AttachedNotesCardProps) {
  const { selectedNotes, setSelectedNotes } = useSelecteNotes();

  // Only show when in attach mode and there are selected notes
  if (inputMode !== "attach" || selectedNotes.length === 0) {
    return null;
  }

  const removeNote = (noteId: string) => {
    setSelectedNotes(selectedNotes.filter(note => note.notes_id !== noteId));
  };

  const clearAllNotes = () => {
    setSelectedNotes([]);
  };

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-md p-2 mb-3">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-1">
          <FileText className="w-3 h-3 text-blue-600" />
          <span className="text-xs font-medium text-blue-800">
            Notes ({selectedNotes.length})
          </span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={clearAllNotes}
          className="h-5 w-5 p-0 text-blue-600 hover:text-blue-800 hover:bg-blue-100"
        >
          <X className="w-3 h-3" />
        </Button>
      </div>
      
      <div className="flex flex-wrap gap-1">
        {selectedNotes.map((note) => (
          <div 
            key={note.notes_id} 
            className="flex items-center gap-1 bg-white border border-blue-200 rounded px-2 py-1 text-xs"
          >
            <span className="text-gray-700 truncate max-w-[120px]">
              {note.heading_text || "Untitled"}
            </span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => removeNote(note.notes_id)}
              className="h-3 w-3 p-0 text-gray-400 hover:text-gray-600 hover:bg-gray-100"
            >
              <X className="w-2 h-2" />
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}
