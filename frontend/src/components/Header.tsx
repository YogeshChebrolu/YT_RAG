import { ProfileCard } from "./profile/ProfileCard";

export function Header(){
  return (
  <>
    {/* Header with profile */}
    <div className="border-b bg-card flex items-center justify-between p-3 sticky top-0 z-50 bg-white">
      <div className="flex items-center space-x-2">
        <img
          src="/icons/logo.png"
          alt="Logo"
          className="w-10 h-10 rounded"
          style={{objectFit:"contain"}}
        />
        <h1 className="text-lg font-semibold text-foreground">YouTube RAG Assistant</h1>
      </div>
      <div className="flex items-center space-x-4">
        <ProfileCard/>
      </div>
    </div>
  </>
  )
}