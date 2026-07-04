import { useSession } from "@/context/AuthContext";
import { supabase } from "@/lib/supabase";
import { useState } from "react";
import { Button } from "./ui/button";
import { Label } from "./ui/label";
import { Input } from "./ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MessageCircle, Mail, Lock } from "lucide-react";

type AuthResult<T=any> = {
  success: boolean;
  data?: T;
  error?: string;
}


export function AuthPage() {
  const {session} = useSession();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  console.log("session: ", session)

  const signUpNewUser = async (email: string, password: string): Promise<AuthResult> => {
    try{
      const { data, error } = await supabase.auth.signUp({
        email: email,
        password: password,
      });
  
      if (error) {
        console.error("Error occurred during signIn", error)
        return { success: false, error: error.message}
      }
      return {success: true, data}
    } catch (error) {
      console.error("Failed to signup: ", error)
      return { success: false, error: error instanceof Error ? error.message : "Error during signup"}
    }
  }

  const signInUser = async (email: string, password: string): Promise<AuthResult> => {
    try {
      const { data, error } =  await supabase.auth.signInWithPassword({
        email: email,
        password: password,
      });
  
      if (error) {
        console.error("Error occured during signIn")
        return { success: false, error: error.message}
      }
      return { success: true, data}
    } catch (error) {
      console.error("Failed to singin: ", error)
      return { success: false, error: error instanceof Error ? error.message : "Error durin signin"}
    }
  } 

  const handleAuth = async (e: React.FormEvent, isSignUp: boolean) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")

    const formData = new FormData(e.target as HTMLFormElement);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    console.log(email, password)
    try {
      const result = isSignUp
      ? await signUpNewUser(email, password)
      : await signInUser(email, password);

      if (!result.success) {
        setError(result.error || "Authentication failed. Try again");
      }
      // No need to navigate - App.tsx will automatically show ChatPage when authenticated
    } finally {
      setIsLoading(false);
    }
  }
  
  return (
    <div className="w-full h-full flex flex-col p-4 bg-white">
      <div className="w-full">
        <div className="text-center mb-6">
          <div className="mx-auto w-10 h-10 bg-gray-800 rounded-xl flex items-center justify-center mb-3 shadow-lg">
            <MessageCircle className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-xl font-bold text-gray-800">YouTube AI Chat</h1>
          <p className="text-gray-600 text-xs">Your intelligent video companion</p>
        </div>

        <Card className="shadow-lg border-0">
          <CardHeader className="pb-3">
            <CardTitle className="text-lg text-center">Welcome</CardTitle>
            <CardDescription className="text-center text-xs">
              Sign in to start chatting with AI about YouTube videos
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="signin" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6">
                <TabsTrigger
                 className="
                  text-sm font-medium rounded-md py-2
                  data-[state=active]:bg-amber-500 
                  data-[state=active]:text-white 
                  data-[state=active]:scale-105 
                  data-[state=active]:shadow-md
                  transition-all
                "
                 value="signin"
                >
                  Log In
                </TabsTrigger>
                <TabsTrigger
                 className="
                  text-sm font-medium rounded-md py-2
                  data-[state=active]:bg-amber-500 
                  data-[state=active]:text-white 
                  data-[state=active]:scale-105 
                  data-[state=active]:shadow-md
                  transition-all
                  "
                  value="signup"
                >
                  Sign Up
                </TabsTrigger>
              </TabsList>
              
              <TabsContent value="signin">
                <form onSubmit={(e) => handleAuth(e, false)} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="signin-email" className="text-sm font-medium">
                      Email
                    </Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                      <Input
                        id="signin-email"
                        name="email"
                        type="email"
                        placeholder="Enter your email"
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="signin-password" className="text-sm font-medium">
                      Password
                    </Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                      <Input
                        id="signin-password"
                        name="password"
                        type="password"
                        placeholder="Enter your password"
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="text-destructive text-sm p-3 bg-destructive/10 rounded-md">
                      {error}
                    </div>
                  )}

                  <Button 
                    type="submit" 
                    className="w-full bg-gray-800 hover:bg-gray-900 text-white hover:shadow-lg transition-all duration-300" 
                    disabled={isLoading}
                  >
                    {isLoading ? "Signing in..." : "Sign In"}
                  </Button>
                </form>
              </TabsContent>
              
              <TabsContent value="signup">
                <form onSubmit={(e) => handleAuth(e, true)} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="signup-email" className="text-sm font-medium">
                      Email
                    </Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                      <Input
                        id="signup-email"
                        name="email"
                        type="email"
                        placeholder="Enter your email"
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="signup-password" className="text-sm font-medium">
                      Password
                    </Label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                      <Input
                        id="signup-password"
                        name="password"
                        type="password"
                        placeholder="Create a password"
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="text-destructive text-sm p-3 bg-destructive/10 rounded-md">
                      {error}
                    </div>
                  )}

                  <Button 
                    type="submit" 
                    className="w-full bg-gray-800 hover:bg-gray-900 text-white hover:shadow-lg transition-all duration-300" 
                    disabled={isLoading}
                  >
                    {isLoading ? "Creating account..." : "Create Account"}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
