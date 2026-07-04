import { Notes } from "./NotesPage";
import { Check, Calendar } from "lucide-react";

interface AttachNotesCardProps {
  note: Notes;
  isSelected: boolean;
  onToggle: (note: Notes) => void;
}

export function AttachNotesCard({ note, isSelected, onToggle }: AttachNotesCardProps) {
  const date = note.created_at 
    ? new Date(note.created_at).toLocaleDateString() 
    : "—";

  return (
    <div
      className={`w-full cursor-pointer transition-all duration-200 p-3 rounded-lg border overflow-hidden ${
        isSelected 
          ? "bg-blue-50 border-blue-300 ring-2 ring-blue-200" 
          : "bg-white border-gray-200 hover:border-gray-300 hover:bg-gray-50"
      }`}
      onClick={() => onToggle(note)}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0 overflow-hidden">
          <div className="flex items-center gap-2 mb-1">
            <h4 className="text-sm font-medium text-gray-900 truncate">
              {note.heading_text || "Untitled Note"}
            </h4>
            {isSelected && (
              <Check className="w-4 h-4 text-blue-600 flex-shrink-0" />
            )}
          </div>
          
          <div className="flex items-center gap-2 text-xs text-gray-500 mb-2 min-w-0">
            <Calendar className="w-3 h-3" />
            <span>{date}</span>
            <span>•</span>
            <span className="truncate">Video: {note.video_id}</span>
          </div>
          
          <p className="text-xs text-gray-600 line-clamp-2 break-words whitespace-pre-wrap">
            {note.notes ? (
              note.notes.length > 100 
                ? `${note.notes.slice(0, 100)}...` 
                : note.notes
            ) : (
              <span className="italic text-gray-400">*No content*</span>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
