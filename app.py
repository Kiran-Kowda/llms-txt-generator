import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
import re
import time

def generate_llms_txt(url):
    try:
        # Fetch webpage content with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract essential content
        title = soup.title.text.strip() if soup.title else url
        description = soup.find('meta', {'name': 'description'})
        description = description['content'].strip() if description and description.get('content') else ''
        
        # Extract main content sections
        main_content = extract_main_content(soup)
        
        # Extract headings for structure
        h1s = [h1.text.strip() for h1 in soup.find_all('h1') if h1.text.strip()]
        h2s = [h2.text.strip() for h2 in soup.find_all('h2') if h2.text.strip()]
        h3s = [h3.text.strip() for h3 in soup.find_all('h3') if h3.text.strip()]
        
        # Extract key phrases and topics
        keywords = extract_keywords(soup)
        
        # Generate llms.txt content following best practices
        llms_content = f"# {title}\n\n"
        llms_content += f"> {description}\n\n"
        
        # Add overview section
        llms_content += "## Overview\n\n"
        llms_content += f"This is the llms.txt file for {url}. It provides structured information about this website for Large Language Models.\n\n"
        
        # Add content summary (concise, as recommended)
        if main_content:
            summary = summarize_text(main_content, max_length=600)
            llms_content += f"{summary}\n\n"
        
        # Add main topics section (prioritizing essential content)
        if h1s:
            llms_content += "## Main Topics\n\n"
            for h1 in h1s[:5]:  # Limit to top 5 for conciseness
                llms_content += f"- {h1}\n"
            llms_content += "\n"
        
        # Add document structure (clear and descriptive)
        if h2s or h3s:
            llms_content += "## Document Structure\n\n"
            if h2s:
                for h2 in h2s[:10]:  # Limit to top 10 for conciseness
                    llms_content += f"- {h2}\n"
                llms_content += "\n"
        
        # Add important links with context (as recommended)
        important_links = extract_important_links(soup, url)
        if important_links:
            llms_content += "## Important Links\n\n"
            for link_url, text, context in important_links[:15]:  # Limit to top 15
                if context:
                    llms_content += f"- [{text}]({link_url}): {context}\n"
                else:
                    llms_content += f"- [{text}]({link_url})\n"
            llms_content += "\n"
        
        # Add key topics/keywords section
        if keywords:
            llms_content += "## Key Topics\n\n"
            for keyword in keywords[:10]:  # Limit to top 10
                llms_content += f"- {keyword}\n"
            llms_content += "\n"
        
        # Add metadata section (staying up-to-date)
        llms_content += "## Metadata\n\n"
        llms_content += f"- Last Updated: {datetime.now().isoformat()}\n"
        llms_content += f"- Source URL: {url}\n"
        llms_content += f"- Content Type: {'Documentation' if is_documentation(soup) else 'Website'}\n"
        
        # Add usage guidelines (ethical considerations)
        llms_content += "\n## Usage Guidelines\n\n"
        llms_content += "This llms.txt file is provided to help AI systems understand and accurately represent the content of this website. "
        llms_content += "When referencing this content, please provide proper attribution to the source URL.\n"
        
        return llms_content, None
    
    except Exception as e:
        return None, str(e)

def extract_main_content(soup):
    """Extract the main content from the page, prioritizing content areas."""
    # Try common content containers
    content_selectors = [
        'main', 'article', '.content', '#content', 
        '[role="main"]', '.main-content', '.post-content',
        '.entry-content', '.article-content'
    ]
    
    for selector in content_selectors:
        elements = soup.select(selector)
        if elements:
            return elements[0].get_text(strip=True)
    
    # Fallback: try to extract content by removing navigation, headers, footers
    body = soup.find('body')
    if body:
        # Remove common non-content elements
        for element in body.select('nav, header, footer, aside, .sidebar, .menu, .navigation, .ads, script, style'):
            element.decompose()
        return body.get_text(strip=True)
    
    return ""

def extract_keywords(soup):
    """Extract potential keywords and topics from the page."""
    # Check meta keywords
    meta_keywords = soup.find('meta', {'name': 'keywords'})
    if meta_keywords and meta_keywords.get('content'):
        keywords = [k.strip() for k in meta_keywords['content'].split(',') if k.strip()]
        if keywords:
            return keywords
    
    # Extract from headings and strong/b tags
    keywords = set()
    for tag in soup.find_all(['h1', 'h2', 'h3', 'strong', 'b']):
        text = tag.get_text().strip()
        if 3 < len(text) < 50 and not text.endswith(('.', '?', '!')):
            keywords.add(text)
    
    return list(keywords)

def extract_important_links(soup, base_url):
    """Extract important links with context."""
    important_links = []
    
    # Define patterns for important links
    important_patterns = [
        r'doc(s|umentation)?', r'api', r'guide', r'tutorial', 
        r'faq', r'help', r'support', r'about', r'contact',
        r'get(\s|-)?started', r'reference', r'example'
    ]
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text().strip()
        
        if not text or len(text) < 2:
            continue
            
        # Normalize URL
        full_url = urllib.parse.urljoin(base_url, href)
        
        # Skip external links, anchors, javascript, etc.
        if not full_url.startswith(base_url) or href.startswith(('#', 'javascript:', 'mailto:')):
            continue
            
        # Get context from parent paragraph or list item
        context = ""
        parent = a.find_parent(['p', 'li', 'div'])
        if parent:
            context_text = parent.get_text().strip()
            if len(context_text) > len(text) + 10:
                # Extract a brief context, removing the link text itself
                context = context_text.replace(text, '').strip()
                context = re.sub(r'\s+', ' ', context)
                if len(context) > 100:
                    context = context[:97] + '...'
        
        # Check if it's an important link
        is_important = False
        for pattern in important_patterns:
            if re.search(pattern, href, re.IGNORECASE) or re.search(pattern, text, re.IGNORECASE):
                is_important = True
                break
                
        if is_important or not context:  # Include links with context even if not matching patterns
            important_links.append((full_url, text, context))
    
    return important_links

def summarize_text(text, max_length=300):
    """Create a simple summary of text by extracting key sentences."""
    # Clean the text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # If text is already short, return it
    if len(text) <= max_length:
        return text
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # If only one sentence, truncate it
    if len(sentences) <= 1:
        return text[:max_length-3] + '...'
    
    # Take first sentence and as many as will fit in max_length
    summary = sentences[0]
    i = 1
    while i < len(sentences) and len(summary) + len(sentences[i]) + 1 < max_length:
        summary += ' ' + sentences[i]
        i += 1
    
    # Add ellipsis if we didn't include all sentences
    if i < len(sentences):
        summary += '...'
    
    return summary

def is_documentation(soup):
    """Determine if the page is likely documentation."""
    # Check for common documentation indicators
    doc_indicators = [
        'documentation', 'docs', 'api reference', 'developer guide',
        'manual', 'handbook', 'reference', 'guide'
    ]
    
    text = soup.get_text().lower()
    for indicator in doc_indicators:
        if indicator in text:
            return True
    
    # Check for code blocks
    if soup.find_all(['code', 'pre']):
        return True
    
    return False

# Streamlit UI with enhanced styling
st.set_page_config(page_title="LLMs.txt Generator", page_icon="📄")

st.title("🤖 LLMs.txt Generator")
st.markdown("""
Generate structured llms.txt files from any website. This tool helps websites communicate effectively 
with AI language models by creating a standardized content summary following best practices.
""")

# Add information about llms.txt
with st.expander("What is llms.txt?"):
    st.markdown("""
    **llms.txt** is a newly proposed web standard designed to help websites communicate effectively with AI language models. 
    
    It's a Markdown-formatted document placed at a website's root (e.g., `yourdomain.com/llms.txt`) that provides a concise, 
    structured summary of the site's content for consumption by Large Language Models (LLMs).
    
    Key benefits:
    - Helps AI models understand your content more accurately
    - Improves visibility in AI-powered search results
    - Gives website owners more control over how their content is used by AI
    - Provides a clean, machine-friendly format optimized for reasoning engines
    """)

# Add custom CSS
st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

url = st.text_input("🌐 Enter website URL:", placeholder="https://example.com")

col1, col2 = st.columns([2, 1])
with col1:
    generate_button = st.button("🔄 Generate LLMs.txt", use_container_width=True)

if generate_button:
    if url:
        with st.spinner("🔍 Analyzing website content..."):
            # Add a small delay to show the spinner
            time.sleep(0.5)
            content, error = generate_llms_txt(url)
            
            if error:
                st.error(f"❌ Error: {error}")
            else:
                st.success("✅ Generated successfully!")
                
                # Preview with tabs
                tab1, tab2 = st.tabs(["📝 Preview", "🔍 Raw Text"])
                
                with tab1:
                    st.markdown(content)
                
                with tab2:
                    st.text_area("Raw Content", content, height=400)
                
                # Download section
                st.markdown("---")
                st.markdown("### 📥 Download Options")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.download_button(
                        label="📄 Download llms.txt",
                        data=content,
                        file_name="llms.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
    else:
        st.warning("⚠️ Please enter a URL")

# Add footer with information based on research
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>
        This tool implements best practices for llms.txt creation as outlined in current research.
        The llms.txt standard helps bridge the gap between human-oriented web content and AI consumption,
        enabling fast, accurate AI responses and enhanced brand visibility.
    </small>
</div>
""", unsafe_allow_html=True)