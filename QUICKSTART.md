# CreatorPulse - Quick Start Guide

Get CreatorPulse running locally in 10 minutes!

## ⚡ Quick Setup

### 1. Frontend (2 minutes)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend runs at `http://localhost:3000`

The frontend works standalone with mock data—you can browse all pages immediately!

### 2. Backend (5 minutes)

#### Install Python Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Create Environment File

Create `backend/.env`:

```env
SUPABASE_URL=https://placeholder.supabase.co
SUPABASE_KEY=placeholder-key
SUPABASE_SERVICE_KEY=placeholder-service-key
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here
OPENROUTER_MODEL=z-ai/glm-4.5-air:free
SECRET_KEY=your-random-secret-key
ENCRYPTION_KEY=your-32-byte-base64-key
CORS_ORIGINS=http://localhost:3000
```

> **Note**: For testing without Supabase, use placeholder values. Openrouter API key is required for draft generation.

#### Start Backend

```bash
# From backend/ directory
uvicorn app.main:app --reload
```

✅ Backend runs at `http://localhost:8000`
✅ API docs at `http://localhost:8000/docs`

### 3. Supabase Setup (Optional - 3 minutes)

If you want to use real database:

1. Go to [supabase.com](https://supabase.com) and create a free project
2. Copy the SQL from `backend/schema.sql`
3. Paste into Supabase SQL Editor and run
4. Copy your project URL and keys to `.env`

## 🎯 What You Can Do Now

### Without Backend
- ✅ Browse all pages
- ✅ View mock drafts
- ✅ Edit mock content
- ✅ See mock analytics
- ✅ Change settings

### With Backend (No Database)
- ✅ All of the above
- ✅ Test API endpoints via `/docs`
- ✅ Generate drafts (RSS + Openrouter AI)
  - Needs Openrouter API key
  - Won't persist to database

### With Backend + Supabase
- ✅ Full functionality
- ✅ Real data persistence
- ✅ User authentication (when implemented)
- ✅ Analytics tracking

## 🧪 Test the System

### 1. Test Frontend
Open browser: `http://localhost:3000`

- Landing page should load
- Click "Get Started" → Dashboard
- Click "Create" → See bundle selector
- Select "AI & ML Trends" → Generate Draft (mock)
- Draft opens in editor

### 2. Test Backend API
Open browser: `http://localhost:8000/docs`

Try these endpoints:
1. `GET /` - Health check
2. `GET /api/bundles/presets` - See all bundles
3. `POST /api/drafts/generate` - Generate a draft
   ```json
   {
     "bundle_id": "preset-1",
     "topic": "AI automation",
     "tone": "professional"
   }
   ```

### 3. Test RSS Parsing
Run from Python shell:

```python
from app.services.rss_service import RSSService

rss = RSSService()
entries = rss.parse_feed("https://techcrunch.com/category/artificial-intelligence/feed/")
print(f"Found {len(entries)} articles")
for e in entries[:3]:
    print(f"- {e['title']}")
```

### 4. Test AI Generation (requires OpenAI key)
```python
from app.services.ai_service import AIService
import asyncio

ai = AIService()
entries = [{"title": "AI Test", "summary": "Test summary", "link": "http://test.com"}]
draft = asyncio.run(ai.generate_newsletter_draft(entries, "professional"))
print(draft)
```

## 📁 Project Overview

### Frontend Structure
```
frontend/
├── app/page.tsx          → Landing page
├── app/dashboard/        → Inbox
├── app/create/           → Create & Editor
├── app/analytics/        → Analytics
├── app/settings/         → Settings
├── components/ui/        → Reusable components
└── lib/mock-data.ts      → Mock data (working now!)
```

### Backend Structure
```
backend/
├── app/main.py           → FastAPI app
├── app/routers/          → API endpoints
├── app/services/         → Business logic
│   ├── rss_service.py    → RSS parsing
│   ├── ai_service.py     → OpenAI integration
│   └── draft_generator.py → Orchestration
└── schema.sql            → Database schema
```

## 🔑 Required API Keys

### Must Have
- **Openrouter API Key**: For draft generation
  - Get at: https://openrouter.ai/keys
  - Cost: **FREE** with z-ai/glm-4.5-air:free model!

### Nice to Have
- **Supabase**: Free tier available
  - Get at: https://supabase.com
  - For: Database + Auth

- **SendGrid/Mailgun**: Free tiers available
  - For: Email sending (can simulate for now)

## 🐛 Troubleshooting

### Frontend Won't Start
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run dev
```

### Backend Won't Start

**"Module not found"**
```bash
# Make sure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

**"Config error"**
- Check `.env` file exists in `backend/` directory
- All variables should have values (can be placeholders)

### Draft Generation Fails

**"Openrouter API error"**
- Check your Openrouter API key in `.env`
- Ensure the key is valid (free tier works!)

**"RSS parsing failed"**
- Some feeds may be down/blocked
- Try a different bundle

## 🎉 Success Indicators

You'll know everything is working when:

✅ Frontend loads at localhost:3000
✅ You can navigate between pages
✅ Backend shows "ok" at localhost:8000
✅ API docs load at localhost:8000/docs
✅ `/api/bundles/presets` returns 10 bundles
✅ `/api/drafts/generate` creates a draft (with Openrouter key)

## 📞 Next Steps

Once you have everything running:

1. **Read** `PROJECT_STATUS.md` for detailed status
2. **Explore** the API docs at `/docs`
3. **Test** draft generation with your OpenAI key
4. **Set up** Supabase for persistence
5. **Connect** frontend to backend (Phase 6)

## 💡 Pro Tips

- Frontend works great without backend—develop UI first
- Test API endpoints in `/docs` before frontend integration
- Use mock data in frontend to speed up development
- RSS parsing works without database
- AI generation only needs OpenAI key
- Supabase can be added anytime

---

**🚀 Happy Building!**

Need help? Check `README.md` for detailed docs or `PROJECT_STATUS.md` for implementation status.

