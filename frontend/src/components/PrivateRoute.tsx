import { useSession } from "@/context/AuthContext"
import { ReactNode } from "react";
import { Navigate } from "react-router-dom";

interface PrivateRouteProviderProps {
    children: ReactNode
}

export const PrivateRoute = ({children}: PrivateRouteProviderProps) => {
    const { session } = useSession();

    if (session === undefined) {
        console.log("Loading...")
        return <p>Loading...</p>
    }

    return <>{session ? <>{children}</>: <Navigate to="/auth"/>}</>
    
}