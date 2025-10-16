# Supabase Authentication Setup Guide

This guide will help you configure Supabase Auth for magic link authentication in CreatorPulse.

## Prerequisites

- A Supabase account and project
- Access to your Supabase dashboard

## Step 1: Get Your Supabase Credentials

1. Go to your [Supabase Dashboard](https://app.supabase.com/)
2. Select your CreatorPulse project
3. Navigate to **Settings** → **API**
4. Copy the following values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public** key
   - **service_role** key (⚠️ Keep this secret!)

## Step 2: Configure Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 3: Configure Backend Environment Variables

Update your `backend/.env` file:

```bash
# Existing Supabase config
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# JWT Configuration (use your Supabase JWT secret)
SECRET_KEY=your-supabase-jwt-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ... (rest of your existing config)
```

**Important:** The `SECRET_KEY` should be your Supabase JWT Secret, which you can find at:
- **Settings** → **API** → **JWT Secret**

## Step 4: Enable Email Auth in Supabase

1. In your Supabase Dashboard, go to **Authentication** → **Providers**
2. Find **Email** provider and click to configure
3. Enable **Email provider**
4. ✅ Enable **Confirm email**
5. ✅ Enable **Secure email change**
6. Click **Save**

## Step 5: Configure Magic Link Settings

1. Go to **Authentication** → **URL Configuration**
2. Add your site URLs:
   - **Site URL**: `http://localhost:3000` (for development)
   - **Redirect URLs**: Add these:
     - `http://localhost:3000/auth/callback`
     - `http://localhost:3000/**` (wildcard for all routes)

For production, add your production URLs as well.

## Step 6: Configure Email Templates (Optional)

1. Go to **Authentication** → **Email Templates**
2. Customize the **Magic Link** template:
   - Subject: "Your CreatorPulse Magic Link"
   - Body: Customize to match your brand

The default template works fine for development!

## Step 7: Test the Magic Link Flow

1. Start both backend and frontend servers:
   ```bash
   # Backend
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload
   
   # Frontend (in another terminal)
   cd frontend
   npm run dev
   ```

2. Navigate to `http://localhost:3000/login`
3. Enter your email address
4. Click "Send Magic Link"
5. Check your email inbox
6. Click the magic link
7. You should be redirected to `/auth/callback` and then to `/dashboard`

## Troubleshooting

### "Invalid or expired token" error
- Make sure your `SECRET_KEY` in backend `.env` matches your Supabase JWT Secret
- Check that the token hasn't expired (default: 1 hour)

### Magic link not working
- Verify your redirect URLs are correctly configured in Supabase
- Check that `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` are set correctly
- Make sure you're using the correct anon key (not service role key) in frontend

### Email not sending
- Check your email in Supabase Auth logs: **Authentication** → **Logs**
- For development, Supabase uses their email service by default
- For production, configure your own SMTP provider

### "User not found" errors
- The first time you use magic link, Supabase automatically creates the user
- Check **Authentication** → **Users** to see registered users
- Users are stored in `auth.users` table automatically

## Production Checklist

Before deploying to production:

- [ ] Update Site URL and Redirect URLs with production domain
- [ ] Configure custom SMTP provider (Settings → Auth → SMTP Settings)
- [ ] Enable rate limiting (Settings → Auth → Rate Limits)
- [ ] Customize email templates with your branding
- [ ] Add your domain to allowed redirect URLs
- [ ] Test magic link flow in production environment
- [ ] Set up custom domain for Supabase project (optional)

## Security Notes

⚠️ **Important Security Practices:**

1. **Never expose `service_role` key** in frontend code
2. **Keep JWT secret secure** - it's used to verify all tokens
3. **Use HTTPS** in production for all requests
4. **Enable RLS policies** on all tables to prevent unauthorized access
5. **Validate tokens** on every backend request

## Need Help?

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Magic Link Guide](https://supabase.com/docs/guides/auth/auth-magic-link)
- [Security Best Practices](https://supabase.com/docs/guides/auth/auth-security)

---

**You're all set! 🎉** Magic link authentication is now enabled for CreatorPulse.

