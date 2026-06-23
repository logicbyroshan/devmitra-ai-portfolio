# ai/utils.py
from portfolio.models import SiteConfiguration, FAQ
from ai.models import AIContext
import re

def clean_html_content(html_content):
    """Remove HTML tags from content"""
    if not html_content:
        return ""
    return re.sub(r'<[^>]+>', '', html_content).strip()

def format_context_as_markdown(context_data):
    """
    Convert context data to properly formatted markdown for Gemini
    """
    markdown_content = "# Roshan Damor - Personal Assistant Context\n\n"
    
    # Add basic info
    if 'name' in context_data:
        markdown_content += f"**Name:** {context_data['name']}\n\n"
    
    if 'bio' in context_data:
        markdown_content += f"**Bio:** {context_data['bio']}\n\n"
    
    if 'email' in context_data:
        markdown_content += f"**Contact Email:** {context_data['email']}\n\n"
    
    # Add FAQs if available
    if 'faqs' in context_data and context_data['faqs']:
        markdown_content += "## Frequently Asked Questions\n\n"
        for faq in context_data['faqs']:
            markdown_content += f"**Q: {faq['question']}**\n\n"
            markdown_content += f"A: {faq['answer']}\n\n"
        markdown_content += "---\n\n"
    
    # Add custom AI context
    if 'ai_contexts' in context_data and context_data['ai_contexts']:
        markdown_content += "## Additional Context About Roshan\n\n"
        for context in context_data['ai_contexts']:
            markdown_content += f"### {context['title']}\n\n"
            markdown_content += f"{context['content']}\n\n"
        markdown_content += "---\n\n"
    
    return markdown_content

def get_portfolio_context():
    """
    Gathers personal context about Roshan Damor for AI responses.
    Focuses only on personal information, FAQs, and custom AI context.
    """
    try:
        context_data = {}
        
        # Get site configuration for basic info
        config = SiteConfiguration.objects.first()
        
        context_data['name'] = "Roshan Damor"
        if config:
            context_data['bio'] = 'Full-Stack Developer and AI Enthusiast'
            context_data['email'] = config.email or 'contact@roshandamor.me'
        else:
            context_data['bio'] = 'Full-Stack Developer and AI Enthusiast'
            context_data['email'] = 'contact@roshandamor.me'
        
        # Get FAQs
        faqs = FAQ.objects.all()[:10]
        if faqs.exists():
            context_data['faqs'] = []
            for faq in faqs:
                context_data['faqs'].append({
                    'question': faq.question,
                    'answer': clean_html_content(faq.answer)
                })
        
        # Get custom AI context
        ai_contexts = AIContext.objects.filter(is_active=True).order_by('title')
        if ai_contexts.exists():
            context_data['ai_contexts'] = []
            for ai_context in ai_contexts:
                context_data['ai_contexts'].append({
                    'title': ai_context.title,
                    'content': ai_context.content
                })
        
        # Convert to markdown format
        return format_context_as_markdown(context_data)
        
    except Exception as e:
        # Fallback context in markdown format
        return f"""# Roshan Damor - Personal Assistant Context

**Name:** Roshan Damor
**Bio:** Full-Stack Developer and AI Enthusiast  
**Contact Email:** contact@roshandamor.me

**NOTE:** Could not load complete personal data - {str(e)}
"""
