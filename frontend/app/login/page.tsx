"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Mail, Sparkles, CheckCircle2, Loader2 } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { signInWithMagicLink } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await signInWithMagicLink(email);

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      setSent(true);
      setLoading(false);
    }
  };

  if (sent) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-primary/5 p-4">
        <Card className="max-w-md w-full p-8 text-center">
          <div className="flex justify-center mb-6">
            <div className="h-16 w-16 bg-green-500/10 rounded-full flex items-center justify-center">
              <CheckCircle2 className="h-8 w-8 text-green-500" />
            </div>
          </div>
          <h1 className="text-2xl font-bold mb-2">Check Your Email!</h1>
          <p className="text-muted mb-6">
            We've sent a magic link to <strong>{email}</strong>
          </p>
          <p className="text-sm text-muted mb-6">
            Click the link in the email to sign in. The link will expire in 1 hour.
          </p>
          <Button
            variant="outline"
            onClick={() => {
              setSent(false);
              setEmail("");
            }}
            className="w-full"
          >
            Send Another Link
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-primary/5 p-4">
      <Card className="max-w-md w-full p-8">
        <div className="flex items-center justify-center mb-6">
          <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center">
            <Sparkles className="h-6 w-6 text-primary" />
          </div>
        </div>
        
        <h1 className="text-3xl font-bold text-center mb-2">Welcome to CreatorPulse</h1>
        <p className="text-center text-muted mb-8">
          Sign in with a magic link sent to your email
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted" />
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="pl-10"
                disabled={loading}
              />
            </div>
          </div>

          {error && (
            <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-3">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Sending Magic Link...
              </>
            ) : (
              <>
                <Mail className="h-4 w-4 mr-2" />
                Send Magic Link
              </>
            )}
          </Button>
        </form>

        <div className="mt-6 pt-6 border-t border-border">
          <p className="text-xs text-center text-muted">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>

        <div className="mt-6 bg-primary/5 border border-primary/20 rounded-lg p-4">
          <h3 className="font-semibold text-sm mb-2">✨ How it works</h3>
          <ol className="text-xs text-muted space-y-1">
            <li>1. Enter your email address</li>
            <li>2. Check your inbox for a magic link</li>
            <li>3. Click the link to sign in instantly</li>
            <li>4. No password needed!</li>
          </ol>
        </div>
      </Card>
    </div>
  );
}

