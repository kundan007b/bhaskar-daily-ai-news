# 📰 Bhaskar Daily AI News

**AI-Curated Bilingual News Platform** | English & हिन्दी

Automated news aggregator generating factual, balanced coverage on Indian politics, business, technology, finance, and startups—updated every 8 hours.

🌐 **Live Site:** [www.kbhaskar.tech](https://www.kbhaskar.tech)

---

## ✨ Features

- 🤖 **AI-Powered Content Generation** using Google Gemini API
- 🌍 **Bilingual Support** - Full content in English & Hindi (Devanagari)
- ⚡ **Auto-Publishing** - New posts every 8 hours (00:00, 08:00, 16:00 UTC)
- 🎨 **AI-Generated Images** - Contextual editorial photos via Imagen
- 📱 **Responsive Design** - Mobile-first Jekyll theme
- 🔍 **SEO Optimized** - Rich metadata, structured data, Open Graph
- 🔒 **Privacy-Focused** - No user tracking, transparent AI disclosure

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         GitHub Actions (Scheduled)              │
│    Runs 3x daily: 00:30, 08:30, 16:30 UTC      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│      scripts/generate_post.py                   │
│  • Selects topic from rotation                  │
│  • Calls Gemini API for content (EN + HI)       │
│  • Generates contextual image via Imagen        │
│  • Validates JSON schema & content quality      │
│  • Writes markdown file to _posts/              │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│      Jekyll Build & GitHub Pages Deploy         │
│  • Builds static site from markdown             │
│  • Deploys to GitHub Pages                      │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Gemini API key ([get one here](https://ai.google.dev/))
- GitHub account (for deployment)

### Local Development

```bash
# Clone repository
git clone https://github.com/kundan007b/bhaskar-daily-ai-news.git
cd bhaskar-daily-ai-news

# Install Python dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your-api-key-here"

# Generate a test post
python scripts/generate_post.py

# Install Jekyll (for local preview)
bundle install

# Serve site locally
bundle exec jekyll serve
# Visit http://localhost:4000
```

### GitHub Actions Setup

1. **Add Secret to Repository:**
   - Go to: Settings → Secrets and variables → Actions
   - Create new secret: `GEMINI_API_KEY`
   - Paste your Gemini API key

2. **Enable GitHub Pages:**
   - Go to: Settings → Pages
   - Source: GitHub Actions
   - Save

3. **Workflow runs automatically** on schedule (3x daily)

---

## 📁 Project Structure

```
bhaskar-daily-ai-news/
├── _config.yml              # Jekyll configuration
├── _posts/                  # Generated markdown posts
├── _layouts/                # Page templates
│   ├── default.html
│   └── post.html
├── _includes/               # Reusable components
│   ├── seo.html            # Meta tags & structured data
│   ├── lang-toggle.html    # Bilingual switcher
│   └── adsense.html        # Ad integration
├── assets/images/          # AI-generated images
├── pages/                  # Static pages
│   ├── about.md
│   ├── contact.md
│   └── privacy-policy.md
├── scripts/
│   └── generate_post.py    # Content generator (main script)
├── .github/workflows/
│   └── auto_post.yml       # GitHub Actions workflow
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🛠️ Configuration

### Topics Rotation

Edit `scripts/generate_post.py`:

```python
TOPICS = [
    "India political news and government updates",
    "India business and economy news",
    "Technology and innovation in India",
    "Personal finance, taxation and savings tips",
    "Startups, entrepreneurs and success stories in India"
]
```

### Content Settings

```python
WORDS = 700                    # Target word count per article
MAX_IMAGE_WIDTH = 1200         # Image optimization width
IMAGE_QUALITY = 85             # JPEG quality (0-100)
```

### AdSense Setup

1. Get AdSense publisher ID from [Google AdSense](https://www.google.com/adsense)
2. Update `_config.yml`:
```yaml
adsense_client_id: "ca-pub-YOUR-ACTUAL-ID"
```

---

## 🔧 Features & Improvements

### ✅ Implemented

- [x] **Error Handling** - Retry logic with exponential backoff
- [x] **JSON Validation** - Schema validation for API responses
- [x] **Content Quality Checks** - Placeholder detection, word count, script validation
- [x] **Image Optimization** - Auto-resize & compression
- [x] **Atomic File Writes** - Collision prevention
- [x] **Comprehensive Logging** - Detailed execution logs
- [x] **SEO Enhancement** - Open Graph, Twitter Cards, JSON-LD
- [x] **Enhanced UI** - Modern language toggle with persistence
- [x] **Privacy Policy** - GDPR-compliant with AI disclosure
- [x] **Workflow Hardening** - Failure checks, change detection

### 🔜 Roadmap

- [ ] Manual review queue before auto-publish
- [ ] Fact-checking integration
- [ ] Multi-language expansion (more Indian languages)
- [ ] Newsletter subscription
- [ ] RSS feed per category
- [ ] Analytics dashboard
- [ ] User comments (Disqus/Utterances)
- [ ] Mobile PWA

---

## 📊 Monitoring & Logs

### Check Workflow Status

```bash
# View latest workflow runs
gh run list --repo kundan007b/bhaskar-daily-ai-news

# View logs for latest run
gh run view --repo kundan007b/bhaskar-daily-ai-news --log
```

### Local Testing

```bash
# Test content generation
python scripts/generate_post.py

# Validate generated posts
for f in _posts/*.md; do
  echo "Checking $f..."
  grep -E "^(title|category|description|keywords|image):" "$f" || echo "Missing field in $f"
done
```

---

## 🐛 Troubleshooting

### API Rate Limits

**Issue:** Gemini API quota exceeded  
**Solution:** 
- Check quota at [Google AI Studio](https://aistudio.google.com/)
- Reduce workflow frequency in `.github/workflows/auto_post.yml`
- Upgrade to paid tier

### Workflow Failures

**Issue:** GitHub Actions failing  
**Solutions:**
```bash
# Check if secret is set
gh secret list --repo kundan007b/bhaskar-daily-ai-news

# View failure logs
gh run view --repo kundan007b/bhaskar-daily-ai-news --log-failed

# Re-run failed workflow
gh run rerun <run-id>
```

### Image Generation Errors

**Issue:** Images not generating  
**Solution:**
- Verify Imagen API is enabled in Google Cloud Console
- Check API key has `generativelanguage.googleapis.com` access
- Review logs for specific error messages

---

## 📄 License

MIT License - See repository for details

---

## 👨‍💻 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

**Areas for contribution:**
- Code quality improvements
- New content validation checks
- UI/UX enhancements
- Documentation
- Bug fixes

---

## ⚠️ Disclaimer

**This is an AI-generated news platform.** Content is created automatically using Google Gemini API without manual fact-checking. While we implement quality controls:

- ❌ Do NOT use as sole news source
- ❌ Do NOT make critical decisions based on content
- ✅ DO verify information from authoritative sources
- ✅ DO treat as experimental/educational

See [Privacy Policy](/privacy-policy) for full disclosure.

---

## 📞 Contact

- **Issues:** [GitHub Issues](https://github.com/kundan007b/bhaskar-daily-ai-news/issues)
- **Website:** [www.kbhaskar.tech](https://www.kbhaskar.tech)
- **Repository:** [kundan007b/bhaskar-daily-ai-news](https://github.com/kundan007b/bhaskar-daily-ai-news)

---

**Built with ❤️ using Jekyll, GitHub Actions, and Google Gemini AI**
