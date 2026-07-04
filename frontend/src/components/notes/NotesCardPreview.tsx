import {
  Dialog,
  DialogTitle,
  DialogHeader,
  DialogContent,
  DialogDescription,
  DialogFooter
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { PlayCircle } from "lucide-react"
import { Separator } from "@/components/ui/separator"

import { Notes } from "./NotesPage"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm";


interface NotesCardPreviewProps{
  note: Notes;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function NotesCardPreview({
  note,
  open,
  onOpenChange
}: NotesCardPreviewProps){

  const date = note.created_at
  ? new Date(note?.created_at).toLocaleDateString()
  : "—"
  
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-120 bg-white overflow-y-scroll border-3 border-white">
        <DialogHeader>
          <DialogTitle className="text-sm text-muted-foreground">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {note.heading_text || "Untitled Note"}
            </ReactMarkdown>
          </DialogTitle>
          <DialogDescription className="text-sm text-mute-foreground">
            Created at: {date}
          </DialogDescription>
        </DialogHeader>

      <Separator className="my-2" />

      <div className="space-y-4">
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {note.notes}
          </ReactMarkdown>
        </div>

        <div className="mt-6">
          <h4 className="text-sm font-medium text-muted-foreground mb-2">
            Linked Video
          </h4>

          <div className="flex items-center gap-2 text-blue-600 hover:underline cursor-pointer">
            <PlayCircle size={18} />
            <a
              href={`https://youtube.com/watch?v=${note.video_id}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              {note.video_id}
            </a>
          </div>
        </div>
      </div>

      <DialogFooter>
        <Button 
          variant="outline"
          onClick={() => onOpenChange(false)}
        >
          Close
        </Button>
      </DialogFooter>
      </DialogContent>

    </Dialog>
  )
}