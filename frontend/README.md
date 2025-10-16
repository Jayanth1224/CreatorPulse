# CreatorPulse Frontend

AI-powered newsletter drafting assistant built with Next.js 15, React, TypeScript, and TailwindCSS v4.

## Features

- 🎨 Modern UI with TailwindCSS v4 and custom design tokens
- 📱 Fully responsive design with mobile navigation
- 🌙 Dark mode support
- ⚡ Built with Next.js 15 App Router
- 🔤 TypeScript for type safety
- 📦 Mock data for development

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

### Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Landing page
│   ├── dashboard/         # Dashboard/Inbox
│   ├── create/            # Create & Editor pages
│   ├── analytics/         # Analytics dashboard
│   └── settings/          # Settings page
├── components/
│   ├── ui/                # Reusable UI components
│   └── layout/            # Layout components (Navigation)
├── lib/
│   ├── utils.ts           # Utility functions
│   └── mock-data.ts       # Mock data for development
└── types/
    └── index.ts           # TypeScript type definitions
```

## Pages

- `/` - Landing page
- `/dashboard` - Draft management and inbox
- `/create` - Generate new draft form
- `/create/[draftId]` - Draft editor
- `/analytics` - Performance analytics
- `/settings` - User settings and preferences

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS v4
- **Icons**: Lucide React
- **Fonts**: Manrope (Google Fonts)

## Current Status

✅ Phase 1 Complete: Frontend with Mock Data
- All pages implemented and functional
- Mock data for testing
- Responsive design
- Dark mode support

🚧 Next: Backend Integration (Python FastAPI + Supabase)
