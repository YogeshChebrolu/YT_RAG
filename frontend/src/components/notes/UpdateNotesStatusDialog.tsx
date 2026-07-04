import { updateNotesStatus } from "@/api/notes";
import { Dialog, DialogHeader, DialogTitle, DialogContent } from "@/components/ui/dialog";
import { Notebook } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Button } from "../ui/button";
import toast from "react-hot-toast";

interface NotesContent {
  notes_id: string;
  content: string;
}

interface UpdateNotesStatusDialogProps{
  open: boolean;
  onOpenChange: (open: boolean) => void;
  notesContent: NotesContent | null,
  // setNotesContent: () => void;
}

// interface NotesStatus{
//   status: "APPROVED" | "DISAPPROVED" |  "PENDING"
// }

export function UpdateNotesStatusDialog({
  open,
  onOpenChange,
  notesContent,
  // setNotesContent,
}: UpdateNotesStatusDialogProps){
    const handleOpenChange = (newChange: boolean) => {
        onOpenChange(newChange);
    };

    const  handleNotesStatus = async (notesId: string, status: string) => {
      console.log("Enter update notes status handler with params", notesId, status)
      console.log("Notes state: ", notesContent)
      const response = await updateNotesStatus({
        notes_id : notesId,
        status : status,
      })
      console.log("Response from update route is: ", response)
      if (response) {
        toast.success("Notes is saved")
        onOpenChange(false)
      }
      else {
        toast.error("New notes is discarded")
      }
    }

    return (
        <Dialog open={open} onOpenChange={handleOpenChange}>
          <DialogContent className="sm:max-w-[425px] bg-white text-black">
            <DialogHeader>
              <DialogTitle className="flex gap-2">
                <Notebook className="w-5 h-5 "/> New notes content 
              </DialogTitle>
            </DialogHeader>
            <div className="rounded-2xl px-4 py-3 hover:shadow-md">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {notesContent?.content || `*No content*`}
              </ReactMarkdown>
            </div>
          <div className="flex gap-2">            
          <Button
            size="sm"
            className="bg-gray-400 hover:bg-gray-300"
            onClick={()=> {
              if (notesContent?.notes_id) {
                handleNotesStatus(notesContent.notes_id, "DISAPPROVED")
              }
            }}
          >
            Discard Notes
          </Button>
          <Button
            size="sm"
            className="bg-green-400 hover:bg-green-500"
            onClick={()=> {
              if (notesContent?.notes_id) {
                handleNotesStatus(notesContent.notes_id, "APPROVED")
              }
            }}
          >
            Accept Notes
          </Button>
          </div>
          </DialogContent>
        </Dialog>
  );
}