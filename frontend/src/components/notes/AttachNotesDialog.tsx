import { useState, useMemo } from "react";
import { Dialog } from "../ui/dialog";
import { DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import { Notes } from "./NotesPage";
import { useNotes } from "@/context/NotesContext";
import { useSelecteNotes } from "@/context/SelectedNotesContext";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { Search, X } from "lucide-react";
import { AttachNotesCard } from "./AttachNotesCard";

interface AttachNotesDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  setInputMode: (mode: "notes" | "normal" | "attach") => void;
}

export function AttachNotesDialog({
  open,
  onOpenChange,
  setInputMode
}: AttachNotesDialogProps){
  const { notes } = useNotes();
  const { selectedNotes, setSelectedNotes } = useSelecteNotes();
  const [searchQuery, setSearchQuery] = useState("");

  const handleOnOpenChange = (newOpen : boolean) => {
    if (!newOpen){
      onOpenChange(newOpen)
    } else{
      setInputMode("normal")
      onOpenChange(newOpen)
    }
  }

  // Filter notes based on search query
  const filteredNotes = useMemo(() => {
    if (!searchQuery.trim()) return notes;
    return notes.filter(note => 
      note.heading_text?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.notes?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.video_id?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [notes, searchQuery]);

  const toggleNoteSelection = (note: Notes) => {
    const isSelected = selectedNotes.some(selected => selected.notes_id === note.notes_id);
    
    if (isSelected) {
      setSelectedNotes(selectedNotes.filter(selected => selected.notes_id !== note.notes_id));
    } else {
      setSelectedNotes([...selectedNotes, note]);
    }
  };

  const isNoteSelected = (note: Notes) => {
    return selectedNotes.some(selected => selected.notes_id === note.notes_id);
  };

  const handleAttach = () => {
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={handleOnOpenChange}>
      <DialogContent className="w-[min(90vw,900px)] max-h-[80vh] bg-white text-black p-4 sm:p-6 overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-xl font-semibold">Select Notes to Attach</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4 overflow-x-hidden">
          {/* Search Bar */}
          <div className="relative border-[1px] border-gray-200 rounded-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              placeholder="Search notes by title, content, or video ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-3 focus-visible:ring-0 focus-visible:ring-offset-0"
            />
          </div>

          {/* Selected Notes Count */}
          {selectedNotes.length > 0 && (
            <div className="text-sm text-muted-foreground">
              {selectedNotes.length} note(s) selected
            </div>
          )}

          {/* Notes List */}
          <div className="max-h-[60vh] overflow-y-auto overflow-x-hidden space-y-2 pr-1 -mr-1 w-full">
            {filteredNotes.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                {searchQuery ? "No notes found matching your search" : "No notes available"}
              </div>
            ) : (
              filteredNotes.map((note) => (
                <AttachNotesCard
                  key={note.notes_id}
                  note={note}
                  isSelected={isNoteSelected(note)}
                  onToggle={toggleNoteSelection}
                />
              ))
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex justify-between items-center pt-4 border-t">
            <Button
              variant="outline"
              onClick={() => setSelectedNotes([])}
              disabled={selectedNotes.length === 0}
            >
              <X className="w-4 h-4 mr-2" />
              Clear Selection
            </Button>
            <div className="flex gap-2">
              <Button
                onClick={handleAttach}
                disabled={selectedNotes.length === 0}
                className="bg-blue-500 text-white hover:bg-blue-600"
              >
                Attach {selectedNotes.length > 0 ? `(${selectedNotes.length})` : ''} Notes
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}