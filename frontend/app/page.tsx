import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Check } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-gray-200/50 dark:border-gray-700/50 bg-background/80 backdrop-blur-sm">
        <div className="container mx-auto flex items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 text-primary">
              <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <path d="M44 11.2727C44 14.0109 39.8386 16.3957 33.69 17.6364C39.8386 18.877 44 21.2618 44 24C44 26.7382 39.8386 29.123 33.69 30.3636C39.8386 31.6043 44 33.9891 44 36.7273C44 40.7439 35.0457 44 24 44C12.9543 44 4 40.7439 4 36.7273C4 33.9891 8.16144 31.6043 14.31 30.3636C8.16144 29.123 4 26.7382 4 24C4 21.2618 8.16144 18.877 14.31 17.6364C8.16144 16.3957 4 14.0109 4 11.2727C4 7.25611 12.9543 4 24 4C35.0457 4 44 7.25611 44 11.2727Z" fill="currentColor"></path>
              </svg>
            </div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">CreatorPulse</h2>
          </div>
          <nav className="hidden items-center gap-8 md:flex">
            <a className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary" href="#features">Features</a>
            <a className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary" href="#pricing">Pricing</a>
            <a className="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary" href="#demo">Demo</a>
          </nav>
          <div className="flex items-center gap-2">
            <Link href="/login">
              <Button variant="ghost" size="sm" className="hidden sm:block">
                Log In
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="sm">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-grow">
        {/* Hero Section */}
        <section className="py-20 text-center sm:py-24 lg:py-32">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-4xl font-extrabold tracking-tighter text-gray-900 dark:text-white sm:text-5xl md:text-6xl">
              CreatorPulse — Daily research, one ready-to-send newsletter.
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
              Aggregate trusted sources, surface trends, and get a voice-matched draft every morning at 08:00.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Link href="/dashboard">
                <Button size="lg" className="shadow-lg transition-transform hover:scale-105">
                  Get Started — Free
                </Button>
              </Link>
              <Button size="lg" variant="outline" className="shadow-lg transition-transform hover:scale-105">
                View Demo
              </Button>
            </div>
            <div className="mt-8">
              <p className="text-sm text-gray-500 dark:text-gray-400">Used by independent creators & agencies</p>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">14-day free — no credit card required.</p>
            </div>
          </div>
        </section>

        {/* How it works Section */}
        <section className="py-16 sm:py-20 lg:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">How it works</h2>
            </div>
            <div className="relative mt-12">
              <div aria-hidden="true" className="absolute left-1/2 top-4 -ml-px h-full w-0.5 bg-gray-200 dark:bg-gray-700"></div>
              <div className="relative flex flex-col items-center gap-12">
                <div className="flex w-full items-start gap-8">
                  <div className="relative z-10 flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-primary text-white">
                    <span className="text-xl font-bold">1</span>
                  </div>
                  <div className="pt-2">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Pick a bundle</h3>
                    <p className="mt-1 text-base text-gray-600 dark:text-gray-300">Choose from curated source bundles or create your own.</p>
                  </div>
                </div>
                <div className="flex w-full items-start gap-8">
                  <div className="relative z-10 flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-primary text-white">
                    <span className="text-xl font-bold">2</span>
                  </div>
                  <div className="pt-2">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Receive daily digest at 08:00</h3>
                    <p className="mt-1 text-base text-gray-600 dark:text-gray-300">Get a voice-matched draft summarizing the latest trends.</p>
                  </div>
                </div>
                <div className="flex w-full items-start gap-8">
                  <div className="relative z-10 flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-primary text-white">
                    <span className="text-xl font-bold">3</span>
                  </div>
                  <div className="pt-2">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Edit & send in &lt; 20 min</h3>
                    <p className="mt-1 text-base text-gray-600 dark:text-gray-300">Review, polish, and send your newsletter to your audience.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-16 sm:py-20 lg:py-24 bg-background">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">All-in-one Platform for Creators</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Everything you need to research, write, and grow your newsletter.</p>
            </div>
            <div className="mt-16 grid gap-12 md:grid-cols-2 lg:grid-cols-3">
              <div className="flex flex-col gap-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-surface p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Voice-matched drafts</h3>
                <p className="text-gray-600 dark:text-gray-300">CreatorPulse generates drafts that match your unique voice, saving you time and ensuring consistency.</p>
              </div>
              <div className="flex flex-col gap-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-surface p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Source bundle & citations</h3>
                <p className="text-gray-600 dark:text-gray-300">Get a curated bundle of sources and citations to back up your newsletter content.</p>
              </div>
              <div className="flex flex-col gap-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-surface p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">ESP send & analytics</h3>
                <p className="text-gray-600 dark:text-gray-300">Send your newsletter directly from CreatorPulse and track your performance with built-in analytics.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section id="pricing" className="py-16 sm:py-20 lg:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">Pricing Plans</h2>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">Start for free, and scale as you grow. No credit card required.</p>
            </div>
            <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
              <div className="flex flex-col rounded-xl border border-gray-200 dark:border-gray-700 bg-surface p-8 shadow-lg">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Free</h3>
                <p className="mt-4 flex items-baseline gap-1">
                  <span className="text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white">$0</span>
                  <span className="text-sm font-semibold text-gray-500 dark:text-gray-400">/month</span>
                </p>
                <Button className="mt-6 w-full" variant="outline">
                  Get Started
                </Button>
                <ul className="mt-8 space-y-4 text-sm text-gray-600 dark:text-gray-300">
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    1 newsletter/month
                  </li>
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    Basic features
                  </li>
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    Community support
                  </li>
                </ul>
              </div>
              <div className="flex flex-col rounded-xl border-2 border-primary bg-surface p-8 shadow-2xl relative">
                <div className="absolute top-0 right-8 -mt-3">
                  <span className="rounded-full bg-primary px-3 py-1 text-xs font-semibold uppercase tracking-wider text-white">Most Popular</span>
                </div>
                <h3 className="text-lg font-semibold text-primary">Pro</h3>
                <p className="mt-4 flex items-baseline gap-1">
                  <span className="text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white">$49</span>
                  <span className="text-sm font-semibold text-gray-500 dark:text-gray-400">/month</span>
                </p>
                <Button className="mt-6 w-full">
                  Get Started
                </Button>
                <ul className="mt-8 space-y-4 text-sm text-gray-600 dark:text-gray-300">
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    Unlimited newsletters
                  </li>
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    Advanced features
                  </li>
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    Priority support
                  </li>
                </ul>
              </div>
              <div className="flex flex-col rounded-xl border border-gray-200 dark:border-gray-700 bg-surface p-8 shadow-lg">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Agency</h3>
                <p className="mt-4 flex items-baseline gap-1">
                  <span className="text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white">$199</span>
                  <span className="text-sm font-semibold text-gray-500 dark:text-gray-400">/month</span>
                </p>
                <Button className="mt-6 w-full" variant="outline">
                  Get Started
                </Button>
                <ul className="mt-8 space-y-4 text-sm text-gray-600 dark:text-gray-300">
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    Unlimited newsletters
                  </li>
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    All features
                  </li>
                  <li className="flex items-center gap-3">
                    <Check className="h-5 w-5 flex-shrink-0 text-primary" />
                    Dedicated account manager
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-background border-t border-gray-200 dark:border-gray-700">
        <div className="container mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
            <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 md:justify-start">
              <Link href="#" className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary">Docs</Link>
              <Link href="#" className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary">Privacy</Link>
              <Link href="#" className="text-sm text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary">Contact</Link>
            </div>
            <div className="flex justify-center space-x-6">
              <a className="text-gray-500 hover:text-primary dark:text-gray-400 dark:hover:text-primary" href="#">
                <span className="sr-only">Twitter</span>
                <svg aria-hidden="true" className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.71v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
                </svg>
              </a>
              <a className="text-gray-500 hover:text-primary dark:text-gray-400 dark:hover:text-primary" href="#">
                <span className="sr-only">LinkedIn</span>
                <svg aria-hidden="true" className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path clipRule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" fillRule="evenodd"></path>
                </svg>
              </a>
            </div>
          </div>
          <p className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">© 2023 CreatorPulse. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

