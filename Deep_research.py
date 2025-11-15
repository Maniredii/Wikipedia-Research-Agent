import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from typing import List, Dict, Any
from datetime import datetime
import base64

# Load environment variables from .env (if present)
load_dotenv()

# Page config
st.set_page_config(page_title="Wikipedia Research Agent", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "openrouter_api_key" not in st.session_state:
    st.session_state.openrouter_api_key = os.environ.get("OPENROUTER_API_KEY", "")
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.environ.get("GROQ_API_KEY", "")
if "research_results" not in st.session_state:
    st.session_state.research_results = None

# Sidebar - API keys
with st.sidebar:
    st.title("⚙️ Configuration")
    
    with st.expander("🔑 API Keys", expanded=False):
        st.markdown("**LLM API Keys** (for enhanced summaries)")
        st.info("ℹ️ API keys are loaded from environment variables (.env file)")
        
        # Show status without revealing keys
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.openrouter_api_key:
                st.success("✅ OpenRouter: Configured")
            else:
                st.warning("⚠️ OpenRouter: Not set")
        with col2:
            if st.session_state.groq_api_key:
                st.success("✅ Groq: Configured")
            else:
                st.warning("⚠️ Groq: Not set")
        
        st.markdown("---")
        st.markdown("**To configure API keys:**")
        st.code("1. Create a .env file in the project directory\n2. Add: OPENROUTER_API_KEY=your_key_here\n3. Add: GROQ_API_KEY=your_key_here\n4. Restart the application", language="text")

    with st.expander("🔐 Validate Keys"):
        if st.button("✓ Validate API Keys"):
            if st.session_state.openrouter_api_key:
                try:
                    payload = {"model": "tngtech/deepseek-r1t2-chimera:free", "messages": [{"role": "user", "content": "Ping"}]}
                    r = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {st.session_state.openrouter_api_key}", "Content-Type": "application/json"},
                        json=payload,
                        timeout=15,
                    )
                    if r.status_code == 200:
                        st.success("✅ OpenRouter key OK")
                    else:
                        st.error(f"❌ OpenRouter validation failed: {r.status_code}")
                except Exception as e:
                    st.error(f"❌ OpenRouter validation error: {e}")
            else:
                st.info("ℹ️ OpenRouter key not set")

# Main UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📚 Wikipedia Research Agent")
    st.markdown("*Comprehensive Research Powered by Wikipedia + AI Summaries*")

with col2:
    st.metric("Version", "2.0")

st.markdown("---")

# Search Configuration
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**🔍 Research Topic**")
    topic = st.text_input("Research Topic", placeholder="e.g., Machine Learning", label_visibility="collapsed")
with col2:
    st.markdown("**📊 Number of Sources**")
    max_urls = st.slider("Sources", min_value=1, max_value=20, value=5, label_visibility="collapsed", help="How many Wikipedia articles to retrieve (1-20)")
with col3:
    st.markdown("**⏱️ Timeout (seconds)**")
    time_limit = st.slider("Timeout", min_value=30, max_value=300, value=120, label_visibility="collapsed", help="Maximum time to wait for research (30-300 seconds)")
with col4:
    st.markdown("**🔗 Search Depth**")
    max_depth = st.slider("Depth", min_value=1, max_value=3, value=2, label_visibility="collapsed", help="Search depth level (1=quick, 3=thorough)")


def generate_summary(research_data: Dict[str, Any], query: str) -> str:
    """Generate AI summary of research findings."""
    if not (st.session_state.openrouter_api_key or st.session_state.groq_api_key):
        return "AI summary unavailable - set API key in configuration"
    
    try:
        sources_text = "\n".join([f"- {s['title']}: {s['snippet'][:200]}" for s in research_data.get("sources", [])[:5]])
        messages = [
            {"role": "system", "content": "You are a research expert. Provide a concise, well-structured summary of the research findings in 2-3 paragraphs."},
            {"role": "user", "content": f"Topic: {query}\n\nSources:\n{sources_text}\n\nPlease summarize the key findings."}
        ]
        return call_llm(messages, temperature=0.7)
    except Exception as e:
        return f"Summary generation failed: {str(e)}"


def download_report(content: str, format_type: str, filename: str):
    """Generate downloadable report."""
    if format_type == "markdown":
        return content
    elif format_type == "text":
        return content.replace("**", "").replace("🔗", "").replace("📖", "")
    elif format_type == "html":
        return f"<html><body><pre>{content}</pre></body></html>"
    return content


def copy_to_clipboard(text: str):
    """Prepare text for clipboard copy."""
    return text


def generate_pdf_report(topic: str, results: Dict[str, Any]) -> bytes:
    """Generate a PDF report from research results."""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib import colors
        from io import BytesIO
        
        # Create PDF in memory
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        # Title
        story.append(Paragraph(f"Research Report: {topic}", title_style))
        story.append(Paragraph(f"<i>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Summary section
        story.append(Paragraph("Executive Summary", heading_style))
        summary_text = results.get('summary', 'No summary available')[:2000]
        story.append(Paragraph(summary_text, styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))
        
        # Sources section
        story.append(Paragraph("Sources", heading_style))
        sources = results.get('sources', [])
        
        if sources:
            # Create table data
            table_data = [['#', 'Title', 'URL']]
            for i, source in enumerate(sources, 1):
                table_data.append([
                    str(i),
                    source.get('title', 'N/A')[:50],
                    source.get('url', 'N/A')[:40]
                ])
            
            # Create and style table
            table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 2.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            story.append(table)
        
        story.append(Spacer(1, 0.2*inch))
        
        # Detailed sources
        if sources:
            story.append(PageBreak())
            story.append(Paragraph("Detailed Source Content", heading_style))
            
            for i, source in enumerate(sources, 1):
                story.append(Paragraph(f"{i}. {source.get('title', 'N/A')}", styles['Heading3']))
                story.append(Paragraph(f"<b>URL:</b> {source.get('url', 'N/A')}", styles['Normal']))
                content = source.get('snippet', 'No content available')[:1000]
                story.append(Paragraph(content, styles['BodyText']))
                story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    
    except ImportError:
        st.error("❌ reportlab not installed. Install with: pip install reportlab")
        return None
    except Exception as e:
        st.error(f"❌ PDF generation failed: {str(e)}")
        return None


def call_llm(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    """Call OpenRouter first, fall back to Groq if available."""
    # OpenRouter HTTP
    if st.session_state.openrouter_api_key:
        try:
            payload = {"model": "tngtech/deepseek-r1t2-chimera:free", "messages": messages, "temperature": temperature}
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {st.session_state.openrouter_api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            # OpenRouter uses OpenAI-like response structure
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            st.warning(f"OpenRouter call failed: {e}")

    # Groq fallback (best-effort)
    if st.session_state.groq_api_key:
        try:
            import groq  # type: ignore
            client = groq.Groq(api_key=st.session_state.groq_api_key)
            resp = client.chat.completions.create(model="mixtral-8x7b-32768", messages=messages, temperature=temperature)
            # adapt to expected structure
            return getattr(resp.choices[0].message, "content", str(resp))
        except Exception as e:
            raise RuntimeError(f"Groq call failed: {e}")

    raise RuntimeError("No LLM provider available. Set OpenRouter or Groq key in the sidebar.")


def deep_research(query: str, max_depth: int, time_limit: int, max_urls: int) -> Dict[str, Any]:
    """Run web research using Wikipedia API."""
    import time
    import json
    
    start_time = time.time()
    results = {"query": query, "sources": []}
    content_summary = []
    
    try:
        with st.spinner(f"Researching '{query}'..."):
            headers = {"User-Agent": "Mozilla/5.0"}
            
            # Search Wikipedia for the query
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": max_urls
            }
            
            st.write(f"🔍 Searching for '{query}'...")
            search_resp = requests.get(search_url, params=search_params, headers=headers, timeout=10)
            search_data = search_resp.json()
            
            if "query" in search_data and "search" in search_data["query"]:
                search_results = search_data["query"]["search"]
                
                if not search_results:
                    return {"success": False, "error": f"No results found for '{query}'"}
                
                # Fetch full content for each result
                counter = 1
                for result in search_results[:max_urls]:
                    if time.time() - start_time > time_limit:
                        break
                    
                    title = result.get("title", "")
                    
                    # Get full page content
                    content_params = {
                        "action": "query",
                        "format": "json",
                        "titles": title,
                        "prop": "extracts",
                        "explaintext": True,
                        "exintro": False,
                        "exlimit": 1
                    }
                    
                    try:
                        st.write(f"📖 Fetching [{counter}] {title}...")
                        content_resp = requests.get(search_url, params=content_params, headers=headers, timeout=10)
                        content_data = content_resp.json()
                        
                        if "query" in content_data and "pages" in content_data["query"]:
                            for page_id, page in content_data["query"]["pages"].items():
                                if "extract" in page:
                                    text = page["extract"][:1200]
                                    url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                                    
                                    results["sources"].append({
                                        "title": title,
                                        "url": url,
                                        "snippet": text
                                    })
                                    
                                    # Format for display
                                    content_summary.append(
                                        f"{counter}. **{title}**\n\n"
                                        f"{text}\n\n"
                                        f"🔗 Source: {url}\n\n"
                                        f"{'─' * 80}\n\n"
                                    )
                                    counter += 1
                                    break
                    except Exception as e:
                        st.write(f"⚠️ Could not fetch {title}: {str(e)[:40]}")
                        continue
            else:
                return {"success": False, "error": "No search results found"}
            
            results["summary"] = "".join(content_summary)
            
            if not content_summary:
                return {"success": False, "error": "Could not retrieve any content"}
        
        return {"success": True, "data": results}
    except Exception as e:
        return {"success": False, "error": f"Research failed: {str(e)}"}


# Main Research Button
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    search_button = st.button("🚀 Start Research", use_container_width=True, type="primary")
with col2:
    clear_button = st.button("🔄 Clear", use_container_width=True)
with col3:
    st.write("")  # Spacer

if clear_button:
    st.session_state.research_results = None
    st.rerun()

if search_button:
    if not topic:
        st.error("❌ Please enter a research topic")
    else:
        st.markdown("---")
        dr = deep_research(topic, max_depth, time_limit, max_urls)
        
        if not dr.get("success"):
            st.error(f"❌ Research failed: {dr.get('error')}")
        else:
            st.session_state.research_results = dr.get("data")
            results = st.session_state.research_results
            
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📚 Sources", "📊 Analysis", "💡 Summary", "⚙️ Export"])
            
            with tab1:
                st.subheader("Research Sources")
                col1, col2 = st.columns([3, 1])
                with col2:
                    sort_by = st.selectbox("Sort by", ["Order", "Title"])
                
                sources = results.get("sources", [])
                if sources:
                    for i, source in enumerate(sources, 1):
                        with st.expander(f"**{i}. {source['title']}**", expanded=(i==1)):
                            st.markdown(f"**Source:** {source.get('url', 'N/A')}")
                            st.markdown(f"**Content:**\n\n{source.get('snippet', 'No content')}")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.button(f"📋 Copy", key=f"copy_{i}")
                            with col2:
                                st.button(f"🔗 Visit", key=f"visit_{i}")
                            with col3:
                                st.button(f"⭐ Save", key=f"save_{i}")
                else:
                    st.info("No sources found")
            
            with tab2:
                st.subheader("Research Analysis")
                full_summary = results.get("summary", "No summary available")
                st.markdown(full_summary)
                
                # Filtering options
                col1, col2 = st.columns(2)
                with col1:
                    filter_text = st.text_input("🔎 Filter content", placeholder="Search within results")
                    if filter_text:
                        filtered = full_summary.lower().find(filter_text.lower()) != -1
                        if filtered:
                            st.success(f"✅ Found: {filter_text}")
                        else:
                            st.warning(f"❌ Not found: {filter_text}")
                
                with col2:
                    st.write("")
            
            with tab3:
                st.subheader("AI-Enhanced Summary")
                with st.spinner("🤖 Generating summary..."):
                    summary = generate_summary(results, topic)
                    st.markdown(summary)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button("🔄 Regenerate Summary")
                with col2:
                    st.button("👎 Not helpful?")
            
            with tab4:
                st.subheader("Export Report")
                
                # Generate report content
                report_content = f"""# Research Report: {topic}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
{results.get('summary', 'No summary available')[:1000]}

## Sources ({len(results.get('sources', []))})
"""
                
                for i, source in enumerate(results.get("sources", []), 1):
                    report_content += f"\n### {i}. {source['title']}\n"
                    report_content += f"**URL:** {source.get('url', 'N/A')}\n\n"
                    report_content += f"{source.get('snippet', 'No content')}\n\n"
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.download_button(
                        label="📥 Markdown",
                        data=report_content,
                        file_name=f"{topic.replace(' ', '_')}_report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        label="📥 Text",
                        data=report_content.replace("**", "").replace("###", ""),
                        file_name=f"{topic.replace(' ', '_')}_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col3:
                    st.download_button(
                        label="📊 JSON",
                        data=json.dumps(results, indent=2),
                        file_name=f"{topic.replace(' ', '_')}_report.json",
                        mime="application/json",
                        use_container_width=True
                    )
                with col4:
                    pdf_data = generate_pdf_report(topic, results)
                    if pdf_data:
                        st.download_button(
                            label="📄 PDF",
                            data=pdf_data,
                            file_name=f"{topic.replace(' ', '_')}_report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                
                # Show statistics
                st.markdown("---")
                st.subheader("📈 Report Statistics")
                col1, col2, col3 = st.columns(3)
                col1.metric("📊 Total Sources", len(results.get("sources", [])))
                col2.metric("📝 Total Characters", len(results.get("summary", "")))
                col3.metric("⏱️ Generation Time", f"{time_limit}s")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><small>📚 Wikipedia Research Agent v2.0</small></p>
    <p><small>Made with ❤️ for Research Excellence by <strong>Manideep Reddy Eevuri</strong></small></p>
    <p style='margin-top: 20px;'>
        <a href='https://github.com/Maniredii' target='_blank' style='text-decoration: none; margin: 0 10px;'>
            <img src='https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'>
        </a>
        <a href='https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/' target='_blank' style='text-decoration: none; margin: 0 10px;'>
            <img src='https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white' alt='LinkedIn'>
        </a>
        <a href='https://buymeacoffee.com/manideep' target='_blank' style='text-decoration: none; margin: 0 10px;'>
            <img src='https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black' alt='Buy Me A Coffee'>
        </a>
    </p>
</div>
""", unsafe_allow_html=True)