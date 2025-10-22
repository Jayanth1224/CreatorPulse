from typing import List, Dict, Optional
import re
import requests
from datetime import datetime
from urllib.parse import urlparse
import base64


class EmailTemplateService:
    """Service for generating professional HTML email templates for newsletters"""
    
    def __init__(self):
        self.base_template = self._get_base_template()
    
    def generate_newsletter_html(
        self,
        draft_content: str,
        bundle_name: str,
        bundle_color: str = "#3B82F6",
        entries: List[Dict] = None,
        include_images: bool = True
    ) -> str:
        """Generate complete HTML email template for newsletter"""
        
        # Extract structured content from draft
        structured_content = self._parse_draft_content(draft_content)
        
        # Get real articles (with source URLs)
        real_articles = self._get_real_articles(entries)
        
        # Get AI insights (without source URLs)
        ai_insights = self._get_ai_insights(structured_content)
        
        # Get trends section
        trends_section = self._get_trends_section(structured_content)
        
        # Generate stats
        stats = self._generate_stats(real_articles, bundle_name)
        
        # Build the complete HTML
        html_content = self.base_template.format(
            bundle_name=bundle_name,
            bundle_color=bundle_color,
            stats=stats,
            real_articles=real_articles,
            ai_insights=ai_insights,
            trends_section=trends_section,
            footer=self._get_footer()
        )
        
        return html_content
    
    def _get_base_template(self) -> str:
        """Get the base HTML email template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bundle_name} Newsletter</title>
    <style>
        /* Reset styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8fafc;
        }}
        
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, {bundle_color}, {bundle_color}dd);
            color: white;
            padding: 24px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        /* Stats bar */
        .stats {{
            background-color: #f1f5f9;
            padding: 16px 24px;
            border-bottom: 1px solid #e2e8f0;
            text-align: center;
            font-size: 14px;
            color: #64748b;
        }}
        
        /* Featured story */
        .featured-story {{
            padding: 24px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .featured-story h2 {{
            font-size: 24px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 12px;
        }}
        
        .featured-story .summary {{
            font-size: 16px;
            color: #475569;
            line-height: 1.6;
            margin-bottom: 16px;
        }}
        
        .featured-story .read-more {{
            display: inline-block;
            background-color: {bundle_color};
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            font-size: 14px;
        }}
        
        /* News items */
        .news-section {{
            padding: 24px;
        }}
        
        .news-section h3 {{
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            border-bottom: 2px solid {bundle_color};
            padding-bottom: 8px;
        }}
        
        .news-item {{
            display: flex;
            margin-bottom: 20px;
            padding: 16px;
            background-color: #f8fafc;
            border-radius: 8px;
            border-left: 4px solid {bundle_color};
        }}
        
        .news-item:last-child {{
            margin-bottom: 0;
        }}
        
        .news-item-image {{
            width: 80px;
            height: 80px;
            border-radius: 6px;
            object-fit: cover;
            margin-right: 16px;
            flex-shrink: 0;
        }}
        
        .news-item-content {{
            flex: 1;
        }}
        
        .news-item h4 {{
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 6px;
            line-height: 1.4;
        }}
        
        .news-item .summary {{
            font-size: 14px;
            color: #64748b;
            line-height: 1.5;
            margin-bottom: 8px;
        }}
        
        .news-item .meta {{
            font-size: 12px;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .news-item .read-more {{
            color: {bundle_color};
            text-decoration: none;
            font-weight: 500;
        }}
        
        /* Real Articles Section */
        .real-articles-section {{
            padding: 24px;
            background-color: #f8fafc;
        }}
        
        .real-articles-section h3 {{
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            border-bottom: 2px solid {bundle_color};
            padding-bottom: 8px;
        }}
        
        .article-item {{
            display: flex;
            margin-bottom: 20px;
            padding: 16px;
            background-color: white;
            border-radius: 8px;
            border-left: 4px solid {bundle_color};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .article-item:last-child {{
            margin-bottom: 0;
        }}
        
        .article-image {{
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 6px;
            margin-right: 16px;
            flex-shrink: 0;
        }}
        
        .article-content {{
            flex: 1;
        }}
        
        .article-content h4 {{
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 6px;
            line-height: 1.4;
        }}
        
        .article-content .summary {{
            font-size: 14px;
            color: #64748b;
            line-height: 1.5;
            margin-bottom: 8px;
        }}
        
        .article-content .meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .article-content .read-more {{
            color: {bundle_color};
            text-decoration: none;
            font-weight: 500;
        }}
        
        /* AI Insights Section */
        .insights-section {{
            padding: 24px;
            background-color: #fef7ff;
        }}
        
        .insights-section h3 {{
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            border-bottom: 2px solid #8b5cf6;
            padding-bottom: 8px;
        }}
        
        .insight-item {{
            margin-bottom: 16px;
            padding: 16px;
            background-color: white;
            border-radius: 8px;
            border-left: 4px solid #8b5cf6;
        }}
        
        .insight-item:last-child {{
            margin-bottom: 0;
        }}
        
        .insight-item h4 {{
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
        }}
        
        .insight-content {{
            font-size: 14px;
            color: #64748b;
            line-height: 1.6;
        }}
        
        /* Trends Section */
        .trends-section {{
            padding: 24px;
            background-color: #f0f9ff;
        }}
        
        .trends-section h3 {{
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            border-bottom: 2px solid #0ea5e9;
            padding-bottom: 8px;
        }}
        
        .trend-item {{
            margin-bottom: 12px;
            padding: 12px;
            background-color: white;
            border-radius: 6px;
            border-left: 3px solid #0ea5e9;
        }}
        
        .trend-item:last-child {{
            margin-bottom: 0;
        }}
        
        .trend-content {{
            font-size: 14px;
            color: #64748b;
            line-height: 1.5;
        }}
        
        /* No content states */
        .no-articles, .no-insights, .no-trends {{
            text-align: center;
            padding: 20px;
            color: #64748b;
            font-style: italic;
        }}
        
        /* Footer */
        .footer {{
            background-color: #1e293b;
            color: white;
            padding: 24px;
            text-align: center;
        }}
        
        .footer h4 {{
            font-size: 18px;
            margin-bottom: 12px;
        }}
        
        .footer p {{
            font-size: 14px;
            opacity: 0.8;
            margin-bottom: 16px;
        }}
        
        .social-links {{
            margin-bottom: 16px;
        }}
        
        .social-links a {{
            color: white;
            text-decoration: none;
            margin: 0 8px;
            font-size: 14px;
        }}
        
        .unsubscribe {{
            font-size: 12px;
            opacity: 0.6;
        }}
        
        /* Responsive */
        @media (max-width: 600px) {{
            .email-container {{
                margin: 0;
                border-radius: 0;
            }}
            
            .news-item {{
                flex-direction: column;
            }}
            
            .news-item-image {{
                width: 100%;
                height: 120px;
                margin-right: 0;
                margin-bottom: 12px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header">
            <h1>{bundle_name}</h1>
            <div class="subtitle">Your Daily News Digest</div>
        </div>
        
        <!-- Stats -->
        <div class="stats">
            {stats}
        </div>
        
        <!-- Real Articles Section -->
        <div class="real-articles-section">
            <h3>📰 Today's Top Stories</h3>
            {real_articles}
        </div>
        
        <!-- AI Insights Section -->
        <div class="insights-section">
            <h3>💡 Key Insights</h3>
            {ai_insights}
        </div>
        
        <!-- Trends Section -->
        <div class="trends-section">
            <h3>📈 Trends to Watch</h3>
            {trends_section}
        </div>
        
        <!-- Footer -->
        {footer}
    </div>
</body>
</html>
"""
    
    def _parse_draft_content(self, draft_content: str) -> Dict:
        """Parse draft content to extract structured information"""
        content = {
            "intro": "",
            "insights": [],
            "trends": []
        }
        
        # Extract intro
        intro_match = re.search(r'<div class="draft-intro">(.*?)</div>', draft_content, re.DOTALL)
        if intro_match:
            content["intro"] = self._clean_html(intro_match.group(1))
        
        # Extract insights
        insights_matches = re.findall(r'<div class="draft-insight">(.*?)</div>', draft_content, re.DOTALL)
        for insight in insights_matches:
            content["insights"].append(self._clean_html(insight))
        
        # Extract trends
        trends_match = re.search(r'<div class="draft-trends">(.*?)</div>', draft_content, re.DOTALL)
        if trends_match:
            content["trends"] = self._extract_trends(trends_match.group(1))
        
        return content
    
    def _get_real_articles(self, entries: List[Dict]) -> str:
        """Generate real articles section with working Read More links"""
        if not entries:
            return """
            <div class="no-articles">
                <p>No articles available at the moment. Check back later for the latest updates.</p>
            </div>
            """
        
        articles_html = []
        for i, entry in enumerate(entries[:5]):  # Limit to 5 real articles
            if entry.get('link') and entry.get('link') != '#':
                # Get image if available
                image_url = self._get_image_for_content(entry.get('title', ''), entry.get('summary', ''))
                image_html = f'<img src="{image_url}" alt="{entry.get("title", "")}" class="article-image">' if image_url else ''
                
                # Get the actual article content (summary or description)
                article_content = entry.get('summary', '') or entry.get('description', '')
                
                # Clean HTML tags and get first couple of lines
                import re
                clean_content = re.sub(r'<[^>]+>', '', article_content)
                clean_content = clean_content.strip()
                
                # Show first 2-3 lines of actual content
                content_lines = clean_content.split('\n')[:2]
                display_content = ' '.join(content_lines)[:300]  # Limit to ~300 chars
                
                articles_html.append(f"""
                <div class="article-item">
                    {image_html}
                    <div class="article-content">
                        <h4>{entry.get('title', f'Article {i+1}')}</h4>
                        <div class="summary">{display_content}...</div>
                        <div class="meta">
                            <a href="{entry.get('link')}" class="read-more">Read Full Article →</a>
                        </div>
                    </div>
                </div>
                """)
        
        return ''.join(articles_html) if articles_html else """
        <div class="no-articles">
            <p>No articles with valid sources available at the moment.</p>
        </div>
        """
    
    def _get_ai_insights(self, structured_content: Dict) -> str:
        """Generate AI insights section without fake Read More links"""
        insights = structured_content.get("insights", [])
        if not insights:
            return """
            <div class="no-insights">
                <p>No insights available at the moment.</p>
            </div>
            """
        
        insights_html = []
        for i, insight in enumerate(insights[:3]):  # Limit to 3 insights
            title_match = re.search(r'<h3>(.*?)</h3>', insight)
            content_match = re.search(r'<p>(.*?)</p>', insight)
            
            title = title_match.group(1) if title_match else f"Insight {i+1}"
            content = content_match.group(1) if content_match else insight
            
            insights_html.append(f"""
            <div class="insight-item">
                <h4>{title}</h4>
                <div class="insight-content">{content}</div>
            </div>
            """)
        
        return ''.join(insights_html)
    
    def _get_trends_section(self, structured_content: Dict) -> str:
        """Generate trends section without links"""
        trends = structured_content.get("trends", [])
        if not trends:
            return """
            <div class="no-trends">
                <p>No trend analysis available at the moment.</p>
            </div>
            """
        
        trends_html = []
        for trend in trends[:3]:  # Limit to 3 trends
            trends_html.append(f"""
            <div class="trend-item">
                <div class="trend-content">{trend}</div>
            </div>
            """)
        
        return ''.join(trends_html)
    
    def _get_featured_story(self, structured_content: Dict, entries: List[Dict]) -> str:
        """Generate featured story section"""
        if structured_content["insights"]:
            # Use first insight as featured story
            insight = structured_content["insights"][0]
            title_match = re.search(r'<h3>(.*?)</h3>', insight)
            content_match = re.search(r'<p>(.*?)</p>', insight)
            
            title = title_match.group(1) if title_match else "Featured Story"
            content = content_match.group(1) if content_match else insight
            
            return f"""
            <div class="featured-story">
                <h2>{title}</h2>
                <div class="summary">{content}</div>
                <a href="#" class="read-more">Read Full Story →</a>
            </div>
            """
        elif entries:
            # Use first entry as featured story
            entry = entries[0]
            link_url = entry.get('link', '#')
            # Only show read more link if we have a real URL
            read_more_link = f'<a href="{link_url}" class="read-more">Read Full Story →</a>' if link_url and link_url != '#' else ''
            return f"""
            <div class="featured-story">
                <h2>{entry.get('title', 'Featured Story')}</h2>
                <div class="summary">{entry.get('summary', '')[:200]}...</div>
                {read_more_link}
            </div>
            """
        else:
            return """
            <div class="featured-story">
                <h2>Today's Featured Story</h2>
                <div class="summary">Stay tuned for the latest developments in your industry.</div>
                <a href="#" class="read-more">Read More →</a>
            </div>
            """
    
    def _get_news_items(self, structured_content: Dict, entries: List[Dict]) -> str:
        """Generate news items section"""
        news_items = []
        
        # Use insights as news items
        for i, insight in enumerate(structured_content["insights"][:5]):
            title_match = re.search(r'<h3>(.*?)</h3>', insight)
            content_match = re.search(r'<p>(.*?)</p>', insight)
            
            title = title_match.group(1) if title_match else f"Story {i+1}"
            content = content_match.group(1) if content_match else insight
            
            # Get image if available
            image_url = self._get_image_for_content(title, content)
            image_html = f'<img src="{image_url}" alt="{title}" class="news-item-image">' if image_url else ''
            
            news_items.append(f"""
            <div class="news-item">
                {image_html}
                <div class="news-item-content">
                    <h4>{title}</h4>
                    <div class="summary">{content[:150]}...</div>
                    <div class="meta">
                        <span>2 min read</span>
                        <a href="#" class="read-more">Read More →</a>
                    </div>
                </div>
            </div>
            """)
        
        # Add entries as news items if we have them
        if entries and len(news_items) < 5:
            for entry in entries[:5-len(news_items)]:
                image_url = self._get_image_for_entry(entry)
                image_html = f'<img src="{image_url}" alt="{entry.get("title", "")}" class="news-item-image">' if image_url else ''
                
                news_items.append(f"""
                <div class="news-item">
                    {image_html}
                    <div class="news-item-content">
                        <h4>{entry.get('title', 'Untitled')}</h4>
                        <div class="summary">{entry.get('summary', '')[:150]}...</div>
                        <div class="meta">
                            <span>{self._format_date(entry.get('published'))}</span>
                            <a href="{entry.get('link', '#')}" class="read-more">Read More →</a>
                        </div>
                    </div>
                </div>
                """)
        
        return "\n".join(news_items)
    
    def _generate_stats(self, news_items: str, bundle_name: str) -> str:
        """Generate stats section"""
        item_count = news_items.count('class="news-item"')
        return f"📰 {item_count} stories today from {bundle_name} • {datetime.now().strftime('%B %d, %Y')}"
    
    def _get_image_for_content(self, title: str, content: str) -> Optional[str]:
        """Get image URL for content (placeholder for now)"""
        # In a real implementation, you'd extract images from the source articles
        # For now, return a placeholder gradient
        return self._generate_placeholder_image(title)
    
    def _get_image_for_entry(self, entry: Dict) -> Optional[str]:
        """Get image URL for RSS entry"""
        # Try to extract image from entry
        if 'image' in entry:
            return entry['image']
        
        # Try to extract from summary HTML
        summary = entry.get('summary', '')
        img_match = re.search(r'<img[^>]+src="([^"]+)"', summary)
        if img_match:
            return img_match.group(1)
        
        # Return placeholder
        return self._generate_placeholder_image(entry.get('title', ''))
    
    def _generate_placeholder_image(self, text: str) -> str:
        """Generate a placeholder gradient image"""
        # Create a simple gradient as data URL
        colors = ['#3B82F6', '#8B5CF6', '#06B6D4', '#10B981', '#F59E0B']
        color = colors[hash(text) % len(colors)]
        
        # Simple gradient SVG as data URL
        svg = f"""
        <svg width="80" height="80" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color}88;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="80" height="80" fill="url(#grad)" rx="6"/>
        </svg>
        """
        
        return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"
    
    def _get_footer(self) -> str:
        """Generate footer section"""
        return """
        <div class="footer">
            <h4>CreatorPulse</h4>
            <p>Your AI-powered newsletter companion</p>
            <div class="social-links">
                <a href="#">Twitter</a>
                <a href="#">LinkedIn</a>
                <a href="#">Website</a>
            </div>
            <div class="unsubscribe">
                <a href="#">Unsubscribe</a> | <a href="#">Update Preferences</a>
            </div>
        </div>
        """
    
    def _clean_html(self, html: str) -> str:
        """Clean HTML content"""
        # Remove HTML tags but keep content
        clean = re.sub(r'<[^>]+>', '', html)
        return clean.strip()
    
    def _extract_trends(self, trends_html: str) -> List[str]:
        """Extract trends from HTML"""
        trends = []
        li_matches = re.findall(r'<li>(.*?)</li>', trends_html)
        for trend in li_matches:
            trends.append(self._clean_html(trend))
        return trends
    
    def _format_date(self, date) -> str:
        """Format date for display"""
        if not date:
            return "Today"
        
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except:
                return "Today"
        
        if isinstance(date, datetime):
            now = datetime.now()
            diff = now - date
            
            if diff.days == 0:
                return "Today"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                return date.strftime("%b %d")
        
        return "Today"
