# CreatorPulse Backend

Python FastAPI backend for the CreatorPulse newsletter drafting assistant.

## Features

- 🚀 FastAPI for high-performance async API
- 📊 Supabase (PostgreSQL) for database
- 🤖 OpenAI GPT-4 for draft generation
- 📰 RSS feed parsing and aggregation
- 📧 Email delivery via SendGrid/Mailgun/SMTP
- 🔐 Encrypted ESP credential storage

## Prerequisites

- Python 3.11+
- Supabase account and project
- Openrouter API key (free tier available!)
- (Optional) SendGrid or Mailgun API key for email sending

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-role-key

OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key
OPENROUTER_MODEL=z-ai/glm-4.5-air:free

SECRET_KEY=your-secret-key-for-jwt
ENCRYPTION_KEY=your-32-byte-base64-key

CORS_ORIGINS=http://localhost:3000
FRONTEND_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
```

### 4. Set Up Supabase Database

Run the SQL schema in your Supabase project (see `schema.sql`).

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using the Python script:

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Supabase client
│   ├── models/              # Pydantic models
│   │   ├── user.py
│   │   ├── bundle.py
│   │   ├── draft.py
│   │   └── analytics.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── bundles.py       # Source bundles
│   │   ├── drafts.py        # Draft management
│   │   └── analytics.py     # Analytics
│   ├── services/            # Business logic
│   │   ├── rss_service.py   # RSS parsing
│   │   ├── ai_service.py    # OpenAI integration
│   │   ├── draft_generator.py  # Draft generation
│   │   └── email_service.py # Email sending
│   └── utils/               # Utilities
├── data/                    # Data files
├── prompts/                 # AI prompts
├── requirements.txt         # Dependencies
└── .env                     # Environment variables
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Bundles
- `GET /api/bundles/presets` - Get preset bundles
- `GET /api/bundles/` - Get all bundles
- `GET /api/bundles/{id}` - Get specific bundle

### Drafts
- `POST /api/drafts/generate` - Generate new draft
- `GET /api/drafts/` - Get user's drafts
- `GET /api/drafts/{id}` - Get specific draft
- `PATCH /api/drafts/{id}` - Update draft
- `POST /api/drafts/{id}/send` - Send draft
- `POST /api/drafts/{id}/regenerate` - Regenerate section
- `POST /api/drafts/{id}/reactions` - Save feedback

### Analytics
- `GET /api/analytics/` - Get analytics summary
- `GET /api/analytics/drafts/{id}` - Get draft analytics

## Testing

```bash
# Run tests (coming soon)
pytest
```

## Deployment

### Railway / Render

1. Connect your Git repository
2. Set environment variables in the dashboard
3. Deploy automatically on push

### DigitalOcean App Platform

1. Create new app from GitHub
2. Configure build and run commands
3. Set environment variables
4. Deploy

## Current Status

✅ Phase 2 Complete: Backend Foundation
- FastAPI application structure
- Supabase connection
- Pydantic models
- API routers
- RSS parsing service
- Openrouter API integration (free GLM-4.5-air model)
- Email service skeleton

🚧 Next Steps:
- Complete Supabase database schema
- Implement authentication
- Add background jobs for scheduled RSS fetching
- Implement ESP integration
- Connect frontend to backend

