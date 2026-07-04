import { createHashRouter } from "react-router-dom";
import App from "./App";
import { Layout } from "./Layout";
import { ChatPage } from "./components/chat/ChatPage";
import { NotesPage } from "./components/notes/NotesPage";

// Use hash router for browser extension compatibility
export const router = createHashRouter([
    { 
        path: "/", 
        element: <App />,
        errorElement: <div className="text-center p-4 text-red-500">Something went wrong! Please try again.</div>
    },
    {
        path: "/chat",
        element: <Layout />,
        children: [
            {
                index: true,
                element: <ChatPage />
            }
        ]
    },
    {
        path: "/notes",
        element: <Layout />,
        children: [
            {
                index: true,
                element: <NotesPage />
            }
        ]
    },
    // Catch-all route to redirect to main app
    {
        path: "*",
        element: <App />,
        errorElement: <div className="text-center p-4 text-red-500">Page not found! Redirecting to main app.</div>
    }
], {
    // Add fallback for extension context
    future: {
        v7_normalizeFormMethod: true,
    }
})