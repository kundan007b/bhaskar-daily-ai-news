# Changelog

All notable changes to Bhaskar Daily AI News project.

## [2.0.0] - 2025-10-31

### 🚀 Major Improvements

#### Security & Reliability
- **API Error Handling**: Implemented retry logic with exponential backoff (3 attempts)
- **Input Validation**: Added JSON schema validation for all API responses
- **Atomic File Writes**: Prevent corruption with temporary file + move strategy
- **Content Quality Checks**: Automated validation for placeholders, word count, and script correctness
- **Environment Validation**: API key verification before execution
- **Comprehensive Logging**: Detailed execution logs with timestamps and severity levels

#### Content Generation
- **Enhanced Prompts**: More detailed instructions for factual, balanced content
- **Image Optimization**: Auto-resize and compress images (max 1200px width, 85% quality)
- **Better Metadata**: Extended front matter with alt text, multi-language meta descriptions
- **Hindi Script Validation**: Ensures proper Devanagari characters in Hindi content
- **Collision Prevention**: Checks for existing posts before writing

#### SEO & Web Standards
- **Rich Meta Tags**: Open Graph, Twitter Cards, canonical URLs
- **Structured Data**: Comprehensive JSON-LD NewsArticle schema
- **Image Metadata**: Proper dimensions and alt text in meta tags
- **Hreflang Tags**: Language alternates for bilingual content
- **Publisher Info**: Organization schema with logo

#### User Interface
- **Modern Language Toggle**: Styled buttons with active states
- **Smooth Transitions**: Fade-in animations for content switching
- **Persistent Preferences**: LocalStorage for language selection
- **Improved Layout**: Better spacing, responsive design
- **Category Tags**: Visual category badges

#### Documentation
- **Comprehensive README**: Full setup guide, architecture, troubleshooting
- **Privacy Policy**: GDPR-compliant with AI disclosure
- **Code Documentation**: Inline comments and docstrings
- **Validation Script**: Pre-flight checks for dependencies and configuration

#### DevOps & CI/CD
- **GitHub Actions Hardening**: Failure detection and error reporting
- **Change Detection**: Only commits when new content exists
- **Better Commit Messages**: Timestamped with UTC time
- **Proper Checkout**: Ensures deploy uses latest main branch
- **Dependency Pinning**: Locked versions for reproducible builds

### 📦 Dependencies Added
- `tenacity==9.0.0` - Retry logic for API calls
- `jsonschema==4.23.0` - JSON validation
- `Pillow==11.0.0` - Image optimization
- `python-dotenv==1.0.1` - Environment variable management

### 🔧 Configuration Changes
- Pinned all Python dependencies to specific versions
- Updated GitHub Actions workflow with error handling
- Enhanced AdSense integration with conditional rendering
- Improved Jekyll exclude patterns

### 📝 Files Modified
- `scripts/generate_post.py` - Complete rewrite with error handling, validation, and logging
- `requirements.txt` - Pinned versions + new dependencies
- `.github/workflows/auto_post.yml` - Enhanced with failure detection
- `_includes/seo.html` - Expanded meta tags and structured data
- `_includes/lang-toggle.html` - Modern UI with animations
- `_includes/adsense.html` - Conditional rendering based on config
- `_layouts/post.html` - Better image handling and metadata
- `pages/privacy-policy.md` - Comprehensive legal disclosure
- `README.md` - Full documentation
- `_config.yml` - Minor formatting improvements

### 📁 Files Added
- `scripts/validate_setup.py` - Pre-flight validation tool
- `CHANGELOG.md` - This file

### 🐛 Bug Fixes
- Fixed potential race conditions in file writing
- Prevented broken posts from placeholder text
- Resolved markdown code block validation
- Fixed image format compatibility (RGBA → RGB conversion)
- Corrected meta description length validation

### ⚡ Performance
- Image optimization reduces file sizes by ~30-50%
- Atomic writes prevent file corruption
- Retry logic prevents transient failures
- Efficient JSON parsing with error recovery

### 🔐 Security
- API key validation on startup
- No secrets logged in GitHub Actions
- Safe file operations with proper error handling
- Input sanitization for generated content

---

## [1.0.0] - Initial Release

### Features
- Basic AI content generation using Gemini API
- Bilingual support (English & Hindi)
- Automated posting via GitHub Actions
- Jekyll-based static site
- Basic SEO optimization
- AdSense integration placeholder

---

## Upgrade Instructions

### From 1.0.0 to 2.0.0

1. **Update Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Validate Setup:**
   ```bash
   python scripts/validate_setup.py
   ```

3. **Test Locally:**
   ```bash
   export GEMINI_API_KEY="your-key-here"
   python scripts/generate_post.py
   ```

4. **Update GitHub Secrets:**
   - Ensure `GEMINI_API_KEY` is set in repository secrets
   - No other secrets required

5. **Deploy:**
   - Push changes to main branch
   - GitHub Actions will handle the rest

### Breaking Changes
- None - All changes are backward compatible
- Existing posts remain unchanged
- New posts will have enhanced metadata

---

## Roadmap

### v2.1.0 (Planned)
- [ ] Manual review queue
- [ ] Fact-checking API integration
- [ ] Email notifications for workflow failures
- [ ] Dry-run mode for testing

### v2.2.0 (Planned)
- [ ] Multi-language expansion (Tamil, Bengali, Telugu)
- [ ] RSS feed per category
- [ ] Newsletter subscription
- [ ] Analytics dashboard

### v3.0.0 (Future)
- [ ] Admin panel for content management
- [ ] User comments system
- [ ] Mobile PWA
- [ ] Advanced ML content moderation

---

**Contributors:** Kundan Bhaskar  
**License:** MIT  
**Repository:** [github.com/kundan007b/bhaskar-daily-ai-news](https://github.com/kundan007b/bhaskar-daily-ai-news)
