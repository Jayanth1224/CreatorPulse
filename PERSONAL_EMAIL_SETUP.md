# Personal Email Setup for CreatorPulse

## Quick Setup (5 minutes)

### 1. Choose Your Email Provider

**Gmail (Recommended for testing):**
- Turn on 2-Factor Authentication
- Go to Google Account → Security → App Passwords
- Generate an "App Password" for "Mail"
- Use these settings:

**Outlook/Hotmail:**
- Enable SMTP AUTH in your account settings
- Use your regular password (or app password if 2FA enabled)

**Zoho Mail:**
- Enable IMAP/SMTP in settings
- Use your regular password

### 2. Add to Your Backend .env File

Add these lines to `/Users/jayanthbandi/CreatorPulse/backend/.env`:

```bash
# Personal Email SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your_app_password_here
FROM_EMAIL=your.email@gmail.com
FROM_NAME=Your Name
```

### 3. Provider-Specific Settings

**Gmail:**
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

**Outlook/Hotmail:**
```bash
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
```

**Zoho:**
```bash
SMTP_HOST=smtp.zoho.com
SMTP_PORT=587
```

**Yahoo:**
```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
```

### 4. Test Your Setup

1. Restart your backend server
2. Create a draft in the app
3. Send it to yourself as a test
4. Check if you receive the email

### 5. Limits to Know

- **Gmail**: ~100-500 emails/day for personal accounts
- **Outlook**: Similar limits
- **Zoho**: Higher limits on paid plans

### 6. For Production Later

When you're ready for real newsletters:
1. Buy a domain (e.g., yourcompany.com)
2. Set up professional email (Zoho, Google Workspace, etc.)
3. Configure DNS records (SPF, DKIM)
4. Switch to SendGrid/Mailgun for better deliverability

## Troubleshooting

**"Authentication failed":**
- Check your app password (Gmail) or enable SMTP AUTH
- Verify username/password are correct

**"Connection refused":**
- Check SMTP_HOST and SMTP_PORT
- Try port 465 with SSL instead of 587 with TLS

**Emails go to spam:**
- This is normal with personal SMTP
- For production, use professional ESP (SendGrid/Mailgun)


