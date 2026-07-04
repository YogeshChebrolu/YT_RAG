import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { useState } from "react";
import { NotesCardPreview } from "./NotesCardPreview"
import { Calendar } from "lucide-react";
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm";
import { Notes } from "./NotesPage";

interface NotesCardProps {
  note: {
    notes_id: string
    video_id: string;
    notes: string;
    heading_text?: string | null
    created_at?: string
  }
  viewMode?: "grid" | "list"
}

export function NotesCard({ note, viewMode = "grid" }: NotesCardProps) {
  const [open, setOpen] = useState(false)

  const date = note.created_at
  ? new Date(note.created_at).toLocaleDateString()
  : "—"

  return (
    <>
      <Card
        className={`w-full cursor-pointer border hover:shadow-lg transition-all duration-200 rounded-lg ${
          viewMode === "list" 
            ? "flex flex-row items-center p-4" 
            : "flex flex-col"
        }`}
        onClick={()=> setOpen(true)}
      >
        {viewMode === "list" ? (
          // List view layout
          <>
            <div className="flex-1 min-w-0">
              <CardTitle className="text-base font-semibold truncate mb-1">
                {note.heading_text || "Untitled Note"}
              </CardTitle>
              <CardDescription className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Calendar size={14}/>
                {date}
              </CardDescription>
              <div className="text-sm text-muted-foreground truncate">
                {note.notes ? (
                  <span>{note.notes.slice(0, 100)}{note.notes.length > 100 ? "..." : ""}</span>
                ) : (
                  <span className="italic">*No content*</span>
                )}
              </div>
            </div>
            <div className="ml-4 text-xs text-muted-foreground">
              Video: {note.video_id}
            </div>
          </>
        ) : (
          // Grid view layout
          <>
            <CardHeader>
              <CardTitle className="text-lg font-semibold truncate">
                {note.heading_text || "Untitled Note"}
              </CardTitle>
              <CardDescription className="flex items-center gap-2 text-sm text-muted-foreground">
                <Calendar size={14}/>
                {date}
              </CardDescription>
            </CardHeader>

            <CardContent>
              {note.notes ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  { note.notes.slice(0, 100) + "..."}
                </ReactMarkdown>
              ) : (
                <p className="text-muted-foreground italic">*No content*</p>
              )}
            </CardContent>
          </>
        )}

      </Card>

      {/**Preview Modal */}
      <NotesCardPreview 
        note={note as Notes}
        open={open}
        onOpenChange={setOpen}
      />
    </>
  )

}