from typing import Dict
from datetime import datetime
from app.services.rss_service import RSSService
from app.services.ai_service import AIService
from app.services.email_template_service import EmailTemplateService
from app.services.content_extractor_service import ContentExtractorService
from app.routers.bundles import PRESET_BUNDLES
import uuid


class DraftGeneratorService:
    """Service to orchestrate draft generation from RSS feeds + AI"""
    
    def __init__(self):
        self.rss_service = RSSService()
        self.ai_service = AIService()
        self.email_template_service = EmailTemplateService()
        self.content_extractor = ContentExtractorService()
    
    async def generate_draft(
        self,
        user_id: str,
        bundle_id: str,
        topic: str = None,
        tone: str = "professional"
    ) -> Dict:
        """Generate a complete newsletter draft"""
        
        # 1. Get bundle information
        print(f"[GENERATOR] Step 1: Getting bundle {bundle_id}")
        bundle = self._get_bundle(bundle_id)
        if not bundle:
            raise ValueError(f"Bundle {bundle_id} not found")
        print(f"[GENERATOR] Found bundle: {bundle['label']}")
        
        # 2. Parse RSS feeds
        print(f"[GENERATOR] Step 2: Parsing {len(bundle['sources'])} RSS feeds")
        entries = self.rss_service.parse_multiple_feeds(bundle["sources"])
        print(f"[GENERATOR] Parsed {len(entries)} entries")
        
        # 3. Filter and score entries
        print(f"[GENERATOR] Step 3: Filtering and scoring entries")
        recent_entries = self.rss_service.filter_recent_entries(entries, days=7)
        scored_entries = self.rss_service.score_entries(recent_entries, topic)
        print(f"[GENERATOR] Using {len(scored_entries)} scored entries")
        
        # 4. Generate draft using AI
        print(f"[GENERATOR] Step 4: Generating draft with Openrouter API")
        ai_generated_html = await self.ai_service.generate_newsletter_draft(
            entries=scored_entries,
            tone=tone,
            topic=topic,
            bundle_name=bundle["label"]
        )
        print(f"[GENERATOR] AI draft generated successfully")
        
        # 5. Generate professional email template with new structure
        print(f"[GENERATOR] Step 5: Generating professional email template with separated content")
        bundle_color = bundle.get("color", "#3B82F6")
        full_email_html = self.email_template_service.generate_newsletter_html(
            draft_content=ai_generated_html,
            bundle_name=bundle["label"],
            bundle_color=bundle_color,
            entries=scored_entries[:10],
            include_images=True
        )
        print(f"[GENERATOR] Email template with new structure generated successfully")
        
        # 6. Use original AI-generated content for editing (don't extract from template)
        print(f"[GENERATOR] Step 6: Using original AI content for editing")
        editable_content = ai_generated_html  # Use the original AI content directly
        print(f"[GENERATOR] Using original AI content for editor")
        
        # 7. Calculate readiness score
        readiness_score = self._calculate_readiness_score(
            full_email_html,
            len(scored_entries)
        )
        
        # 8. Extract source links
        source_links = [entry["link"] for entry in scored_entries[:10] if entry.get("link")]
        
        # 9. Create draft object
        draft_data = {
            "user_id": user_id,
            "bundle_id": bundle_id,
            "bundle_name": bundle["label"],
            "topic": topic,
            "tone": tone,
            "generated_html": editable_content,  # Store editable content for editor
            "full_email_html": full_email_html,  # Store full template for sending
            "edited_html": None,
            "status": "draft",
            "readiness_score": readiness_score,
            "sources": source_links
        }
        
        # 8. Save to Supabase database
        from app.database import SupabaseDB
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        response = db.table("drafts").insert(draft_data).execute()
        
        if not response.data:
            raise Exception("Failed to save draft to database")
        
        saved_draft = response.data[0]
        print(f"[GENERATOR] Draft saved to database with ID: {saved_draft['id']}")
        
        return saved_draft
    
    def _get_bundle(self, bundle_id: str) -> Dict:
        """Get bundle by ID"""
        return next((b for b in PRESET_BUNDLES if b["id"] == bundle_id), None)
    
    def _calculate_readiness_score(self, html_content: str, num_sources: int) -> int:
        """Calculate how ready the draft is (0-100)"""
        score = 0
        
        # Has content
        if len(html_content) > 200:
            score += 40
        
        # Has multiple sections
        if html_content.count("<h") >= 3:
            score += 20
        
        # Has insights
        if "draft-insight" in html_content or "<h3>" in html_content:
            score += 20
        
        # Has sources
        if num_sources >= 5:
            score += 20
        
        return min(score, 100)

