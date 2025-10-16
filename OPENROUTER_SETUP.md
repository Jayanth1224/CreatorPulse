# Openrouter API Setup Guide

CreatorPulse now uses **Openrouter API** instead of OpenAI, which gives you access to the **FREE** GLM-4.5-air model!

## 🎉 Benefits

- ✅ **100% FREE** with z-ai/glm-4.5-air:free model
- ✅ No credit card required
- ✅ Great performance for newsletter generation
- ✅ Easy to switch to other models if needed

## 🔑 Get Your API Key

### Step 1: Sign Up
1. Go to [https://openrouter.ai/](https://openrouter.ai/)
2. Click "Sign In" or "Sign Up"
3. Create a free account (can use GitHub, Google, or email)

### Step 2: Create API Key
1. After logging in, go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Click "Create Key"
3. Give it a name (e.g., "CreatorPulse")
4. Copy your API key (starts with `sk-or-v1-...`)

### Step 3: Add to .env
1. Open `/backend/.env` in your editor
2. Replace the placeholder:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-YOUR_ACTUAL_KEY_HERE
   OPENROUTER_MODEL=z-ai/glm-4.5-air:free
   ```
3. Save the file

### Step 4: Restart Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

## 🧪 Test It

Once your backend is running with the API key:

### Test Draft Generation
```bash
curl -X POST http://localhost:8000/api/drafts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "bundle_id": "preset-1",
    "topic": "AI automation",
    "tone": "professional"
  }'
```

Or visit: `http://localhost:8000/docs` and test via the interactive API docs!

## 🔄 Using Different Models

Want to try other models? Just change `OPENROUTER_MODEL` in `.env`:

### Free Models
```env
OPENROUTER_MODEL=z-ai/glm-4.5-air:free
OPENROUTER_MODEL=google/gemini-flash-1.5:free
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
```

### Paid Models (for better quality)
```env
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_MODEL=openai/gpt-4o
OPENROUTER_MODEL=google/gemini-pro-1.5
```

See all models at: [https://openrouter.ai/models](https://openrouter.ai/models)

## 💰 Costs (if using paid models)

- **Free models**: $0.00 per generation ✨
- **Paid models**: You'll need to add credits to your Openrouter account
  - Rates vary by model
  - Typically $0.001-0.01 per newsletter draft
  - Much cheaper than direct OpenAI API

## 📊 Check Your Usage

Visit [https://openrouter.ai/activity](https://openrouter.ai/activity) to:
- See your API usage
- Track costs
- Monitor rate limits

## 🐛 Troubleshooting

### "Authentication failed"
- Check your API key is correct in `.env`
- Make sure it starts with `sk-or-v1-`
- Verify your Openrouter account is active

### "Model not found"
- Check model name spelling in `.env`
- Visit [https://openrouter.ai/models](https://openrouter.ai/models) for valid model names
- Some models require credits even if they're listed

### "Rate limit exceeded"
- Free tier has rate limits
- Wait a few minutes and try again
- Consider upgrading or using paid models

## ✨ Why Openrouter?

1. **Access to Multiple AI Models** - Switch between models easily
2. **Better Pricing** - Often cheaper than direct API access
3. **Free Tier** - Test without cost
4. **No Vendor Lock-in** - Easy to switch providers
5. **Unified API** - One API for all models

## 🔐 Security

- Never commit your `.env` file (it's in `.gitignore`)
- Keep your API key secret
- Rotate keys if compromised
- Use separate keys for dev/prod

---

**Ready to generate your first newsletter draft!** 🚀

Visit the frontend at `http://localhost:3000`, click "Create", select a bundle, and generate!

