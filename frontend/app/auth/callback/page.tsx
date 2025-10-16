"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase-client";
import { Loader2, CheckCircle2, XCircle } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function AuthCallbackPage() {
  const router = useRouter();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Case 1: New flow - code exchange (recommended by Supabase v2)
        const url = new URL(window.location.href);
        const code = url.searchParams.get("code");
        if (code) {
          const { error } = await supabase.auth.exchangeCodeForSession(code);
          if (error) throw error;
          setStatus("success");
          setTimeout(() => router.push("/dashboard"), 800);
          return;
        }

        // Case 2: Legacy hash tokens (access_token + refresh_token in hash)
        const hashParams = new URLSearchParams(window.location.hash.substring(1));
        const accessToken = hashParams.get("access_token");
        const refreshToken = hashParams.get("refresh_token");
        if (accessToken && refreshToken) {
          const { error: sessionError } = await supabase.auth.setSession({
            access_token: accessToken,
            refresh_token: refreshToken,
          });
          if (sessionError) throw sessionError;
          setStatus("success");
          setTimeout(() => router.push("/dashboard"), 800);
          return;
        }

        throw new Error("No auth code or tokens found in URL");
      } catch (err: any) {
        console.error("Auth callback error:", err);
        setError(err.message || "Failed to authenticate");
        setStatus("error");
      }
    };

    handleCallback();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-primary/5 p-4">
      <Card className="max-w-md w-full p-8 text-center">
        {status === "loading" && (
          <>
            <div className="flex justify-center mb-6">
              <Loader2 className="h-16 w-16 text-primary animate-spin" />
            </div>
            <h1 className="text-2xl font-bold mb-2">Signing you in...</h1>
            <p className="text-muted">Please wait a moment</p>
          </>
        )}

        {status === "success" && (
          <>
            <div className="flex justify-center mb-6">
              <div className="h-16 w-16 bg-green-500/10 rounded-full flex items-center justify-center">
                <CheckCircle2 className="h-8 w-8 text-green-500" />
              </div>
            </div>
            <h1 className="text-2xl font-bold mb-2">Success!</h1>
            <p className="text-muted">Redirecting to your dashboard...</p>
          </>
        )}

        {status === "error" && (
          <>
            <div className="flex justify-center mb-6">
              <div className="h-16 w-16 bg-destructive/10 rounded-full flex items-center justify-center">
                <XCircle className="h-8 w-8 text-destructive" />
              </div>
            </div>
            <h1 className="text-2xl font-bold mb-2">Authentication Failed</h1>
            <p className="text-muted mb-6">{error}</p>
            <Button onClick={() => router.push("/login")} className="w-full">
              Back to Login
            </Button>
          </>
        )}
      </Card>
    </div>
  );
}

