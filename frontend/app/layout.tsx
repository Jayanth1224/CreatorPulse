import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import "./globals.css";
import { Navigation } from "@/components/layout/navigation";

const manrope = Manrope({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
});

export const metadata: Metadata = {
  title: "CreatorPulse - AI-Powered Newsletter Drafting Assistant",
  description: "Reduce newsletter creation time from hours to minutes with AI-powered content curation and drafting.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={manrope.variable}>
      <body 
        className="min-h-screen bg-background text-foreground antialiased"
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
