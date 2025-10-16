# CreatorPulse

**AI-Powered Newsletter Drafting Assistant**

CreatorPulse automatically aggregates insights from trusted sources, detects emerging trends, and generates voice-matched newsletter drafts—reducing creation time from 2-3 hours to under 20 minutes.

## 🎯 Overview

CreatorPulse is designed for newsletter writers, content curators, and agency professionals who want to:
- Aggregate insights from RSS feeds (Twitter, YouTube, and more coming soon)
- Detect emerging trends automatically
- Generate ready-to-edit newsletter drafts in their unique voice
- Send newsletters via their existing ESP (SendGrid, Mailgun, SMTP)
- Track open rates, CTR, and engagement metrics

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** (for frontend)
- **Python 3.11+** (for backend)
- **Supabase account** (free tier works)
- **Openrouter API key** (free tier available!)

### 1. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

See [frontend/README.md](frontend/README.md) for details.

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your credentials
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

API docs: `http://localhost:8000/docs`

See [backend/README.md](backend/README.md) for details.

### 3. Database Setup

1. Create a free Supabase project at [supabase.com](https://supabase.com)
2. Run the SQL schema from `backend/schema.sql` in the Supabase SQL Editor
3. Copy your Supabase URL and keys to `backend/.env`

## 📁 Project Structure

```
CreatorPulse/
├── frontend/                 # Next.js 15 + React + TypeScript
│   ├── app/                 # Next.js App Router pages
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utilities and mock data
│   └── types/               # TypeScript definitions
│
├── backend/                  # Python FastAPI
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Business logic (RSS, AI, Email)
│   │   ├── models/         # Pydantic models
│   │   └── main.py         # FastAPI app
│   ├── schema.sql          # Database schema
│   └── requirements.txt    # Python dependencies
│
├── Frontend_wireframes/      # Original design wireframes
├── CreatorPulse_Masterplan.md
└── CreatorPulse_Updated_Frontend_Spec_MVP.md
```

## ✨ Features

### Current (MVP)
- ✅ Complete responsive UI with dark mode
- ✅ Dashboard for managing drafts
- ✅ Create page with preset bundles
- ✅ WYSIWYG editor for draft editing
- ✅ Analytics dashboard with KPIs
- ✅ Settings page (ESP, tone, preferences)
- ✅ FastAPI backend with async endpoints
- ✅ RSS feed parsing and aggregation
- ✅ OpenAI GPT-4 draft generation
- ✅ Supabase database integration ready
- ✅ Email service framework

### Coming Soon
- 🚧 Authentication (Supabase Auth)
- 🚧 Real-time autosave
- 🚧 Scheduled draft delivery (8 AM daily)
- 🚧 Custom bundle creation
- 🚧 Voice training from writing samples
- 🚧 Background RSS crawler jobs
- 🚧 Advanced analytics and charts
- 🚧 Multi-recipient lists

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS v4
- **Icons**: Lucide React
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI**: Openrouter API (GLM-4.5-air free model)
- **RSS**: feedparser
- **Email**: SendGrid/Mailgun/SMTP
- **Deployment**: Railway/Render

## 📊 Database Schema

- **users** - User profiles and preferences
- **bundles** - Content source bundles (preset + custom)
- **sources** - RSS feed URLs and metadata
- **drafts** - Generated newsletter drafts
- **feedback** - User reactions and edits for learning
- **analytics** - Open rates, CTR, performance metrics
- **esp_credentials** - Encrypted email provider credentials

See `backend/schema.sql` for complete schema.

## 🔐 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
OPENROUTER_API_KEY=sk-or-v1-your-key
OPENROUTER_MODEL=z-ai/glm-4.5-air:free
SECRET_KEY=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key
CORS_ORIGINS=http://localhost:3000
```

## 🎨 Design System

- **Primary Color**: #13a4ec (Blue)
- **Font**: Manrope (Google Fonts)
- **Dark Mode**: Full support
- **Responsive**: Mobile-first design

## 📖 API Documentation

When the backend is running, visit:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

Key endpoints:
- `POST /api/drafts/generate` - Generate newsletter draft
- `GET /api/bundles/presets` - Get preset bundles
- `GET /api/drafts/` - List user drafts
- `POST /api/drafts/{id}/send` - Send newsletter
- `GET /api/analytics/` - Get analytics summary

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest
```

## 🚀 Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables
3. Deploy automatically on push to main

### Backend (Railway)
1. Connect your GitHub repository to Railway
2. Set environment variables
3. Deploy automatically on push to main

### Database (Supabase)
Already hosted—no deployment needed!

## 📝 Development Roadmap

- [x] **Phase 1**: Frontend with mock data
- [x] **Phase 2**: Backend foundation
- [ ] **Phase 3**: RSS integration (in progress)
- [ ] **Phase 4**: AI draft generation
- [ ] **Phase 5**: Email delivery
- [ ] **Phase 6**: Frontend-backend connection
- [ ] **Phase 7**: Analytics implementation
- [ ] **Phase 8**: Testing & deployment

## 🤝 Contributing

This is a private project currently in MVP development.

## 📄 License

Proprietary - All rights reserved

## 🐛 Known Issues

- Authentication is currently stubbed (needs Supabase Auth implementation)
- Email sending is simulated (needs ESP integration)
- Background RSS crawler not yet implemented
- Voice training feature pending

## 📧 Support

For questions or issues, contact: jayanth@example.com

---

**Status**: 🚧 MVP Development in Progress

Built with ❤️ using Next.js, FastAPI, and Supabase

