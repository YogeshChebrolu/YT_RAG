import './App.css'
import { useSession } from './context/AuthContext'
import { AuthPage } from './components/AuthPage'
import { Toaster } from 'react-hot-toast'
import { Navigate } from 'react-router-dom'

function App() {
  const { session, isAuthenticated, isLoading } = useSession()

  console.log("App.tsx session state:", { session, isAuthenticated, isLoading })

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="w-full h-screen bg-white flex items-center justify-center p-4 overflow-hidden">
        <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-6 w-full text-center">
          <h1 className="text-xl font-bold text-gray-800 mb-3">
            YouTube RAG Assistant
          </h1>
          <p className="text-gray-600 mb-4 text-sm">
            Loading your personalized YouTube chat experience...
          </p>
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-800 mx-auto"></div>
        </div>
      </div>
    )
  }

  // Redirect to chat if authenticated, otherwise show auth page
  if (isAuthenticated) {
    return <Navigate to="/chat" replace />
  }

  return (
    <>
    <div className="w-full h-screen bg-white overflow-hidden">
      <AuthPage />
    </div>
    <Toaster position="top-right" reverseOrder={false}/>
    </>
  )
}

export default App
