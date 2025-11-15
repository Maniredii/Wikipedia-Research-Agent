# 📚 Wikipedia Research Agent

A powerful AI-powered research tool that leverages Wikipedia's vast knowledge base combined with advanced LLM capabilities to provide comprehensive research reports on any topic.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **Intelligent Wikipedia Search**: Automatically searches and retrieves relevant Wikipedia articles
- **AI-Enhanced Summaries**: Generates concise summaries using OpenRouter or Groq LLMs
- **Multi-Format Export**: Download reports in Markdown, Text, JSON, or PDF formats
- **Interactive UI**: Beautiful Streamlit interface with tabs, filters, and real-time updates
- **Configurable Depth**: Control search depth, number of sources, and timeout limits
- **Source Management**: View, filter, and organize research sources efficiently
- **Secure API Key Handling**: Keys loaded from environment variables, never displayed in UI

## 🚀 Live Demo

Try the app live on Streamlit Cloud:

**[Launch Wikipedia Research Agent →](https://wikipedia-research-agent.streamlit.app)**

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- API keys (optional, for AI summaries):
  - [OpenRouter API Key](https://openrouter.ai/) - Primary LLM provider
  - [Groq API Key](https://console.groq.com/) - Fallback LLM provider

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/wikipedia-research-agent.git
cd wikipedia-research-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# .env
OPENROUTER_API_KEY=sk-or-your-key-here
GROQ_API_KEY=gsk-your-key-here
```

**Note**: API keys are optional. The app will work without them, but AI-enhanced summaries won't be available.

## 📦 Dependencies

Create a `requirements.txt` file with:

```txt
streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
reportlab>=4.0.0
groq>=0.4.0
```

## 🎯 Usage

### Running Locally

```bash
streamlit run Deep_research.py
```

The app will open in your default browser at `http://localhost:8501`

### Basic Workflow

1. **Enter Research Topic**: Type your topic in the search box (e.g., "Machine Learning")
2. **Configure Settings**: Adjust sources, timeout, and depth using sliders
3. **Start Research**: Click "🚀 Start Research" button
4. **Explore Results**: Navigate through tabs:
   - 📚 **Sources**: View all retrieved Wikipedia articles
   - 📊 **Analysis**: Read full research content with filtering
   - 💡 **Summary**: Get AI-generated summary (requires API key)
   - ⚙️ **Export**: Download reports in multiple formats

### Advanced Features

#### API Key Validation

Navigate to sidebar → 🔑 API Keys → 🔐 Validate Keys to test your API connections.

#### Export Options

- **Markdown**: Formatted report with headers and links
- **Text**: Plain text version
- **JSON**: Structured data for programmatic use
- **PDF**: Professional report with tables and formatting

#### Search Customization

- **Sources (1-20)**: Number of Wikipedia articles to retrieve
- **Timeout (30-300s)**: Maximum time for research
- **Depth (1-3)**: Search depth level (currently uses depth 1)

## 🏗️ Project Structure

```
wikipedia-research-agent/
├── Deep_research.py       # Main application file
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore file
```

## 🔐 Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly
4. **Limit API key permissions** to minimum required scope
5. **Monitor API usage** to detect unauthorized access

Add to `.gitignore`:

```gitignore
.env
*.pyc
__pycache__/
.streamlit/secrets.toml
```

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `Deep_research.py`
6. Add secrets in "Advanced settings":
   ```toml
   OPENROUTER_API_KEY = "your-key-here"
   GROQ_API_KEY = "your-key-here"
   ```
7. Click "Deploy"

### Deploy to Other Platforms

- **Heroku**: Use `Procfile` with `web: streamlit run Deep_research.py`
- **AWS EC2**: Run with `nohup streamlit run Deep_research.py &`
- **Docker**: Create Dockerfile with Streamlit base image
- **Google Cloud Run**: Use Cloud Run with Streamlit container

## 🛠️ Customization Guide

This section explains what you can customize in the application to fit your needs.

### 🎨 1. UI Appearance & Theme

**What you can change**: Colors, button styles, spacing, fonts

**Where to edit**: `Deep_research.py` - Lines 18-40 (Custom CSS section)

**Example changes**:

```python
# Change button color gradient
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  # Change these hex colors
}

# Modify metric card colors
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  # Your custom gradient
}
```

**Quick color schemes**:
- Blue theme: `#667eea` → `#4158D0`
- Green theme: `#11998e` → `#38ef7d`
- Orange theme: `#f46b45` → `#eea849`

---

### 🤖 2. AI Models (LLM Configuration)

**What you can change**: Which AI model generates summaries

**Where to edit**: `Deep_research.py` - Line 169 (OpenRouter) and Line 181 (Groq)

**OpenRouter model options**:

```python
# In the call_llm() function, find this line:
payload = {"model": "tngtech/deepseek-r1t2-chimera:free", ...}

# Replace with any of these:
"openai/gpt-3.5-turbo"           # Fast, affordable
"anthropic/claude-3-haiku"       # Balanced performance
"meta-llama/llama-3-8b-instruct" # Open source
"google/gemini-pro"              # Google's model
```

Browse all models: [OpenRouter Models](https://openrouter.ai/models)

**Groq model options**:

```python
# Find this line:
resp = client.chat.completions.create(model="mixtral-8x7b-32768", ...)

# Replace with:
"llama-3.1-70b-versatile"  # Most capable
"llama-3.1-8b-instant"     # Fastest
"gemma2-9b-it"             # Efficient
```

Browse all models: [Groq Models](https://console.groq.com/docs/models)

---

### 📊 3. Search Parameters (Default Values)

**What you can change**: Default number of sources, timeout, depth

**Where to edit**: `Deep_research.py` - Lines 68-74

**Current defaults**:

```python
max_urls = st.slider("📊 Sources", min_value=1, max_value=20, value=5, ...)
# Change value=5 to your preferred default (e.g., value=10)

time_limit = st.slider("⏱️ Timeout (s)", min_value=30, max_value=300, value=120, ...)
# Change value=120 to your preferred timeout (e.g., value=180)

max_depth = st.slider("🔗 Depth", min_value=1, max_value=3, value=2, ...)
# Change value=2 to your preferred depth (e.g., value=1)
```

**Recommended settings**:
- Quick research: `sources=3, timeout=60, depth=1`
- Standard research: `sources=5, timeout=120, depth=2`
- Deep research: `sources=10, timeout=300, depth=3`

---

### 📝 4. Summary Length & Style

**What you can change**: How detailed AI summaries are

**Where to edit**: `Deep_research.py` - Line 79 (generate_summary function)

**Current prompt**:

```python
{"role": "system", "content": "You are a research expert. Provide a concise, well-structured summary of the research findings in 2-3 paragraphs."}
```

**Alternative prompts**:

```python
# Detailed summary (5-7 paragraphs)
"You are a research expert. Provide a comprehensive, detailed summary with key findings, implications, and conclusions in 5-7 paragraphs."

# Bullet-point summary
"You are a research expert. Provide a summary as bullet points highlighting the most important findings."

# Executive summary
"You are a research expert. Provide an executive summary suitable for business stakeholders in 1-2 paragraphs."

# Academic style
"You are a research expert. Provide an academic-style summary with methodology, findings, and conclusions."
```

---

### 🔍 5. Wikipedia Search Behavior

**What you can change**: Search parameters and content extraction

**Where to edit**: `Deep_research.py` - Lines 103-150 (deep_research function)

**Adjustable parameters**:

```python
# Number of search results (line 117)
"srlimit": max_urls  # Already configurable via UI

# Content length per source (line 141)
text = page["extract"][:1200]  # Change 1200 to extract more/less text
# Recommended: 800 (brief), 1200 (standard), 2000 (detailed)

# Search language (line 113)
search_url = "https://en.wikipedia.org/w/api.php"
# Change 'en' to other languages: 'es', 'fr', 'de', 'ja', etc.
```

---

### 📄 6. Export Formats

**What you can change**: Report structure and formatting

**Where to edit**: `Deep_research.py` - Lines 267-285 (Export tab)

**Customize report content**:

```python
# Add custom sections to report (line 271)
report_content = f"""# Research Report: {topic}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
{results.get('summary', 'No summary available')[:1000]}

## Key Findings  # Add this section
- Finding 1
- Finding 2

## Detailed Sources
"""
```

**PDF customization** (lines 93-101):
- Change page size: `pagesize=letter` → `pagesize=A4`
- Modify colors: `colors.HexColor('#667eea')` → your color
- Adjust fonts: `fontName='Helvetica-Bold'` → other fonts

---

### ⚙️ 7. Page Configuration

**What you can change**: App title, icon, layout

**Where to edit**: `Deep_research.py` - Line 13

```python
st.set_page_config(
    page_title="Wikipedia Research Agent",  # Change app title
    page_icon="📚",                         # Change emoji icon
    layout="wide",                          # Options: "wide" or "centered"
    initial_sidebar_state="expanded"        # Options: "expanded" or "collapsed"
)
```

**Icon options**: Use any emoji: 🔬, 🎓, 📖, 🧠, 💡, 🔍, 📊

---

### 🔒 8. API Key Management

**What you can change**: How API keys are loaded

**Where to edit**: `Deep_research.py` - Lines 15-20

**Current method**: Environment variables from `.env` file

**Alternative methods**:

```python
# Option 1: Streamlit secrets (for cloud deployment)
st.session_state.openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY", "")

# Option 2: Direct input (less secure, for testing only)
# Uncomment the text_input fields in sidebar if needed

# Option 3: Config file
import json
with open('config.json') as f:
    config = json.load(f)
    st.session_state.openrouter_api_key = config.get("openrouter_key", "")
```

---

### 📱 9. UI Layout & Components

**What you can change**: Number of columns, tab names, button labels

**Where to edit**: Throughout `Deep_research.py`

**Examples**:

```python
# Change number of columns (line 66)
col1, col2, col3, col4 = st.columns(4)  # Change to 3 or 5 columns

# Rename tabs (line 223)
tab1, tab2, tab3, tab4 = st.tabs(["📚 Sources", "📊 Analysis", "💡 Summary", "⚙️ Export"])
# Change to: ["Research", "Details", "AI Summary", "Download"]

# Modify button text (line 77)
search_button = st.button("🚀 Start Research", ...)
# Change to: "Begin Analysis", "Search Now", etc.
```

---

### 🎯 Quick Customization Checklist

Use this checklist to track your customizations:

- [ ] Changed color scheme to match brand
- [ ] Updated default search parameters
- [ ] Selected preferred AI model
- [ ] Customized summary prompt style
- [ ] Adjusted content extraction length
- [ ] Modified report format
- [ ] Changed page title and icon
- [ ] Set up API keys properly
- [ ] Tested all export formats
- [ ] Updated footer/branding

---

### 💡 Pro Tips

1. **Test changes locally** before deploying to Streamlit Cloud
2. **Keep backups** of original code before major changes
3. **Use version control** (Git) to track modifications
4. **Check API costs** when changing models
5. **Validate changes** with different search topics
6. **Monitor performance** after customization

---

### 🆘 Need Help?

If you're unsure about a customization:

1. Check the [Streamlit Documentation](https://docs.streamlit.io/)
2. Review [OpenRouter API Docs](https://openrouter.ai/docs)
3. Read [Wikipedia API Guide](https://www.mediawiki.org/wiki/API:Main_page)
4. Create an issue on GitHub with your question

## 📊 API Rate Limits

Be aware of rate limits:

- **Wikipedia API**: Generally unlimited for reasonable use
- **OpenRouter**: Varies by model and plan
- **Groq**: Check your account limits

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No LLM provider available"
- **Solution**: Set API keys in `.env` file and restart app

**Issue**: "No results found"
- **Solution**: Try different search terms or increase timeout

**Issue**: PDF generation fails
- **Solution**: Install reportlab: `pip install reportlab`

**Issue**: Groq import error
- **Solution**: Install groq: `pip install groq`

### Debug Mode

Enable Streamlit debug mode:

```bash
streamlit run Deep_research.py --logger.level=debug
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) for providing free access to knowledge
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [OpenRouter](https://openrouter.ai/) for unified LLM access
- [Groq](https://groq.com/) for fast inference
- [ReportLab](https://www.reportlab.com/) for PDF generation

## 📧 Contact

For questions or support:

- Create an [Issue](https://github.com/yourusername/wikipedia-research-agent/issues)
- Email: your.email@example.com
- Twitter: [@yourhandle](https://twitter.com/yourhandle)

## 🗺️ Roadmap

- [ ] Add support for multiple languages
- [ ] Implement citation management
- [ ] Add collaborative research features
- [ ] Create browser extension
- [ ] Add voice input/output
- [ ] Implement research history tracking
- [ ] Add export to Notion/Obsidian
- [ ] Create mobile app version

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for Research Excellence**

[⬆ Back to Top](#-wikipedia-research-agent)
