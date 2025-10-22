from typing import Dict, List, Optional
from app.services.email_template_service import EmailTemplateService
from app.database import SupabaseDB
import json


class EmailRendererService:
    """Service for rendering drafts into professional email HTML"""
    
    def __init__(self):
        self.template_service = EmailTemplateService()
    
    async def render_draft_for_sending(
        self,
        draft_id: str,
        custom_subject: str = None,
        custom_bundle_color: str = None
    ) -> Dict:
        """Render a draft into final email HTML for sending"""
        
        # Get draft from database
        db = SupabaseDB.get_service_client()
        draft_response = db.table("drafts").select("*").eq("id", draft_id).execute()
        
        if not draft_response.data:
            raise ValueError(f"Draft {draft_id} not found")
        
        draft = draft_response.data[0]
        
        # Get bundle information for customization
        bundle_info = self._get_bundle_info(draft.get("bundle_id"))
        
        # Use custom color if provided, otherwise use bundle color
        bundle_color = custom_bundle_color or bundle_info.get("color", "#3B82F6")
        
        # Always generate from new template structure (ignore old full_email_html)
        # This ensures we use the new separated content structure
        final_html = self.template_service.generate_newsletter_html(
            draft_content=draft.get("generated_html", ""),
            bundle_name=draft.get("bundle_name", "Newsletter"),
            bundle_color=bundle_color,
            entries=self._get_draft_entries(draft),
            include_images=True
        )
        
        # Generate subject line
        subject = custom_subject or self._generate_subject_line(draft)
        
        return {
            "html_content": final_html,
            "subject": subject,
            "bundle_name": draft.get("bundle_name"),
            "bundle_color": bundle_color,
            "draft_id": draft_id
        }
    
    async def render_preview(
        self,
        draft_id: str,
        custom_bundle_color: str = None
    ) -> Dict:
        """Render a draft for preview (without tracking pixels)"""
        
        # Get draft from database
        db = SupabaseDB.get_service_client()
        draft_response = db.table("drafts").select("*").eq("id", draft_id).execute()
        
        if not draft_response.data:
            raise ValueError(f"Draft {draft_id} not found")
        
        draft = draft_response.data[0]
        
        # Get bundle information
        bundle_info = self._get_bundle_info(draft.get("bundle_id"))
        bundle_color = custom_bundle_color or bundle_info.get("color", "#3B82F6")
        
        # Generate preview HTML (same as final but without tracking)
        preview_html = self.template_service.generate_newsletter_html(
            draft_content=draft.get("generated_html", ""),
            bundle_name=draft.get("bundle_name", "Newsletter"),
            bundle_color=bundle_color,
            entries=self._get_draft_entries(draft),
            include_images=True
        )
        
        return {
            "html_content": preview_html,
            "bundle_name": draft.get("bundle_name"),
            "bundle_color": bundle_color,
            "readiness_score": draft.get("readiness_score", 0)
        }
    
    def _get_bundle_info(self, bundle_id: str) -> Dict:
        """Get bundle information for customization"""
        # Import here to avoid circular imports
        from app.routers.bundles import PRESET_BUNDLES
        
        bundle = next((b for b in PRESET_BUNDLES if b["id"] == bundle_id), {})
        return bundle
    
    def _get_draft_entries(self, draft: Dict) -> List[Dict]:
        """Extract entries from draft sources"""
        sources = draft.get("sources", [])
        entries = []
        
        print(f"[EMAIL_RENDERER] Draft sources: {sources}")
        
        for source_url in sources[:10]:  # Limit to 10 sources
            if source_url and source_url.strip():  # Only add non-empty URLs
                entries.append({
                    "title": f"Source Article",
                    "link": source_url,
                    "summary": "Read the full article for more details.",
                    "published": None,
                    "image": None
                })
        
        print(f"[EMAIL_RENDERER] Generated entries: {len(entries)}")
        return entries
    
    def _generate_subject_line(self, draft: Dict) -> str:
        """Generate a compelling subject line for the newsletter"""
        bundle_name = draft.get("bundle_name", "Newsletter")
        topic = draft.get("topic", "")
        
        # Get current date for time-sensitive subject
        from datetime import datetime
        today = datetime.now()
        
        # Generate subject based on content
        if topic:
            return f"{bundle_name}: {topic} Update - {today.strftime('%B %d')}"
        else:
            return f"{bundle_name} Daily Digest - {today.strftime('%B %d, %Y')}"
    
    async def render_test_email(
        self,
        bundle_name: str = "Test Newsletter",
        bundle_color: str = "#3B82F6"
    ) -> Dict:
        """Render a test email for preview purposes"""
        
        # Create sample content
        sample_content = """
        <div class="draft-intro">
            <h2>Welcome to Your Newsletter</h2>
            <p>This is a sample newsletter to test the email template and formatting.</p>
        </div>
        
        <div class="draft-insight">
            <h3>Sample Story 1</h3>
            <p>This is a sample news story that demonstrates how content will appear in your newsletter.</p>
        </div>
        
        <div class="draft-insight">
            <h3>Sample Story 2</h3>
            <p>Another sample story to show the variety of content in your newsletter.</p>
        </div>
        
        <div class="draft-trends">
            <h3>Trends to Watch</h3>
            <ul>
                <li>Sample trend 1</li>
                <li>Sample trend 2</li>
                <li>Sample trend 3</li>
            </ul>
        </div>
        """
        
        # Generate test HTML
        test_html = self.template_service.generate_newsletter_html(
            draft_content=sample_content,
            bundle_name=bundle_name,
            bundle_color=bundle_color,
            entries=[],
            include_images=True
        )
        
        return {
            "html_content": test_html,
            "subject": f"{bundle_name} - Test Email",
            "bundle_name": bundle_name,
            "bundle_color": bundle_color
        }
