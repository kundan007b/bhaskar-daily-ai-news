# 📰 Bhaskar Daily News

**Bilingual News Platform** | English & हिन्दी

Bilingual news covering Indian politics, business, technology, finance, and startups—written by KB with regular updates.

🌐 **Live Site:** [www.kbhaskar.tech](https://www.kbhaskar.tech)

---

## ✨ Features

- ✍️ **Written by KB** - Personal insights and analysis
- 🌍 **Bilingual Support** - Full content in English & Hindi (Devanagari)
- 📝 **Manual Publishing** - Admin panel for easy content management
- 🖼️ **Custom Images** - Manually curated images for each post
- 📱 **Responsive Design** - Mobile-first Jekyll theme
- 🔍 **SEO Optimized** - Rich metadata, structured data, Open Graph
- 🔒 **Privacy-Focused** - No user tracking

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         Admin Panel (Browser-based)             │
│    /admin - Write, edit, and publish posts      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│      GitHub API (via Personal Token)            │
│  • Creates/updates markdown files in _posts/    │
│  • Uploads images to assets/images/             │
│  • Commits changes directly to repository       │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│      Jekyll Build & GitHub Pages Deploy         │
│  • Builds static site from markdown             │
│  • Deploys automatically on push                │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- GitHub account (for deployment and admin access)
- GitHub Personal Access Token (for admin panel)

### Local Development

```bash
# Clone repository
git clone https://github.com/kundan007b/bhaskar-daily-ai-news.git
cd bhaskar-daily-ai-news

# Install Jekyll (for local preview)
bundle install

# Serve site locally
bundle exec jekyll serve
# Visit http://localhost:4000
```

### GitHub Pages Setup

1. **Enable GitHub Pages:**
   - Go to: Settings → Pages
   - Source: GitHub Actions
   - Save

2. **Site automatically deploys** on every push to main

### Admin Panel Access

1. **Visit:** https://www.kbhaskar.tech/admin/
2. **Login:** Username: `kb007`, Password: `Kundan@20`
3. **Generate GitHub Token:**
   - Go to: https://github.com/settings/tokens?type=beta
   - Create fine-grained token with "Contents: Read and write"
4. **Start writing posts!**

---

## � Tier 1: No‑cost subscribers & post submissions (GitHub‑native)

This repo includes two GitHub‑native workflows that let you collect emails and publish posts without any external backend.

### 1) Subscribe via GitHub Issues

- Link: https://github.com/kundan007b/bhaskar-daily-ai-news/issues/new?template=subscribe.yml
- Form stores emails to a private repository as CSV using a Personal Access Token (PAT).

Setup (one‑time):

1. Create or choose a private repo to store subscribers, e.g. `kundan007b/news-subscribers`
2. Create a classic PAT with `repo` scope (Settings → Developer settings → Personal access tokens → Tokens (classic))
3. Add two repository secrets here (Settings → Secrets and variables → Actions):
   - `SUBS_REPO` = `OWNER/REPO` (e.g., `kundan007b/news-subscribers`)
   - `SUBS_REPO_TOKEN` = your PAT with repo scope
4. The workflow `.github/workflows/subscribe-intake.yml` will:
   - Parse the email from the issue
   - Clone the private repo, append to `data/subscribers.csv`
   - Comment and close the issue

CSV schema: `timestamp,email,source,issue_url`

### 2) Submit a post via GitHub Issues

- Link: https://github.com/kundan007b/bhaskar-daily-ai-news/issues/new?template=new_post.yml
- The workflow `.github/workflows/issue-to-post.yml` converts the issue into a Jekyll post in `_posts/` and pushes to `main`. Our existing deploy-on-push workflow takes care of publishing.

Tips:
- Provide a concise English title and one-line summary (used for SEO description)
- Category must be one of: politics, business, technology, finance, startups
- You may include an optional image URL
- You can also add a Hindi section (optional)

Security & privacy:
- Subscriber emails are stored in a private repo you control
- No extra SaaS cost; everything runs on GitHub Actions

---

## �📁 Project Structure

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
- [x] Newsletter subscription via GitHub Issues (Tier 1 backend)
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
