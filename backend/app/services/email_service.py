from typing import List, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, TrackingSettings, ClickTracking, OpenTracking
from app.config import settings
from app.services.email_renderer_service import EmailRendererService
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re


class EmailService:
    """Email service for sending newsletters via SendGrid or SMTP"""
    
    def __init__(self):
        self.sendgrid_api_key = getattr(settings, 'sendgrid_api_key', None) or ""
        self.smtp_host = getattr(settings, 'smtp_host', None) or ""
        self.smtp_port = getattr(settings, 'smtp_port', 587)
        self.smtp_username = getattr(settings, 'smtp_username', None) or ""
        self.smtp_password = getattr(settings, 'smtp_password', None) or ""
        self.from_email = getattr(settings, 'from_email', 'noreply@creatorpulse.com')
        self.from_name = getattr(settings, 'from_name', 'CreatorPulse')
        self.renderer_service = EmailRendererService()
    
    async def send_newsletter(
        self,
        recipients: List[str],
        subject: str,
        html_content: str,
        draft_id: str,
        use_sendgrid: bool = True
    ) -> dict:
        """Send newsletter to recipients with tracking"""
        
        # Insert tracking pixel for open tracking
        tracking_pixel = self._generate_tracking_pixel(draft_id)
        html_with_tracking = html_content + tracking_pixel
        
        # Wrap links for click tracking
        html_with_links = self._wrap_links(html_with_tracking, draft_id)
        
        if use_sendgrid and self.sendgrid_api_key:
            return await self._send_via_sendgrid(recipients, subject, html_with_links)
        elif self.smtp_host:
            return await self._send_via_smtp(recipients, subject, html_with_links)
        else:
            # Fallback: simulate sending
            print(f"[EMAIL] Simulating send to {len(recipients)} recipients")
            print(f"[EMAIL] Subject: {subject}")
            print(f"[EMAIL] Draft ID: {draft_id}")
            
            return {
                "success": True,
                "recipients_count": len(recipients),
                "message_id": f"simulated-{draft_id}",
                "method": "simulated"
            }
    
    async def send_newsletter_with_tokens(
        self,
        recipients_with_tokens: List[dict],
        subject: str,
        html_content: str,
        draft_id: str,
        use_sendgrid: bool = True
    ) -> dict:
        """Send newsletter to recipients with per-recipient token tracking"""
        
        if use_sendgrid and self.sendgrid_api_key:
            return await self._send_via_sendgrid_with_tokens(recipients_with_tokens, subject, html_content, draft_id)
        elif self.smtp_host:
            return await self._send_via_smtp_with_tokens(recipients_with_tokens, subject, html_content, draft_id)
        else:
            # Fallback: simulate sending
            print(f"[EMAIL] Simulating send to {len(recipients_with_tokens)} recipients")
            print(f"[EMAIL] Subject: {subject}")
            print(f"[EMAIL] Draft ID: {draft_id}")
            
            return {
                "success": True,
                "recipients_count": len(recipients_with_tokens),
                "message_id": f"simulated-{draft_id}",
                "method": "simulated"
            }
    
    async def _send_via_sendgrid(
        self,
        recipients: List[str],
        subject: str,
        html_content: str
    ) -> dict:
        """Send email via SendGrid"""
        try:
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=recipients,
                subject=subject,
                html_content=html_content
            )
            
            # Enable tracking
            message.tracking_settings = TrackingSettings()
            message.tracking_settings.click_tracking = ClickTracking(True, True)
            message.tracking_settings.open_tracking = OpenTracking(True)
            
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = sg.send(message)
            
            return {
                "success": True,
                "recipients_count": len(recipients),
                "message_id": response.headers.get('X-Message-Id'),
                "method": "sendgrid"
            }
        
        except Exception as e:
            print(f"[EMAIL ERROR] SendGrid send failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "method": "sendgrid"
            }
    
    async def _send_via_smtp(
        self,
        recipients: List[str],
        subject: str,
        html_content: str
    ) -> dict:
        """Send email via SMTP"""
        try:
            sent_count = 0
            
            for recipient in recipients:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"{self.from_name} <{self.from_email}>"
                msg['To'] = recipient
                
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
                
                # Send via SMTP
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
                    sent_count += 1
            
            return {
                "success": True,
                "recipients_count": sent_count,
                "message_id": f"smtp-{hash(subject)}",
                "method": "smtp"
            }
        
        except Exception as e:
            print(f"[EMAIL ERROR] SMTP send failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "method": "smtp"
            }
    
    async def _send_via_smtp_with_tokens(
        self,
        recipients_with_tokens: List[dict],
        subject: str,
        html_content: str,
        draft_id: str
    ) -> dict:
        """Send email via SMTP with per-recipient token tracking"""
        try:
            sent_count = 0
            
            for recipient_data in recipients_with_tokens:
                recipient = recipient_data["email"]
                token = recipient_data["token"]
                
                # Generate personalized tracking for this recipient
                tracking_pixel = self._generate_tracking_pixel(draft_id, token)
                html_with_tracking = html_content + tracking_pixel
                html_with_links = self._wrap_links(html_with_tracking, draft_id, token)
                
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f"{self.from_name} <{self.from_email}>"
                msg['To'] = recipient
                
                html_part = MIMEText(html_with_links, 'html')
                msg.attach(html_part)
                
                # Send via SMTP
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
                    sent_count += 1
            
            return {
                "success": True,
                "recipients_count": sent_count,
                "message_id": f"smtp-{hash(subject)}",
                "method": "smtp"
            }
        
        except Exception as e:
            print(f"[EMAIL ERROR] SMTP send failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "method": "smtp"
            }
    
    def _generate_tracking_pixel(self, draft_id: str, token: str = None) -> str:
        """Generate tracking pixel HTML for open tracking"""
        from app.config import settings
        token_param = f"?token={token}" if token else ""
        tracking_url = f"{settings.api_base_url}/api/analytics/track/open/{draft_id}{token_param}"
        return f'<img src="{tracking_url}" width="1" height="1" style="display:none;" alt="" />'
    
    def _wrap_links(self, html_content: str, draft_id: str, token: str = None) -> str:
        """Wrap all links for click tracking"""
        from app.config import settings
        # Find all href attributes in anchor tags
        def replace_link(match):
            original_url = match.group(1)
            # Skip tracking for certain URLs
            if original_url.startswith('#') or original_url.startswith('mailto:') or original_url.startswith('tel:'):
                return f'href="{original_url}"'
            # Create tracking URL
            token_param = f"&token={token}" if token else ""
            tracking_url = f"{settings.api_base_url}/api/analytics/track/click/{draft_id}?url={original_url}{token_param}"
            return f'href="{tracking_url}"'
        
        # Replace all href attributes
        wrapped_html = re.sub(r'href="([^"]+)"', replace_link, html_content)
        return wrapped_html
    
    async def send_test_email(
        self,
        recipient: str,
        html_content: str,
        subject: str = "Test Email from CreatorPulse"
    ) -> dict:
        """Send a test email"""
        print(f"[EMAIL] Sending test email to {recipient}")
        
        if self.sendgrid_api_key:
            return await self._send_via_sendgrid([recipient], subject, html_content)
        elif self.smtp_host:
            return await self._send_via_smtp([recipient], subject, html_content)
        else:
            return {
                "success": True,
                "message": "Test email simulated (no email provider configured)",
                "method": "simulated"
            }
    
    async def get_draft_preview(
        self,
        draft_id: str,
        custom_bundle_color: str = None
    ) -> dict:
        """Get preview of draft as rendered email"""
        return await self.renderer_service.render_preview(
            draft_id=draft_id,
            custom_bundle_color=custom_bundle_color
        )