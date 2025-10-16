from typing import List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings


class EmailService:
    """Service for sending emails via ESP (SendGrid, Mailgun, SMTP)"""
    
    def __init__(self):
        self.sendgrid_client = None
        if hasattr(settings, 'sendgrid_api_key'):
            self.sendgrid_client = SendGridAPIClient(settings.sendgrid_api_key)
    
    async def send_newsletter(
        self,
        to_emails: List[str],
        from_email: str,
        from_name: str,
        subject: str,
        html_content: str,
        draft_id: str = None
    ) -> bool:
        """Send newsletter email"""
        
        # For MVP, simulate sending
        # TODO: Implement actual ESP integration
        
        print(f"[EMAIL] Sending newsletter:")
        print(f"  To: {', '.join(to_emails)}")
        print(f"  From: {from_name} <{from_email}>")
        print(f"  Subject: {subject}")
        print(f"  Draft ID: {draft_id}")
        
        # Simulate success
        return True
    
    async def send_via_sendgrid(
        self,
        to_emails: List[str],
        from_email: str,
        from_name: str,
        subject: str,
        html_content: str
    ) -> bool:
        """Send email via SendGrid"""
        try:
            message = Mail(
                from_email=(from_email, from_name),
                to_emails=to_emails,
                subject=subject,
                html_content=html_content
            )
            
            if self.sendgrid_client:
                response = self.sendgrid_client.send(message)
                return response.status_code in [200, 201, 202]
            
            return False
        
        except Exception as e:
            print(f"Error sending via SendGrid: {str(e)}")
            return False
    
    def add_tracking_pixel(self, html_content: str, draft_id: str, base_url: str) -> str:
        """Add tracking pixel to email for open tracking"""
        pixel_url = f"{base_url}/api/tracking/open/{draft_id}"
        tracking_pixel = f'<img src="{pixel_url}" width="1" height="1" alt="" />'
        
        # Insert before closing body tag
        if "</body>" in html_content:
            html_content = html_content.replace("</body>", f"{tracking_pixel}</body>")
        else:
            html_content += tracking_pixel
        
        return html_content
    
    def wrap_links_for_tracking(self, html_content: str, draft_id: str, base_url: str) -> str:
        """Wrap all links with tracking redirects"""
        # Simple implementation - in production, use proper HTML parser
        import re
        
        def replace_link(match):
            original_url = match.group(1)
            tracked_url = f"{base_url}/api/tracking/click/{draft_id}?url={original_url}"
            return f'href="{tracked_url}"'
        
        # Replace href attributes
        html_content = re.sub(r'href="([^"]+)"', replace_link, html_content)
        
        return html_content

