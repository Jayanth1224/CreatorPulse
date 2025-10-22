from typing import Dict, List, Optional
import re


class ContentExtractorService:
    """Service for extracting editable content from email templates"""
    
    def extract_editable_content(self, full_email_html: str) -> str:
        """Extract just the editable content sections from the full email template"""
        
        # Extract the main content sections that users should be able to edit
        content_sections = []
        
        # Extract featured story
        featured_story = self._extract_featured_story(full_email_html)
        if featured_story:
            content_sections.append(featured_story)
        
        # Extract news items
        news_items = self._extract_news_items(full_email_html)
        if news_items:
            content_sections.append(news_items)
        
        # If no structured content found, try to extract from the original draft format
        if not content_sections:
            content_sections = self._extract_from_draft_format(full_email_html)
        
        # Combine all sections
        if content_sections:
            return "\n\n".join(content_sections)
        else:
            # Fallback: return a simple structure
            return self._create_fallback_content()
    
    def _extract_featured_story(self, html: str) -> Optional[str]:
        """Extract featured story section"""
        featured_match = re.search(
            r'<div class="featured-story">(.*?)</div>', 
            html, 
            re.DOTALL
        )
        
        if featured_match:
            featured_html = featured_match.group(1)
            
            # Extract title
            title_match = re.search(r'<h2>(.*?)</h2>', featured_html)
            title = title_match.group(1) if title_match else "Featured Story"
            
            # Extract content
            content_match = re.search(r'<div class="summary">(.*?)</div>', featured_html)
            content = content_match.group(1) if content_match else ""
            
            return f"""
            <div class="draft-featured">
                <h2>{title}</h2>
                <p>{content}</p>
            </div>
            """
        
        return None
    
    def _extract_news_items(self, html: str) -> Optional[str]:
        """Extract news items section"""
        news_section_match = re.search(
            r'<div class="news-section">(.*?)</div>', 
            html, 
            re.DOTALL
        )
        
        if news_section_match:
            news_html = news_section_match.group(1)
            
            # Extract individual news items
            news_items = re.findall(
                r'<div class="news-item">(.*?)</div>', 
                news_html, 
                re.DOTALL
            )
            
            if news_items:
                items_html = []
                for i, item in enumerate(news_items[:5]):  # Limit to 5 items
                    # Extract title
                    title_match = re.search(r'<h4>(.*?)</h4>', item)
                    title = title_match.group(1) if title_match else f"Story {i+1}"
                    
                    # Extract summary
                    summary_match = re.search(r'<div class="summary">(.*?)</div>', item)
                    summary = summary_match.group(1) if summary_match else ""
                    
                    items_html.append(f"""
                    <div class="draft-insight">
                        <h3>{title}</h3>
                        <p>{summary}</p>
                    </div>
                    """)
                
                return "\n".join(items_html)
        
        return None
    
    def _extract_from_draft_format(self, html: str) -> List[str]:
        """Extract content from original draft format (draft-intro, draft-insight, etc.)"""
        content_sections = []
        
        # First, try to extract from the hidden draft-content div
        draft_content_match = re.search(r'<div style="display: none;" class="draft-content">(.*?)</div>', html, re.DOTALL)
        if not draft_content_match:
            # Try alternative pattern
            draft_content_match = re.search(r'<div class="draft-content"[^>]*>(.*?)</div>', html, re.DOTALL)
        
        if draft_content_match:
            draft_content = draft_content_match.group(1)
            print(f"🔍 Found draft content: {len(draft_content)} chars")
            # Extract sections from the draft content
            content_sections = self._extract_draft_sections(draft_content)
            if content_sections:
                print(f"✅ Extracted {len(content_sections)} draft sections")
                return content_sections
            else:
                print("❌ No sections found in draft content")
        else:
            print("❌ No draft-content div found")
        
        # Fallback: extract directly from the HTML
        # Extract intro
        intro_match = re.search(r'<div class="draft-intro">(.*?)</div>', html, re.DOTALL)
        if intro_match:
            content_sections.append(intro_match.group(1))
        
        # Extract insights
        insights = re.findall(r'<div class="draft-insight">(.*?)</div>', html, re.DOTALL)
        for insight in insights:
            content_sections.append(f'<div class="draft-insight">{insight}</div>')
        
        # Extract trends
        trends_match = re.search(r'<div class="draft-trends">(.*?)</div>', html, re.DOTALL)
        if trends_match:
            content_sections.append(trends_match.group(1))
        
        return content_sections
    
    def _extract_draft_sections(self, draft_content: str) -> List[str]:
        """Extract sections from draft content"""
        content_sections = []
        
        # Extract intro
        intro_match = re.search(r'<div class="draft-intro">(.*?)</div>', draft_content, re.DOTALL)
        if intro_match:
            content_sections.append(intro_match.group(1))
        
        # Extract insights
        insights = re.findall(r'<div class="draft-insight">(.*?)</div>', draft_content, re.DOTALL)
        for insight in insights:
            content_sections.append(f'<div class="draft-insight">{insight}</div>')
        
        # Extract trends
        trends_match = re.search(r'<div class="draft-trends">(.*?)</div>', draft_content, re.DOTALL)
        if trends_match:
            content_sections.append(trends_match.group(1))
        
        return content_sections
    
    def _create_fallback_content(self) -> str:
        """Create fallback content if extraction fails"""
        return """
        <div class="draft-intro">
            <h2>Your Newsletter</h2>
            <p>Welcome to your curated news digest.</p>
        </div>
        
        <div class="draft-insight">
            <h3>Featured Story</h3>
            <p>Add your featured story content here.</p>
        </div>
        
        <div class="draft-trends">
            <h3>Trends to Watch</h3>
            <ul>
                <li>Key trend 1</li>
                <li>Key trend 2</li>
                <li>Key trend 3</li>
            </ul>
        </div>
        """
    
    def get_preview_html(self, full_email_html: str) -> str:
        """Get the full email template for preview"""
        return full_email_html
    
    def get_editable_html(self, full_email_html: str) -> str:
        """Get just the editable content for the editor"""
        return self.extract_editable_content(full_email_html)
