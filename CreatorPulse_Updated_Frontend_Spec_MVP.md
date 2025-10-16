# CreatorPulse — Updated Frontend Spec (MVP)

## Overview
This document describes the final updated frontend specification for **CreatorPulse MVP**, incorporating recent changes: simplified global navigation, preset bundles, a streamlined Create page that integrates directly with the existing Editor page, and minor Settings improvements.

---

## 1. Global Navigation

### Primary Nav (Top Bar)
```
[Logo] | Dashboard | Create | Analytics | Settings
```
Right side: `🔔 Notifications | 👤 Avatar`

- Identical across all pages.
- Active item is underlined and bold.
- Mobile: bottom tab bar with the same four primary items.

---

## 2. Page Overview

| Page | Route | Purpose |
|-------|--------|----------|
| Dashboard (Inbox) | `/dashboard` | Manage drafts (All, Sent, Scheduled, Bundles) |
| Create | `/create` | Generate a new draft from preset bundles |
| Editor | `/create/:draftId` | Edit, regenerate, or send a generated draft |
| Analytics | `/analytics` | Track open rates, CTR, review time, and performance |
| Settings | `/settings` | Manage account, ESP connection, tone, default recipient |

---

## 3. Create Page (New)

**Route:** `/create`

### Purpose
A minimal form to generate a new newsletter draft. Once generated, it opens directly in the existing Editor page.

### Layout
Centered vertical card (~600–700px width).

#### Header
**Title:** “Generate a New Draft”  
**Subtitle:** “Pick a bundle, add a focus, choose tone (optional). We’ll prepare a ready-to-edit newsletter draft.”

#### Form Fields
1. **Bundle Selector (Required)**  
   - Dropdown populated with **preset bundles** (searchable).  
   - Groups:  
     - ✨ Preset Bundles  
     - 📦 Your Custom Bundles (empty initially)  
   - Presets include:  
     - AI & ML Trends  
     - Creator Economy  
     - Marketing & Growth  
     - Startups & Innovation  
     - Cybersecurity & Privacy  
     - Productivity & Workflow Tools  
     - Sustainability & Future Tech  
     - Tech Policy & Regulation  
     - Health & Wellness Tech  
     - Mindset & Creativity  

2. **Topic / Focus (Optional)**  
   Input field for a short focus statement.  
   *Placeholder:* “e.g., AI content automation or Web3 community growth”

3. **Tone Preset (Optional)**  
   Dropdown or radio: Professional (default) / Conversational / Analytical / Friendly

4. **Generate Draft (Primary CTA)**  
   - Disabled until a bundle is selected.  
   - On click → spinner → calls `POST /drafts/generate`.  
   - On success → redirect to `/create/:draftId` (Editor).

#### Helper Text
> 💡 “We’ll analyze the latest posts from your selected bundle and prepare a newsletter draft in your voice.”

#### States
| State | Behavior |
|--------|-----------|
| Initial | Dropdown visible, Generate disabled |
| Generating | Spinner + “Generating draft…” |
| Error | Inline message: “Couldn’t generate draft. Try again.” |
| Success | Redirect to Editor page |

#### Empty State
If user has no bundles: “You haven’t connected any sources yet.” → CTA to Settings.

---

## 4. Editor Page (Existing)
**Route:** `/create/:draftId`  
- Reuses the existing WYSIWYG sectioned editor.  
- Autosave, section regenerate, thumbs feedback, tone control, revert, and send actions.  
- Send uses the user’s **default recipient list** (set in Settings).

---

## 5. Dashboard / Inbox

**Route:** `/dashboard`  
Displays daily drafts and previous sends.

### Tabs
All drafts | Sent | Scheduled | Bundles

### Draft Card
- Subject, date, brief summary, readiness %, and quick actions (open, regenerate).  
- Clicking a card → `/create/:draftId` (Editor).  
- Scroll position preserved on return.

---

## 6. Analytics Page

**Route:** `/analytics`  
Simple KPI overview:
- Open Rate (7-day / 30-day)
- CTR
- Avg Review Time
- Draft Acceptance Rate

Includes per-draft performance table linking to Editor.

---

## 7. Settings Page

**Route:** `/settings`

### Sections
- **Account:** name, email, timezone.  
- **ESP Connections:** connect SendGrid / Mailgun / SMTP; verify send.  
- **Default Recipient List (MVP):** one default recipient list or address for sending.  
- **Tone & Voice:** tone presets, upload >20 samples, opt-in/out of training.  
- **Billing & Plan:** subscription management.  

---

## 8. API Summary

| Method | Endpoint | Purpose |
|---------|-----------|----------|
| `POST` | `/drafts/generate` | Generate new draft from bundle/topic/tone |
| `GET` | `/drafts/:id` | Load draft for Editor |
| `POST` | `/drafts/:id/edit` | Autosave draft edits |
| `POST` | `/drafts/:id/regenerate` | Regenerate specific section |
| `POST` | `/drafts/:id/reactions` | Save thumbs feedback |
| `POST` | `/drafts/:id/send` | Send newsletter using default recipient list |
| `GET` | `/bundles/presets` | (Optional) return list of preset bundles |
| `POST` | `/user/default-recipient` | Save default recipient list |

---

## 9. Data Model (Frontend Summary)

### Draft Object
```json
{
  "id": "string",
  "bundle": "string",
  "tone": "string",
  "topic": "string",
  "generated_html": "string",
  "edited_html": "string",
  "sources": ["string"],
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Bundle Object
```json
{
  "key": "string",
  "label": "string",
  "description": "string",
  "sources": ["string"]
}
```

---

## 10. UX Flow

**Generate + Edit Flow**
1. User visits `/create`  
2. Selects bundle → optional topic/tone → clicks Generate  
3. App calls `POST /drafts/generate`  
4. Backend returns `{ draftId }`  
5. Redirect → `/create/:draftId` → Editor page opens generated draft

**Inbox → Editor Flow**
1. User opens `/dashboard`  
2. Clicks a draft card → opens `/create/:draftId`  
3. Edits or sends the draft

---

## 11. Accessibility & UX Rules
- Keyboard accessible nav; `aria-current` on active page.  
- Visible focus outlines on all inputs and buttons.  
- High contrast and readable labels.  
- Spinner/Loading text announced for screen readers.

---

## 12. Acceptance Criteria
- Consistent nav across all pages.  
- Create page prefilled with preset bundles.  
- Generate disabled until bundle chosen.  
- Generate → API call → redirect to Editor.  
- Inbox → Editor → back preserves position.  
- Settings page allows ESP + default recipient setup.  
- Mobile responsive; all primary actions accessible.

---

## 13. Future Enhancements (Post-MVP)
- Multi-bundle selection.  
- Scheduled sends.  
- In-editor re-generation of entire draft.  
- “Regenerate Again” flow from Create page.  
- Manage Bundles in Settings.  
- AI-driven “Suggested Topics” based on bundle trends.

---

## End of Spec
