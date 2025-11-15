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

## 🛠️ Configuration

### Customizing LLM Models

Edit the `call_llm()` function to change models:

```python
# OpenRouter model
payload = {"model": "tngtech/deepseek-r1t2-chimera:free", ...}

# Groq model
resp = client.chat.completions.create(model="mixtral-8x7b-32768", ...)
```

Available OpenRouter models: [OpenRouter Models](https://openrouter.ai/models)

Available Groq models: [Groq Models](https://console.groq.com/docs/models)

### Adjusting UI Theme

Modify the custom CSS in the `st.markdown()` section at the top of `Deep_research.py`.

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
