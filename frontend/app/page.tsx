import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Zap, Mail, TrendingUp, Clock } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="border-b border-border bg-surface/95 backdrop-blur">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-2 text-primary">
              <svg
                className="h-8 w-8"
                fill="currentColor"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M44 11.2727C44 14.0109 39.8386 16.3957 33.69 17.6364C39.8386 18.877 44 21.2618 44 24C44 26.7382 39.8386 29.123 33.69 30.3636C39.8386 31.6043 44 33.9891 44 36.7273C44 40.7439 35.0457 44 24 44C12.9543 44 4 40.7439 4 36.7273C4 33.9891 8.16144 31.6043 14.31 30.3636C8.16144 29.123 4 26.7382 4 24C4 21.2618 8.16144 18.877 14.31 17.6364C8.16144 16.3957 4 14.0109 4 11.2727C4 7.25611 12.9543 4 24 4C35.0457 4 44 7.25611 44 11.2727Z" />
              </svg>
              <span className="font-bold text-xl">CreatorPulse</span>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/dashboard">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link href="/dashboard">
                <Button size="sm">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="flex-1 flex items-center justify-center px-4 py-20 sm:py-32">
        <div className="container mx-auto max-w-6xl text-center">
          <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary mb-8">
            <Zap className="h-4 w-4" />
            AI-Powered Newsletter Assistant
          </div>
          
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6">
            From 3 Hours to 20 Minutes
            <br />
            <span className="text-primary">Transform Your Newsletter Workflow</span>
          </h1>
          
          <p className="text-lg sm:text-xl text-muted max-w-3xl mx-auto mb-10">
            CreatorPulse automatically aggregates insights from your trusted sources, 
            detects emerging trends, and generates voice-matched newsletter drafts—delivered 
            to your inbox every morning at 8 AM.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/dashboard">
              <Button size="lg" className="w-full sm:w-auto">
                Start Free Trial
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="w-full sm:w-auto">
              Watch Demo
            </Button>
          </div>

          {/* Feature Grid */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
            <FeatureCard
              icon={<Zap className="h-6 w-6 text-primary" />}
              title="AI Draft Generation"
              description="Generate ready-to-edit newsletter drafts in your unique voice"
            />
            <FeatureCard
              icon={<TrendingUp className="h-6 w-6 text-primary" />}
              title="Trend Detection"
              description="Automatically spot emerging topics and conversations"
            />
            <FeatureCard
              icon={<Mail className="h-6 w-6 text-primary" />}
              title="Daily Delivery"
              description="Wake up to a curated draft in your inbox every morning"
            />
            <FeatureCard
              icon={<Clock className="h-6 w-6 text-primary" />}
              title="Save Time"
              description="Reduce newsletter creation from hours to under 20 minutes"
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-sm text-muted">
              © 2025 CreatorPulse. All rights reserved.
            </p>
            <div className="flex items-center gap-6">
              <Link href="#" className="text-sm text-muted hover:text-primary transition-colors">
                Privacy
              </Link>
              <Link href="#" className="text-sm text-muted hover:text-primary transition-colors">
                Terms
              </Link>
              <Link href="#" className="text-sm text-muted hover:text-primary transition-colors">
                Contact
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-xl bg-surface border border-border p-6 text-left hover:border-primary/50 transition-colors">
      <div className="mb-4">{icon}</div>
      <h3 className="font-semibold mb-2">{title}</h3>
      <p className="text-sm text-muted">{description}</p>
    </div>
  );
}
