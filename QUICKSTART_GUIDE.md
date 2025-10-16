# 🚀 CreatorPulse - Quick Start Guide

Get your CreatorPulse MVP up and running in 5 minutes!

---

## ✅ Prerequisites

- ✅ Python 3.13 (backend)
- ✅ Node.js 18+ (frontend)
- ✅ Supabase account (database already set up!)

---

## 📝 Step 1: Configure Environment Variables

### Backend `.env`

Create `/Users/jayanthbandi/CreatorPulse/backend/.env`:

```env
# Supabase (REQUIRED)
SUPABASE_URL=https://vnohbotdrcrrxdiqakoj.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_key_here

# OpenRouter (REQUIRED for AI generation)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=z-ai/glm-4.5-air:free

# Security (REQUIRED)
SECRET_KEY=your-secret-key-minimum-32-characters
ENCRYPTION_KEY=your-encryption-key-minimum-32-characters

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
CORS_ORIGINS=http://localhost:3000

# Email (OPTIONAL - will simulate if not provided)
SENDGRID_API_KEY=
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
FROM_EMAIL=noreply@creatorpulse.com
FROM_NAME=CreatorPulse

# LinkedIn (OPTIONAL)
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
```

### Frontend `.env.local`

Create `/Users/jayanthbandi/CreatorPulse/frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎯 Step 2: Start the Backend

```bash
cd /Users/jayanthbandi/CreatorPulse/backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --reload
```

✅ **Backend running at**: http://localhost:8000  
📚 **API Docs**: http://localhost:8000/docs

---

## 🎨 Step 3: Start the Frontend

Open a **new terminal**:

```bash
cd /Users/jayanthbandi/CreatorPulse/frontend

# Install dependencies (if not done)
npm install

# Start the dev server
npm run dev
```

✅ **Frontend running at**: http://localhost:3000

---

## 🎉 Step 4: Use the App!

### Create Your First Draft

1. Visit http://localhost:3000
2. Click **"Create New Draft"**
3. Select a bundle (e.g., "AI & ML Trends")
4. Optionally add a topic
5. Click **"Generate Draft"**
6. Wait ~10-30 seconds for AI generation
7. Edit in the WYSIWYG editor
8. Autosave happens automatically!

### Send via Email

1. Open a draft
2. Add recipient email(s) (comma-separated)
3. Click **"Send"**
4. Check console for send status

### Post to LinkedIn

1. First, set up LinkedIn OAuth credentials
2. Connect your LinkedIn account
3. Open a draft
4. Click **"Post to LinkedIn"**

### View Analytics

1. Navigate to **Analytics** page
2. See open rates, click rates, etc.
3. View per-draft analytics

---

## 🔧 Troubleshooting

### Backend won't start

**Issue**: `ModuleNotFoundError`
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: `Database connection error`
- Check SUPABASE_URL and keys in `.env`
- Make sure Supabase project is active

### Frontend won't start

**Issue**: `Module not found`
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue**: `API requests failing`
- Make sure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in `.env.local`

### Draft generation fails

**Issue**: `Failed to generate draft`
- Check OPENROUTER_API_KEY in backend `.env`
- Make sure you have API credits
- Check backend logs for detailed error

### Email sending simulation

**Issue**: Emails are simulated (not actually sent)
- Add SENDGRID_API_KEY or SMTP credentials to `.env`
- Restart backend after adding credentials

---

## 📊 Database Management

Your Supabase database is already set up with:
- ✅ 8 tables
- ✅ Row Level Security policies
- ✅ 10 preset bundles
- ✅ Indexes for performance

To view/manage:
1. Go to https://app.supabase.com
2. Select project: **CreatorPulse** (vnohbotdrcrrxdiqakoj)
3. Navigate to Table Editor or SQL Editor

---

## 🌐 API Endpoints

Full API documentation available at: http://localhost:8000/docs

### Key Endpoints

```
# Authentication
POST   /api/auth/signup
POST   /api/auth/login
GET    /api/auth/me

# Drafts
POST   /api/drafts/generate
GET    /api/drafts/
GET    /api/drafts/{id}
PATCH  /api/drafts/{id}
POST   /api/drafts/{id}/send

# LinkedIn
GET    /api/linkedin/auth/url
POST   /api/linkedin/post
GET    /api/linkedin/status

# Analytics
GET    /api/analytics/
GET    /api/analytics/drafts/{id}
```

---

## 🎯 What Works Right Now

### ✅ Fully Functional
- AI-powered draft generation
- Real-time autosave (2-second debounce)
- Email sending (simulated or real)
- LinkedIn posting (with OAuth)
- Analytics tracking
- Background RSS crawler (every 6 hours)

### 🔧 Needs Configuration
- Email sending (add ESP credentials)
- LinkedIn posting (add OAuth app)

### 🚀 Coming Soon
- Scheduled sends
- Custom bundles
- Voice training
- Advanced analytics

---

## 💡 Tips

### For Developers

1. **Backend logs**: Watch terminal for detailed error messages
2. **Frontend dev tools**: Open browser console for API call logs
3. **Database queries**: Use Supabase dashboard SQL editor
4. **API testing**: Use the interactive docs at `/docs`

### For Testing

1. **Mock data**: Frontend has fallback mocks if backend is down
2. **Test emails**: Use a test email service like Mailtrap
3. **LinkedIn**: Test with LinkedIn sandbox app
4. **Analytics**: Generate sample data by sending drafts

---

## 📚 More Documentation

- **Full Implementation**: See `IMPLEMENTATION_COMPLETE.md`
- **Project Status**: See `PROJECT_STATUS.md`
- **Master Plan**: See `CreatorPulse_Masterplan.md`

---

## 🆘 Need Help?

1. Check backend logs for errors
2. Check browser console for frontend errors
3. Verify all environment variables are set
4. Make sure Supabase project is active
5. Confirm API keys are valid

---

## 🎉 Success!

If you can:
- ✅ Generate a draft
- ✅ Edit with autosave
- ✅ See it in dashboard

**You're all set! The MVP is working perfectly.** 🚀

---

**Last Updated**: October 16, 2025  
**Status**: Production Ready ✅

