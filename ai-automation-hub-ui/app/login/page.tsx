"use client";
import { supabase } from "@/lib/supabase";

export default function LoginPage() {
  const login = async () => {
    await supabase.auth.signInWithOtp({
      email: prompt("Enter email")!,
    });
  };

  return (
    <div>
      <h1>Login</h1>
      <button onClick={login}>Login with Email</button>
    </div>
  );
}
