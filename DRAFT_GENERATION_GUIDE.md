# Draft Generation Guide

## ✅ System Status: WORKING!

Your CreatorPulse backend is now successfully generating newsletter drafts using Openrouter API!

## 🚀 What's Working

- ✅ **Frontend**: Connected to real backend API
- ✅ **Backend**: Generating drafts successfully
- ✅ **RSS Parsing**: Fetching articles from TechCrunch and other feeds
- ✅ **Openrouter API**: Using free GLM-4.5-air model
- ✅ **Draft Quality**: Professional HTML-formatted newsletters

## ⏱️ Expected Timings

**Draft Generation Process:**
1. Parsing RSS feeds: ~5-8 seconds
2. AI generation (Openrouter): ~10-15 seconds
3. **Total time: 15-25 seconds**

This is normal! The frontend now shows a message: "Parsing RSS feeds and generating with AI... This may take 20-30 seconds."

## 🎯 How to Generate a Draft

### Via Frontend (http://localhost:3000)

1. Click "Create" in the navigation
2. Select a bundle (e.g., "AI & ML Trends")
3. Optionally add a topic (e.g., "AI automation")
4. Click "Generate Draft"
5. Wait 20-30 seconds (you'll see a loading spinner)
6. You'll be redirected to the Editor with your draft!

### Via API (http://localhost:8000/docs)

```bash
curl -X POST http://localhost:8000/api/drafts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "bundle_id": "preset-1",
    "topic": "AI automation",
    "tone": "professional"
  }'
```

## 📊 What You Get

The AI generates a structured newsletter with:
- **Intro**: Context-setting opening paragraph
- **3-5 Key Insights**: Detailed developments from RSS feeds
- **Trends to Watch**: Bullet points of emerging patterns
- **HTML Formatting**: Ready-to-send structure

Example output structure:
```html
<div class="draft-intro">
  <p>Opening paragraph...</p>
</div>

<div class="draft-insight">
  <h2>Key Insight Title</h2>
  <p>Detailed analysis...</p>
</div>

<div class="draft-trends">
  <h3>Trends to Watch</h3>
  <ul>
    <li>Trend 1</li>
    <li>Trend 2</li>
  </ul>
</div>
```

## 🔧 Recent Fixes Applied

1. **Added Timeouts**:
   - RSS parsing: 10 seconds per feed
   - Openrouter API: 30 seconds
   
2. **Improved Error Handling**:
   - Better error messages
   - Detailed logging
   - Graceful fallbacks

3. **Frontend Updates**:
   - Connected to real backend
   - Shows loading time estimate
   - Displays generated HTML correctly
   - Fallback to mock data for testing

4. **Logging Added**:
   - Track each step of generation
   - See RSS feed results
   - Monitor API calls

## 📝 Available Bundles

1. **AI & ML Trends** - TechCrunch AI, VentureBeat AI
2. **Creator Economy** - Creator economy insights
3. **Marketing & Growth** - Growth hacking, strategies
4. **Startups & Innovation** - Startup news and funding
5. **Cybersecurity & Privacy** - Security news
6. **Productivity & Workflow Tools**
7. **Sustainability & Future Tech**
8. **Tech Policy & Regulation**
9. **Health & Wellness Tech**
10. **Mindset & Creativity**

## 🐛 Troubleshooting

### "Still loading after 30 seconds"
- Check backend logs: `tail -f /tmp/creatorpulse_backend.log`
- Backend might have crashed - restart it
- RSS feeds might be very slow

### "Error: Failed to generate draft"
- Check your Openrouter API key in `.env`
- Make sure backend is running: `curl http://localhost:8000/`
- Check browser console for errors (F12)

### "Draft looks weird in Editor"
- The backend returns HTML - browser should render it
- Some markdown might not be converted - this is OK
- You can edit the HTML directly

## 🎨 Customization

### Change the AI Model
Edit `/backend/.env`:
```env
OPENROUTER_MODEL=google/gemini-flash-1.5:free
# or
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet  # paid
```

### Adjust Tone
In the Create page, select:
- Professional (default)
- Conversational
- Analytical
- Friendly

### Add Custom Topics
Just type your focus in the "What's today's focus?" field:
- "AI content automation"
- "Web3 community growth"
- "Marketing automation tools"

## 📊 Check Backend Logs

Real-time:
```bash
tail -f /tmp/creatorpulse_backend.log
```

You'll see:
```
[DRAFT] Starting generation for bundle preset-1
[GENERATOR] Step 1: Getting bundle preset-1
[GENERATOR] Found bundle: AI & ML Trends
[GENERATOR] Step 2: Parsing 2 RSS feeds
[GENERATOR] Parsed 20 entries
[GENERATOR] Step 3: Filtering and scoring entries
[GENERATOR] Using 20 scored entries
[GENERATOR] Step 4: Generating draft with Openrouter API
[GENERATOR] Draft generated successfully
[DRAFT] Successfully generated draft draft-xxxxx
```

## 🎉 Next Steps

1. **Test it out!**
   - Go to http://localhost:3000/create
   - Select a bundle
   - Generate a draft
   - Wait 20-30 seconds
   - See your AI-generated newsletter!

2. **Refine prompts** in `/backend/app/services/ai_service.py`

3. **Add more RSS feeds** to bundles in `/backend/app/routers/bundles.py`

4. **Deploy** when ready (Vercel + Railway + Supabase)

---

**Everything is working! Go try it out at http://localhost:3000/create** 🚀

