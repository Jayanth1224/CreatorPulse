from openai import OpenAI
from typing import List, Dict
from app.config import settings


class AIService:
    """Service for Openrouter API interactions (OpenAI-compatible)"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = settings.openrouter_model  # Default: z-ai/glm-4.5-air:free
    
    async def generate_newsletter_draft(
        self,
        entries: List[Dict],
        tone: str = "professional",
        topic: str = None,
        bundle_name: str = "Tech News",
        voice_samples: List[Dict] = None
    ) -> str:
        """Generate a newsletter draft from RSS entries"""
        
        # Build system prompt with optional voice training
        system_prompt = self._build_system_prompt(tone, voice_samples)
        
        # Build user prompt with entries
        user_prompt = self._build_user_prompt(entries, topic, bundle_name)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                timeout=30  # 30 second timeout
            )
            
            content = response.choices[0].message.content
            
            # Convert markdown to HTML if needed
            html_content = self._format_as_html(content)
            
            return html_content
        
        except Exception as e:
            print(f"Error generating draft: {str(e)}")
            # Return fallback content
            return self._generate_fallback_content(entries, bundle_name)
    
    async def regenerate_section(
        self,
        section_type: str,
        current_content: str,
        entries: List[Dict],
        tone: str = "professional",
        voice_samples: List[Dict] = None
    ) -> str:
        """Regenerate a specific section of the newsletter"""
        
        system_prompt = self._build_system_prompt(tone, voice_samples)
        system_prompt += f"\n\nRegenerate only the {section_type} section of the newsletter."
        
        user_prompt = f"""
Current {section_type} section:
{current_content}

Based on these articles:
{self._format_entries_for_prompt(entries[:5])}

Generate a new, different version of the {section_type} section. Keep it concise and engaging.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error regenerating section: {str(e)}")
            return current_content
    
    def _build_system_prompt(self, tone: str, voice_samples: List[Dict] = None) -> str:
        """Build system prompt based on tone and optional voice training samples"""
        tone_descriptions = {
            "professional": "formal, authoritative, and business-oriented",
            "conversational": "casual, friendly, and approachable",
            "analytical": "data-driven, precise, and detailed",
            "friendly": "warm, engaging, and personal"
        }
        
        tone_desc = tone_descriptions.get(tone, "professional and informative")
        
        base_prompt = f"""You are an expert newsletter writer specializing in curating and summarizing content. 
Your writing style is {tone_desc}."""
        
        # Add voice training examples if available
        if voice_samples and len(voice_samples) >= 3:
            voice_examples = self._build_voice_examples_section(voice_samples)
            base_prompt += f"\n\n{voice_examples}"
        
        base_prompt += """

Generate a well-structured newsletter draft with:
1. An engaging intro paragraph (2-3 sentences)
2. 3-5 key insights, each as a separate section with a heading and 2-3 sentences
3. A "Trends to Watch" section with 3-4 bullet points
4. Keep the total length to 250-400 words

Format the output as clean HTML using <div>, <h2>, <h3>, <p>, and <ul>/<li> tags.
Use class names: draft-intro, draft-insight, draft-trends."""
        
        return base_prompt
    
    def _build_voice_examples_section(self, voice_samples: List[Dict]) -> str:
        """Build voice training examples section for system prompt"""
        
        # Take the best 3-5 samples (most recent and diverse)
        selected_samples = voice_samples[:5]
        
        examples_text = "Here are examples of my writing style to match:\n\n"
        
        for i, sample in enumerate(selected_samples, 1):
            # Truncate long samples to keep prompt manageable (max 800 chars per sample)
            content = sample.get('content', '')
            if len(content) > 800:
                content = content[:800] + "..."
            
            title = sample.get('title', f'Example {i}')
            examples_text += f"Example {i} ({title}):\n{content}\n\n"
        
        examples_text += "Match this writing style, tone, voice, and approach in your newsletter generation. Pay attention to:\n"
        examples_text += "- Sentence structure and flow\n"
        examples_text += "- Vocabulary choices and tone\n"
        examples_text += "- How ideas are introduced and connected\n"
        examples_text += "- Overall writing personality and voice"
        
        return examples_text
    
    def _build_user_prompt(self, entries: List[Dict], topic: str, bundle_name: str) -> str:
        """Build user prompt with RSS entries"""
        entries_text = self._format_entries_for_prompt(entries[:15])
        
        topic_context = f" with a focus on {topic}" if topic else ""
        
        return f"""Generate a newsletter draft for "{bundle_name}"{topic_context}.

Here are the latest articles and posts:

{entries_text}

Create a cohesive newsletter that highlights the most important developments and trends."""
    
    def _format_entries_for_prompt(self, entries: List[Dict]) -> str:
        """Format RSS entries for the prompt"""
        formatted = []
        
        for i, entry in enumerate(entries, 1):
            formatted.append(
                f"{i}. {entry.get('title', 'Untitled')}\n"
                f"   {entry.get('summary', 'No summary')[:200]}...\n"
                f"   Source: {entry.get('link', '')}\n"
            )
        
        return "\n".join(formatted)
    
    def _format_as_html(self, content: str) -> str:
        """Convert markdown or plain text to HTML"""
        # Simple conversion - in production, use a proper markdown parser
        if "<div" in content or "<p>" in content:
            return content  # Already HTML
        
        # Basic markdown to HTML conversion
        lines = content.split("\n")
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("# "):
                html_lines.append(f"<h2>{line[2:]}</h2>")
            elif line.startswith("## "):
                html_lines.append(f"<h3>{line[3:]}</h3>")
            elif line.startswith("- "):
                html_lines.append(f"<li>{line[2:]}</li>")
            else:
                html_lines.append(f"<p>{line}</p>")
        
        return "\n".join(html_lines)
    
    def _generate_fallback_content(self, entries: List[Dict], bundle_name: str) -> str:
        """Generate simple fallback content if AI fails"""
        insights_html = ""
        
        for i, entry in enumerate(entries[:3], 1):
            insights_html += f"""
<div class="draft-insight">
    <h3>{entry.get('title', 'Untitled')}</h3>
    <p>{entry.get('summary', 'No summary available.')[:150]}...</p>
</div>
"""
        
        return f"""
<div class="draft-intro">
    <h2>This Week in {bundle_name}</h2>
    <p>Here's a curated roundup of the latest developments and insights from across the industry.</p>
</div>

{insights_html}

<div class="draft-trends">
    <h3>Trends to Watch</h3>
    <ul>
        <li>Emerging patterns in the space</li>
        <li>Key developments to monitor</li>
        <li>Future opportunities</li>
    </ul>
</div>
"""

