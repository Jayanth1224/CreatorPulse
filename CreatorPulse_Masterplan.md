# CreatorPulse — Masterplan.md

## 🧭 Overview
**CreatorPulse** is a daily feed curator and newsletter drafting assistant designed for newsletter writers, content curators, and agency professionals.  
It automatically aggregates insights from trusted sources, detects emerging trends, and generates voice-matched newsletter drafts — all delivered via email at **08:00 local time**.

### 🎯 Core Objective
Reduce newsletter creation time from **2–3 hours to under 20 minutes** by automating research, summarization, and first-draft creation — enabling creators to publish more consistently, with higher engagement and less fatigue.

---

## 👥 Target Audience
| Persona | Key Need | Why They’ll Buy First |
|----------|-----------|-----------------------|
| **Independent Creator / Curator** (Substack, Beehiiv, etc.) | Time savings, consistency, voice fidelity | Direct pain, quick ROI via improved consistency & engagement |
| **Agency / Brand Newsletter Manager** | Scalable curation and feed aggregation | Reduces manual monitoring; cost aligns with output volume |

---

## 💼 Jobs To Be Done
As a **content curator or agency professional**, I want to:
1. Aggregate insights from my chosen sources (Twitter handles, newsletters, YouTube channels).  
2. Tap into emerging trends without manually scanning dozens of feeds.  
3. Receive a **voice-matched draft newsletter** that feels 70%+ ready to send.  
4. Review, tweak, and approve in under 20 minutes.  
5. Deliver the final draft via email (no dashboards).  
6. Track open and click-through rates to prove ROI.

---

## ⚙️ Core MVP Features

### 1. Source Connections
- Twitter handles / hashtags  
- YouTube channels  
- Newsletter RSS feeds / custom parsing  

🔧 **Implementation Approach:**  
Hybrid method — RSS feeds + official APIs (YouTube, Twitter/X) for structured data.  
Future: expand to arXiv, TechCrunch, Google Trends.

### 2. Research & Trend Engine
- **Scheduled crawls** via Firecrawl or cron jobs  
- **Spike detection** using Google Alerts / Trends APIs  
- **Aggregation logic:** identify topics with unusual content velocity or engagement  
- **Filtering:** remove duplicates, promotional noise, or low-quality posts  

### 3. Writing Style Trainer
#### a. For new users:
- Choose from predefined tone categories (e.g., *Analyst*, *Storyteller*, *Curator*).  

#### b. For experienced writers:
- Upload ≥20 top newsletters/posts (CSV or text paste).  
- Use **in-context learning** to match their style and tone.  

#### c. Feedback Loop:
- Inline 👍 / 👎 reactions and auto-diff on edits.  
- Continuous tone refinement and source ranking optimization.  
- Approved drafts feed into personalized style retraining.

### 4. Newsletter Draft Generator
- Generates a ready-to-edit **250–400 word newsletter draft**.  
- Includes:  
  - Intro paragraph (contextual hook)  
  - 3–5 key insights with short summaries  
  - “Trends to Watch” block  
  - Source citations  
- Tailored to the user’s tone profile.  

### 5. Morning Delivery
- **Daily email** at **08:00 local time**.  
- Contains:  
  1. Pulse Summary (top 3–5 insights)  
  2. Newsletter Draft (ready-to-edit)  
  3. Source Bundle (citations and links)  
  4. Quick Actions (Edit, Regenerate Tone, Add to Next Issue)  


### 6. Delivery & Analytics
- **ESP/SMTP Integration (MVP)**  
  - Connect SendGrid, Mailgun, Postmark, or SMTP credentials.  
  - CreatorPulse sends via the user’s existing ESP for compliance and deliverability.  
- **Engagement Tracking**  
  - Insert tracking pixels and wrapped links to measure opens and CTR.  
  - Aggregate metrics returned via ESP webhooks.  
- Weekly engagement summaries emailed to user.

### 7. Feedback & Continuous Learning
- Users can react inline or reply to email feedback prompts.  
- System learns from:
  - Edits (auto-diff comparison)  
  - Reactions (👍 / 👎 per insight)  
  - Open & CTR signals (to adjust source prioritization).  

### 8. Optional Web Dashboard (v1.1+)
- Source management  
- Delivery preferences  
- Usage & billing overview  

---

## 📊 Success Metrics (90 Days)
| Metric | Target |
|--------|--------|
| Avg. review time per accepted draft | ≤ 20 minutes |
| Draft acceptance rate | ≥ 70% |
| Engagement uplift (open/CTR) | ≥ 2× baseline |
| Active daily users | 60%+ of early signups |

---

## 💰 Monetization Strategy
**Model:** Freemium → Paid Upgrade  

| Tier | Features | Price |
|------|-----------|-------|
| **Free Plan** | 1 topic bundle, basic summaries, default tone | $0 |
| **Pro Plan** | Custom voice training, analytics, 3+ bundles | ~$20–$30/mo |
| **Agency Plan** | Multi-newsletter support, shared analytics | Custom (usage-based) |


---

## 🔐 Security & Compliance
- OAuth-secured ESP connections (SendGrid, Mailgun, etc.)  
- All credentials encrypted (AES256).  
- Email deliverability handled by user’s ESP (SPF/DKIM compliance).  
- GDPR-safe opt-out tracking for engagement metrics.

---


## ⚠️ Key Challenges & Mitigations

| Challenge | Mitigation |
|------------|-------------|
| API rate limits (Twitter/YouTube) | Caching, delta crawls, back-off queues |
| Voice mismatch or tone drift | Human-in-loop feedback retraining |
| Trend false positives | Ensemble scoring + manual override flag |
| Email deliverability | ESP integration, verified sender domains |
| Content bias/noise | Source weighting based on user edits & engagement |

---

## 🌱 Future Expansion Ideas
- Integrate with **Beehiiv/Substack APIs** for automatic scheduling.  
- Add **AI-generated visuals** (charts or cover images) to drafts.  
- Launch **CreatorPulse Chrome Extension** for one-click content clipping.  
- Multi-language support (EN → HI, DE, ES).  
- Direct **social post generation** for X and LinkedIn.

---

## 🧩 Conceptual Data Model
```
User
 ├─ profile (name, email, timezone)
 ├─ preferences (tone, bundles)
 ├─ sources [array]
 ├─ ESP credentials (encrypted)
 ├─ analytics summary (open_rate, ctr)
 └─ feedback history

Source
 ├─ type (Twitter, YouTube, RSS)
 ├─ feed_url / handle / hashtag
 ├─ last_crawled
 └─ signal_score

Draft
 ├─ generated_content
 ├─ edit_diffs
 ├─ feedback (👍 / 👎)
 ├─ send_status
 └─ performance_metrics
```

---

## 🧠 Conceptual Stack Recommendation
| Layer | Recommended Approach | Notes |
|-------|----------------------|-------|
| **Content Aggregation** | Firecrawl + RSS + YouTube/Twitter APIs | Proven, modular, scalable |
| **Processing & Trend Detection** | Python (cron jobs, Google Trends API, NLP for deduplication) | Stable ecosystem for parsing and scheduling |
| **Draft Generation** | OpenAI GPT models with in-context learning | Tuned with user samples |
| **Email Delivery** | Node.js/Express + ESP APIs (SendGrid, Mailgun) | Secure and flexible |
| **Data Storage** | PostgreSQL (structured), Redis (queue/cache) | Reliable foundation |
| **Analytics Tracking** | Webhook ingestion + tracking pixels | Simple, privacy-safe analytics |
| **Future Dashboard** | React + Next.js + Tailwind + Shadcn | Clean, maintainable UI stack |

---

## 🧭 Summary
CreatorPulse redefines the content curation workflow for creators and agencies.  
It automates research, preserves voice, and delivers ready-to-send newsletters — daily, via email.  
By balancing simplicity (no dashboards) with intelligence (voice training + trend detection), CreatorPulse gives creators their most precious resource back: **time**.
