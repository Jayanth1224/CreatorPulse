"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Navigation } from "@/components/layout/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { generateDraft } from "@/lib/api-client";
import { tonePresets } from "@/lib/mock-data";
import { Loader2, Sparkles } from "lucide-react";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { useBundles } from "@/contexts/BundlesContext";
import { VoiceTrainingStatus } from "@/components/VoiceTrainingStatus";

export default function CreatePage() {
  return (
    <ProtectedRoute>
      <CreateContent />
    </ProtectedRoute>
  );
}

function CreateContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { bundles, loading: bundlesLoading, error: bundlesError } = useBundles();
  const [selectedBundle, setSelectedBundle] = useState("");
  const [topic, setTopic] = useState("");
  const [tone, setTone] = useState("professional");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedBundle) {
      setError("Please select a bundle");
      return;
    }

    setError("");
    setIsGenerating(true);

    const response = await generateDraft(selectedBundle, topic || undefined, tone);

    if (response.error) {
      setError(response.error.detail);
      setIsGenerating(false);
      return;
    }

    if (response.data) {
      // Redirect to editor
      router.push(`/create/${response.data.id}`);
    } else {
      setError("Failed to generate draft. Please try again.");
      setIsGenerating(false);
    }
  };

  // Handle bundle parameter from URL
  useEffect(() => {
    const bundleParam = searchParams.get('bundle');
    if (bundleParam && bundles.length > 0) {
      setSelectedBundle(bundleParam);
    }
  }, [searchParams, bundles]);

  const selectedBundleData = bundles.find((b) => b.id === selectedBundle);

  return (
    <>
      <Navigation />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="w-full max-w-2xl">
          <Card className="p-8 sm:p-10">
            <CardHeader className="text-center p-0 mb-8">
              <CardTitle className="text-3xl font-extrabold mb-2">
                Generate a New Draft
              </CardTitle>
              <CardDescription className="text-base max-w-lg mx-auto">
                Pick a bundle, add a focus if you like, and we'll prepare a
                ready-to-edit newsletter draft in your voice.
              </CardDescription>
            </CardHeader>

            <CardContent className="p-0">
              <form onSubmit={handleGenerate} className="space-y-6">
                {/* Bundle Selector */}
                <div>
                  <Label htmlFor="bundle" className="text-base">
                    Select Source Bundle <span className="text-red-500">*</span>
                  </Label>
                  <Select
                    id="bundle"
                    value={selectedBundle}
                    onChange={(e) => setSelectedBundle(e.target.value)}
                    className="mt-2"
                    disabled={bundlesLoading}
                  >
                    <option value="">
                      {bundlesLoading ? "Loading bundles..." : "Choose a bundle..."}
                    </option>
                    <optgroup label="✨ Preset Bundles">
                      {bundles
                        .filter((b) => b.isPreset)
                        .map((bundle) => (
                          <option key={bundle.id} value={bundle.id}>
                            {bundle.label}
                          </option>
                        ))}
                    </optgroup>
                    <optgroup label="📦 Your Custom Bundles">
                      {bundles
                        .filter((b) => !b.isPreset)
                        .map((bundle) => (
                          <option key={bundle.id} value={bundle.id}>
                            {bundle.label}
                          </option>
                        ))}
                    </optgroup>
                  </Select>
                  {selectedBundleData && (
                    <p className="mt-2 text-xs text-muted">
                      {selectedBundleData.description}
                    </p>
                  )}
                </div>

                {/* Topic/Focus */}
                <div>
                  <Label htmlFor="topic" className="text-base">
                    What's today's focus?{" "}
                    <span className="text-muted font-normal">(Optional)</span>
                  </Label>
                  <Input
                    id="topic"
                    type="text"
                    placeholder="e.g., AI content automation or Web3 community growth"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    className="mt-2"
                  />
                  <p className="mt-2 text-xs text-muted">
                    We'll bias your draft around this topic.
                  </p>
                </div>

                {/* Tone Preset */}
                <div>
                  <Label htmlFor="tone" className="text-base">
                    Tone{" "}
                    <span className="text-muted font-normal">(Optional)</span>
                  </Label>
                  <Select
                    id="tone"
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                    className="mt-2"
                  >
                    {tonePresets.map((preset) => (
                      <option key={preset.value} value={preset.value}>
                        {preset.label}
                      </option>
                    ))}
                  </Select>
                  <p className="mt-2 text-xs text-muted">
                    {tonePresets.find((p) => p.value === tone)?.description}
                  </p>
                </div>

                {/* Error Message */}
                {error && (
                  <div className="bg-red-100 dark:bg-red-900/20 border border-red-400 dark:border-red-600 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg">
                    <strong className="font-bold">Error: </strong>
                    <span>{error}</span>
                  </div>
                )}

                {/* Generate Button */}
                <div>
                  <Button
                    type="submit"
                    className="w-full"
                    size="lg"
                    disabled={isGenerating || !selectedBundle}
                  >
                    {isGenerating ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        Generating your draft...
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-5 w-5" />
                        Generate Draft
                      </>
                    )}
                  </Button>
                  <p className="text-xs text-center text-muted mt-4">
                    {isGenerating ? (
                      <>⏱️ Parsing RSS feeds and generating with AI... This may take 20-30 seconds.</>
                    ) : (
                      <>💡 We'll analyze the latest posts from your selected bundle and prepare a newsletter draft in your voice.</>
                    )}
                  </p>
                </div>

                {/* Voice Training Status */}
                <VoiceTrainingStatus 
                  tone={tone}
                  className="mt-4"
                />
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </>
  );
}

