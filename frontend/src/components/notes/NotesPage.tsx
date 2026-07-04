import { useNavigate } from "react-router-dom";
import { useState, useMemo } from "react";
import { Button } from "../ui/button";
import { ArrowLeft, SortAsc, SortDesc, Youtube, FileText, Grid, List, Search, Video } from "lucide-react";
import { Label } from "../ui/label";
import { Select, SelectContent, SelectItem } from "../ui/select";
import { SelectTrigger, SelectValue } from "@radix-ui/react-select";
import { Input } from "../ui/input";
import { NotesCard } from "./NotesCard";
import { useNotes } from "@/context/NotesContext";
import { Ban } from "lucide-react";
export interface Notes{
  "notes_id": string;
  "video_id": string;
  "notes": string;
  "heading_text": string;
  "created_at": string;
}

export function NotesPage(){
  const navigate = useNavigate();
  const { notes, sortOrder, setSortOrder} = useNotes();
  // const [sortOrder, setSortOrder] = useState<"newest" | "oldest">("newest");
  const [ groupByVideo, setGroupByVideo ] = useState<boolean>(false);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  // const { session } = useSession();

  // const userId = session?.user.id
  // // console.log("user id", session?.user?.id)

  // const fetchNotes = async () => {
  //   const { data, error } = await supabase
  //     .from('notes')
  //     .select("notes_id, user_id, video_id, notes, heading_text, created_at")
  //     .eq("user_id", userId)
  //     .order("created_at", { ascending: sortOrder === "oldest" })

  //     if (error) console.error("Error fetching notes: ", error)
  //     else setNotes(data);
  // }
  // console.log("Fetched notes: ", notes)

  // useEffect(()=>{
  //   if (!userId) return;
  //   fetchNotes();

  //   const channel = supabase
  //   .channel("realtime-notes")
  //   .on(
  //     'postgres_changes',
  //     {
  //       event: "*",
  //       schema: 'public',
  //       table: "notes",
  //       filter: `user_id=eq.${userId}`,
  //     },
  //     (payload) => {
  //       console.log('Realtime change received!', payload);

  //        setNotes((prevNotes) => {
  //         switch(payload.eventType) {
  //           case 'INSERT':
  //             return [payload.new as Notes, ...prevNotes];
  //           case 'UPDATE':
  //             return prevNotes.map((n) =>
  //               n.notes_id === (payload.new as Notes).notes_id ? payload.new as Notes : n
  //             )
  //           case "DELETE":
  //             return prevNotes.filter((n)=> n.notes_id !== (payload.old as Notes).notes_id);
  //           default:
  //             return prevNotes
  //         }
  //       });
  //     }
  //   )
  //   .subscribe();

  //   //clean up on unmount
  //   return ()=> {
  //     supabase.removeChannel(channel);
  //   };

  // }, [userId])

  // useEffect(() => {
  //   if (userId) fetchNotes();
  // }, [sortOrder]);

  // Filter and search notes
  const filteredNotes = useMemo(() => {
    if (!searchQuery.trim()) return notes;
    return notes.filter(note => 
      note.heading_text?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.notes?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.video_id?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [notes, searchQuery]);

  // Group notes by video_id
  const groupedNotes = useMemo(() => {
    if (!groupByVideo) return { all: filteredNotes };
    const groups: Record<string, Notes[]> = {};
    for (const note of filteredNotes) {
      if (!groups[note.video_id]) groups[note.video_id] = [];
      groups[note.video_id].push(note);      
    }
    return groups;
  }, [filteredNotes, groupByVideo])

  return (
    <div className="h-full w-full flex flex-col bg-background">
      {/* Header */}
      <div className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate("/chat")}
                className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
              >
                <ArrowLeft className="w-4 h-4" />
                Back to Chat
              </Button>
              <div className="h-6 w-px bg-border" />
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary" />
                <h1 className="text-xl font-semibold">My Notes</h1>
                <span className="text-sm text-muted-foreground">({filteredNotes.length})</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-7xl mx-auto p-6">
          {/* Search and Filters */}
          <div className="mb-6 space-y-4">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                placeholder="Search notes by title, content, or video ID..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Toolbar */}
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                {/* Sort */}
                <div className="flex items-center gap-2">
                  <Label className="text-sm font-medium">Sort by</Label>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSortOrder(sortOrder === "newest" ? "oldest" : "newest")}
                    className="flex items-center gap-2"
                  >
                    {sortOrder === "newest" ? (
                      <>
                        <SortDesc className="w-4 h-4" />
                        Newest
                      </>
                    ) : (
                      <>
                        <SortAsc className="w-4 h-4" />
                        Oldest
                      </>
                    )}
                  </Button>
                </div>

                {/* Group By */}
                <div className="flex items-center space-x-2">
                  <Label className="text-sm font-medium ">Group by</Label>
                  <Select
                    onValueChange={(val) => setGroupByVideo(val === "video")}
                    defaultValue="none"
                  >
                    <SelectTrigger className="w-28 border rounded px-3 py-1 text-sm">
                      <SelectValue placeholder="None" />
                    </SelectTrigger>
                    <SelectContent className="bg-white border rounded shadow-sm ">
                      <SelectItem value="none"><span className="font-semibold flex item-center gap-2"><Ban className="w-4 h-4 my-auto"/>None</span></SelectItem>
                      <div className="border-t-1 mx-2"></div>
                      <SelectItem value="video"><span className="font-semibold flex items-center gap-2"><Video className="w-4 h-4"/>Video Id</span></SelectItem>
                    </SelectContent>
                  </Select>
                </div>

              </div>

              {/* View Mode Toggle */}
              <div className="flex items-center gap-1 border rounded-lg p-1">
                <Button
                  variant={viewMode === "grid" ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setViewMode("grid")}
                  className={`h-8 w-8 p-0 ${
                      viewMode === "grid"
                      ? "bg-gray-100"
                      : ""
                    }`}
                >
                  <Grid className="w-4 h-4" />
                </Button>
                <div className="border-1 h-7"></div>
                <Button
                  variant={viewMode === "list" ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setViewMode("list")}
                  className={`h-8 w-8 p-0 ${
                      viewMode === "list" 
                      ? "bg-gray-100"
                      : ""
                    }`}
                >
                  <List className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Notes Display */}
          {filteredNotes.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <FileText className="w-12 h-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium text-muted-foreground mb-2">
                {searchQuery ? "No notes found" : "No notes yet"}
              </h3>
              <p className="text-sm text-muted-foreground max-w-md">
                {searchQuery 
                  ? "Try adjusting your search terms or clear the search to see all notes."
                  : (<div className="font-medium text-md">
                    <span className="grid">"Start creating notes by chatting with your videos to see them appear here."</span>
                    <Button
                      className="rounded-lg bg-blue-500 text-white hover:bg-blue-600 px-4 py-2 m-4"
                      onClick={()=>(navigate("/chat"))}
                    >
                      Go to Chat
                    </Button>
                    </div>
                  )
                }
              </p>
              {searchQuery && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSearchQuery("")}
                  className="mt-4"
                >
                  Clear search
                </Button>
              )}
            </div>
          ) : !groupByVideo ? (
            // Flat view
            <div className={`grid gap-4 ${
              viewMode === "grid" 
                ? "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" 
                : "grid-cols-1"
            }`}>
              {filteredNotes.map((note) => (
                <NotesCard 
                  key={note.notes_id}
                  note={note}
                  viewMode={viewMode}
                />
              ))}
            </div>
          ) : (
            // Grouped view
            <div className="space-y-8">
              {Object.entries(groupedNotes).map(([videoId, group]) => (
                <div key={videoId} className="space-y-4">
                  <div className="flex items-center gap-2 pb-2 border-b">
                    <Youtube className="w-5 h-5 text-primary" />
                    <h3 className="text-lg font-semibold">
                      Video: {videoId}
                    </h3>
                    <span className="text-sm text-muted-foreground">({group.length} notes)</span>
                  </div>
                  <div className={`grid gap-4 ${
                    viewMode === "grid" 
                      ? "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" 
                      : "grid-cols-1"
                  }`}>
                    {group.map((note) => (
                      <NotesCard 
                        key={note.notes_id} 
                        note={note} 
                        viewMode={viewMode}
                      />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}