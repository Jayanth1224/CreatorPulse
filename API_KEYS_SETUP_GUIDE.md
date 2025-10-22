# API Keys Setup Guide

**Date**: December 19, 2024  
**Purpose**: Configure API keys for advanced auto-newsletter features

---

## 🔧 Where to Configure API Keys

### 1. **Environment Variables File**
Create or update your `.env` file in the `backend/` directory:

```bash
# Navigate to backend directory
cd backend/

# Create or edit .env file
nano .env
```

### 2. **Add the Following Variables to .env**

```bash
# ===========================================
# EXISTING CONFIGURATION (keep these)
# ===========================================

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=z-ai/glm-4.5-air:free

# Security
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key

# LinkedIn OAuth (optional)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Email Configuration (optional)
SENDGRID_API_KEY=your_sendgrid_api_key
SMTP_HOST=your_smtp_host
SMTP_PORT=587
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password

# ===========================================
# NEW ADVANCED FEATURES API KEYS
# ===========================================

# Firecrawl API Key (for web crawling and trend data)
FIRECRAWL_API_KEY=your_firecrawl_api_key

# Google Trends API Key (for trend detection)
GOOGLE_TRENDS_API_KEY=your_google_trends_api_key
```

---

## 🔑 How to Get API Keys

### 1. **Firecrawl API Key** (Required for trend detection)

**What it does**: Provides web crawling and content extraction for trend analysis

**How to get it**:
1. Go to [Firecrawl.dev](https://firecrawl.dev)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key
5. Add to `.env` file as `FIRECRAWL_API_KEY=your_key_here`

**Pricing**: Free tier available, paid plans for higher usage

### 2. **Google Trends API Key** (Optional, for enhanced trend data)

**What it does**: Provides real-time Google Trends data for better trend detection

**How to get it**:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable the "Google Trends API" 
4. Create credentials (API key)
5. Add to `.env` file as `GOOGLE_TRENDS_API_KEY=your_key_here`

**Note**: This is optional. The system will work without it using simulated trend data.

---

## 🚀 Quick Setup Steps

### Step 1: Create .env file
```bash
cd backend/
touch .env
```

### Step 2: Add your existing keys
Copy your existing configuration from your current setup.

### Step 3: Add new API keys
Add the Firecrawl API key (required) and Google Trends API key (optional).

### Step 4: Test the configuration
```bash
# Start the server
python -m uvicorn app.main:app --reload

# Check if the server starts without errors
# Look for any "API key not configured" warnings in the logs
```

---

## 🔍 Verification

### Check if API keys are loaded:
```bash
# Test the health endpoint
curl http://localhost:8000/health

# Check server logs for any API key warnings
# Look for messages like:
# - "Firecrawl API key not configured"
# - "Google Trends API key not configured"
```

### Test trend detection:
```bash
# Create a test auto-newsletter with trend detection
curl -X POST "http://localhost:8000/api/advanced-auto-newsletter/create" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "bundle_id": "test-bundle",
    "trend_detection": {
      "enabled": true,
      "keywords": ["AI", "Machine Learning"]
    }
  }'
```

---

## ⚠️ Important Notes

### 1. **API Key Security**
- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore` file
- Use environment variables in production

### 2. **Optional vs Required**
- **Firecrawl API Key**: Required for trend detection to work properly
- **Google Trends API Key**: Optional, system works without it

### 3. **Fallback Behavior**
- If Firecrawl API key is missing: Trend detection will use simulated data
- If Google Trends API key is missing: Will use alternative trend sources
- System will log warnings but continue to function

### 4. **Rate Limits**
- Firecrawl: Check your plan's rate limits
- Google Trends: Free tier has daily limits
- Monitor usage in your respective dashboards

---

## 🛠️ Troubleshooting

### Common Issues:

#### 1. **"API key not configured" warnings**
```bash
# Check if .env file exists and has the right keys
cat backend/.env | grep -E "(FIRECRAWL|GOOGLE_TRENDS)"
```

#### 2. **Trend detection not working**
```bash
# Check server logs for API errors
# Look for HTTP 401/403 errors from Firecrawl
```

#### 3. **Environment variables not loading**
```bash
# Make sure .env file is in the backend/ directory
# Restart the server after adding new variables
```

#### 4. **API key format issues**
```bash
# Make sure there are no extra spaces or quotes
FIRECRAWL_API_KEY=fc-your-actual-key-here
# NOT: FIRECRAWL_API_KEY="fc-your-actual-key-here"
# NOT: FIRECRAWL_API_KEY = fc-your-actual-key-here
```

---

## 📋 Complete .env Template

Here's a complete `.env` template with all possible variables:

```bash
# ===========================================
# CORE CONFIGURATION (Required)
# ===========================================
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
OPENROUTER_API_KEY=your_openrouter_api_key
SECRET_KEY=your_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# ===========================================
# OPTIONAL INTEGRATIONS
# ===========================================
# LinkedIn OAuth
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Email Services
SENDGRID_API_KEY=your_sendgrid_api_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# ===========================================
# ADVANCED AUTO-NEWSLETTER FEATURES
# ===========================================
# Firecrawl (Required for trend detection)
FIRECRAWL_API_KEY=fc-your_firecrawl_api_key_here

# Google Trends (Optional, for enhanced trends)
GOOGLE_TRENDS_API_KEY=your_google_trends_api_key_here

# ===========================================
# SERVER CONFIGURATION
# ===========================================
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
CORS_ORIGINS=http://localhost:3000
```

---

## ✅ Success Checklist

- [ ] `.env` file created in `backend/` directory
- [ ] Firecrawl API key added and working
- [ ] Google Trends API key added (optional)
- [ ] Server starts without API key errors
- [ ] Trend detection works in test requests
- [ ] No sensitive keys committed to git

---

## 🆘 Need Help?

### If you're having issues:

1. **Check the server logs** for specific error messages
2. **Verify API key format** (no extra spaces or quotes)
3. **Test API keys independently** using curl or Postman
4. **Check rate limits** in your API provider dashboards
5. **Restart the server** after making changes

### Support Resources:
- Firecrawl Documentation: https://docs.firecrawl.dev
- Google Trends API: https://developers.google.com/trends
- CreatorPulse Documentation: See `ADVANCED_AUTO_NEWSLETTER_FEATURES.md`

**Your advanced auto-newsletter features are now ready to use! 🚀**
