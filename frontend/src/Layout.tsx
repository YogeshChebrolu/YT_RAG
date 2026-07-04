import { Outlet } from "react-router-dom";
import { Header } from "./components/Header";

export function Layout(){
  return (
    <div className="min-h-screen w-full flex flex-col">
      <Header />
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  )
}