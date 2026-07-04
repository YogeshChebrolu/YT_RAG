import { useSession } from "@/context/AuthContext"
import { useState, useEffect } from "react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel } from "../ui/dropdown-menu"
import { DropdownMenuSeparator, DropdownMenuTrigger } from "@radix-ui/react-dropdown-menu"
import { Button } from "../ui/button"
import { Avatar, AvatarFallback } from "../ui/avatar"
import { ChevronDown, LogOut, Settings, User } from "lucide-react"

export function ProfileCard(){
  const { session, logout } = useSession()
  
  const [userEmail, setUserEmail] = useState<string>("")
  const [isLoggingOut, setIsLoggingOut] = useState(false)
  
  useEffect(()=>{
    if (session) {
      const email: string = session?.user?.email!
      setUserEmail(email)
    }
  }, [session]);

  const handleLogOut = async (e: React.MouseEvent) => {
    try{
      e.preventDefault()
      setIsLoggingOut(true)
      await logout()
    } catch ( error ) {
      console.error("Error during signOut:", error)
    } finally {
      setIsLoggingOut(false)
    }
  }

  const getInitials = (email: string) => {
    if (!email) return "U"
    return email.split("@")[0].slice(0, 2).toUpperCase()
  };

  const getDisplayName = (email: string) => {
    if (!email) return "User"
    return email.split("@")[0]
  };

  if (!session || !userEmail) {
    return null
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="flex items-center space-x-2 h-auto p-2 hover:bg-muted/50 transition-colors rounded-lg">
          <Avatar className="w-8 h-8">
            <AvatarFallback className="bg-primary text-primary-foreground text-xs font-medium">
              {getInitials(userEmail)}
            </AvatarFallback>
          </Avatar>
          <div className="flex flex-col items-start min-w-0">
            <span className="text-sm font-medium text-foreground truncate max-w-[120px]">
              {getDisplayName(userEmail)}
            </span>
          </div>
          <ChevronDown className="w-3 h-3 text-muted-foreground flex-shrink-0"/>
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="end"
        className="w-56 bg-popover border shadow-lg bg-white"
        sideOffset={8}
      >
        <DropdownMenuLabel>
          <div className="flex flex-col space-y-1">
            <div className="flex items-center space-x-2">
              <User className="w-4 h-4 text-muted-foreground" />
              <p className="text-sm font-medium text-foreground">Account</p>
            </div>
            <p className="text-xs text-muted-foreground truncate pl-6">{userEmail}</p>
          </div>
        </DropdownMenuLabel>

        <DropdownMenuSeparator className="my-1 border-gray-500 border-1" />

        <DropdownMenuItem className="cursor-pointer focus:bg-muted/50" disabled>
          <Settings className="w-4 h-4 mr-2"/>
          <span>Settings</span>
        </DropdownMenuItem>

        <DropdownMenuSeparator className="my-1  border-gray-500 border-1" />

        <DropdownMenuItem
          className="cursor-pointer focus:bg-destructive/10 focus:text-destructive text-destructive"
          onClick={handleLogOut}
          disabled={isLoggingOut}
        >
          <LogOut className="w-4 h-4 mr-2" />
          <span>{isLoggingOut ? "Logging out..." : "Log out"}</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}