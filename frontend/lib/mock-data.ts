import { Bundle, Draft, AnalyticsSummary, TonePreset } from "@/types";

export const mockBundles: Bundle[] = [
  {
    id: "preset-1",
    key: "ai-ml-trends",
    label: "AI & ML Trends",
    description: "The latest news, research, and breakthroughs in Artificial Intelligence and Machine Learning.",
    isPreset: true,
    sources: [
      "https://techcrunch.com/category/artificial-intelligence/feed/",
      "https://venturebeat.com/category/ai/feed/",
    ],
  },
  {
    id: "preset-2",
    key: "creator-economy",
    label: "Creator Economy",
    description: "Insights on the creator economy, monetization, and platform trends.",
    isPreset: true,
    sources: [
      "https://blog.creator-economy.com/feed/",
    ],
  },
  {
    id: "preset-3",
    key: "marketing-growth",
    label: "Marketing & Growth",
    description: "Growth hacking, marketing strategies, and conversion optimization.",
    isPreset: true,
    sources: [
      "https://growthhackers.com/feed",
    ],
  },
  {
    id: "preset-4",
    key: "startups-innovation",
    label: "Startups & Innovation",
    description: "Startup news, funding rounds, and innovation in tech.",
    isPreset: true,
    sources: [
      "https://techcrunch.com/category/startups/feed/",
    ],
  },
  {
    id: "preset-5",
    key: "cybersecurity-privacy",
    label: "Cybersecurity & Privacy",
    description: "Security vulnerabilities, privacy concerns, and data protection news.",
    isPreset: true,
    sources: [
      "https://feeds.feedburner.com/TheHackersNews",
    ],
  },
  {
    id: "preset-6",
    key: "productivity-workflow",
    label: "Productivity & Workflow Tools",
    description: "Tools and techniques to boost productivity and streamline workflows.",
    isPreset: true,
    sources: [],
  },
  {
    id: "preset-7",
    key: "sustainability-future-tech",
    label: "Sustainability & Future Tech",
    description: "Green technology, climate tech, and sustainable innovation.",
    isPreset: true,
    sources: [],
  },
  {
    id: "preset-8",
    key: "tech-policy-regulation",
    label: "Tech Policy & Regulation",
    description: "Regulatory changes, policy debates, and legal issues in tech.",
    isPreset: true,
    sources: [],
  },
  {
    id: "preset-9",
    key: "health-wellness-tech",
    label: "Health & Wellness Tech",
    description: "Digital health, wellness apps, and medical technology.",
    isPreset: true,
    sources: [],
  },
  {
    id: "preset-10",
    key: "mindset-creativity",
    label: "Mindset & Creativity",
    description: "Creative thinking, mental models, and personal development.",
    isPreset: true,
    sources: [],
  },
];

export const mockDrafts: Draft[] = [
  {
    id: "draft-1",
    userId: "user-1",
    bundleId: "preset-1",
    bundleName: "AI & ML Trends",
    topic: "AI content automation",
    tone: "professional",
    generatedHtml: `
      <div class="draft-intro">
        <h2>The AI Revolution in Content Creation</h2>
        <p>This week has seen remarkable advancements in AI-powered content automation, with several major players announcing new capabilities that promise to reshape how creators approach their work.</p>
      </div>
      <div class="draft-insight">
        <h3>OpenAI's Latest Model Shows Promise</h3>
        <p>OpenAI released updates to their GPT models this week, focusing on improved reasoning capabilities and reduced hallucination rates. Early tests show a 40% improvement in factual accuracy.</p>
      </div>
      <div class="draft-insight">
        <h3>Google Announces Gemini Pro 1.5</h3>
        <p>Google's new Gemini Pro 1.5 model features a massive 1M token context window, enabling unprecedented document analysis capabilities for content creators and researchers.</p>
      </div>
      <div class="draft-insight">
        <h3>Anthropic Focuses on Safety</h3>
        <p>Anthropic's Claude 3 update emphasizes constitutional AI principles, making it particularly suitable for enterprise content workflows where accuracy and safety are paramount.</p>
      </div>
      <div class="draft-trends">
        <h3>Trends to Watch</h3>
        <ul>
          <li>Multi-modal AI (text + image + video generation)</li>
          <li>Fine-tuning for niche industries</li>
          <li>AI-human collaboration workflows</li>
        </ul>
      </div>
    `,
    status: "draft",
    readinessScore: 85,
    sources: [
      "https://techcrunch.com/ai-news-1",
      "https://venturebeat.com/ai-news-2",
    ],
    createdAt: new Date("2025-10-16T08:00:00"),
    updatedAt: new Date("2025-10-16T08:00:00"),
  },
  {
    id: "draft-2",
    userId: "user-1",
    bundleId: "preset-2",
    bundleName: "Creator Economy",
    tone: "conversational",
    generatedHtml: `
      <div class="draft-intro">
        <h2>Creator Monetization Gets a Makeover</h2>
        <p>The creator economy is evolving fast. This week brought news of new platforms, tools, and strategies that creators are using to diversify their income streams.</p>
      </div>
      <div class="draft-insight">
        <h3>Patreon Introduces Tiered Perks</h3>
        <p>Patreon rolled out advanced tier customization, letting creators offer more nuanced membership levels. Early adopters report a 25% increase in conversions.</p>
      </div>
      <div class="draft-insight">
        <h3>TikTok Expands Creator Fund</h3>
        <p>TikTok announced a $1B expansion to its creator fund, focusing on educational and how-to content. The move signals a shift toward rewarding value-driven content.</p>
      </div>
      <div class="draft-trends">
        <h3>What's Next</h3>
        <ul>
          <li>Micro-subscriptions (pay-per-content models)</li>
          <li>Cross-platform creator tools</li>
          <li>Community-driven products</li>
        </ul>
      </div>
    `,
    status: "sent",
    readinessScore: 92,
    sources: [
      "https://creator-economy.com/news-1",
    ],
    createdAt: new Date("2025-10-15T08:00:00"),
    updatedAt: new Date("2025-10-15T09:30:00"),
    sentAt: new Date("2025-10-15T10:00:00"),
  },
  {
    id: "draft-3",
    userId: "user-1",
    bundleId: "preset-3",
    bundleName: "Marketing & Growth",
    tone: "analytical",
    generatedHtml: `
      <div class="draft-intro">
        <h2>Data-Driven Marketing in 2025</h2>
        <p>New analytics tools and privacy regulations are reshaping how marketers approach growth strategies.</p>
      </div>
      <div class="draft-insight">
        <h3>First-Party Data Takes Center Stage</h3>
        <p>With third-party cookies phasing out, marketers are investing heavily in first-party data strategies. Survey data shows 78% of companies plan to increase budgets in this area.</p>
      </div>
    `,
    status: "draft",
    readinessScore: 65,
    sources: [],
    createdAt: new Date("2025-10-14T08:00:00"),
    updatedAt: new Date("2025-10-14T08:00:00"),
  },
];

export const mockAnalytics: AnalyticsSummary = {
  openRate: 42.5,
  clickThroughRate: 8.3,
  avgReviewTime: 18.5,
  draftAcceptanceRate: 73.2,
  totalDrafts: 45,
  totalSent: 33,
};

export const tonePresets: TonePreset[] = [
  {
    value: "professional",
    label: "Professional",
    description: "Formal, authoritative, and business-oriented",
  },
  {
    value: "conversational",
    label: "Conversational",
    description: "Casual, friendly, and approachable",
  },
  {
    value: "analytical",
    label: "Analytical",
    description: "Data-driven, precise, and detailed",
  },
  {
    value: "friendly",
    label: "Friendly",
    description: "Warm, engaging, and personal",
  },
];

// Mock API functions
export async function getMockBundles(): Promise<Bundle[]> {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return mockBundles;
}

export async function getMockDrafts(): Promise<Draft[]> {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return mockDrafts;
}

export async function getMockDraft(id: string): Promise<Draft | null> {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return mockDrafts.find((d) => d.id === id) || null;
}

export async function getMockAnalytics(): Promise<AnalyticsSummary> {
  await new Promise((resolve) => setTimeout(resolve, 500));
  return mockAnalytics;
}

export async function generateMockDraft(
  bundleId: string,
  topic?: string,
  tone?: string
): Promise<Draft> {
  await new Promise((resolve) => setTimeout(resolve, 2000));
  
  const bundle = mockBundles.find((b) => b.id === bundleId);
  const newDraft: Draft = {
    id: `draft-${Date.now()}`,
    userId: "user-1",
    bundleId,
    bundleName: bundle?.label || "Unknown Bundle",
    topic,
    tone: (tone as Draft["tone"]) || "professional",
    generatedHtml: `
      <div class="draft-intro">
        <h2>Your Generated Newsletter</h2>
        <p>This is a mock generated draft based on ${bundle?.label}${topic ? ` focusing on ${topic}` : ""}.</p>
      </div>
      <div class="draft-insight">
        <h3>Key Insight #1</h3>
        <p>Here's an interesting development in this space...</p>
      </div>
      <div class="draft-insight">
        <h3>Key Insight #2</h3>
        <p>Another notable trend worth watching...</p>
      </div>
      <div class="draft-trends">
        <h3>Trends to Watch</h3>
        <ul>
          <li>Emerging pattern #1</li>
          <li>Emerging pattern #2</li>
          <li>Emerging pattern #3</li>
        </ul>
      </div>
    `,
    status: "draft",
    readinessScore: 80,
    sources: bundle?.sources || [],
    createdAt: new Date(),
    updatedAt: new Date(),
  };
  
  return newDraft;
}

