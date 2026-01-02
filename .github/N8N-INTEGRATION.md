# N8N Integration Guide for Autonomous Article Publishing

This guide explains how to set up an N8N workflow to automatically publish 6 articles daily to your Jekyll blog, directly deploying to Azure Static Web Apps.

## Overview

**Direct N8N → Azure Architecture:**

```
N8N Workflow (every 4 hours)
  ↓
1. AI generates article content
  ↓
2. Create markdown file locally
  ↓
3. Build Jekyll site in N8N
  ↓
4. Deploy directly to Azure Static Web Apps
  ↓
Live site updated!
```

**Benefits:**
- ✅ No GitHub needed (fully self-contained)
- ✅ Complete control in N8N
- ✅ All files managed locally
- ✅ Fastest deployment (direct to Azure)

## Prerequisites

### 1. Azure Setup

Get Azure Static Web Apps deployment token:
1. Go to Azure Portal
2. Navigate to your Static Web App
3. Click "Manage deployment token"
4. Copy the token
5. Save securely for use in N8N

### 2. N8N Setup

Install required tools in N8N environment:
- **Ruby** (for Jekyll)
- **Bundler** (for Jekyll dependencies)
- **Azure Static Web Apps CLI** (for deployment)

For N8N Cloud: Use Docker container or shell commands
For Self-hosted N8N: Install on host system

## N8N Workflow Structure

### Complete Workflow (5 nodes)

```
[Schedule Trigger] → [AI Content] → [Build Post File] → [Save File] → [Build Jekyll] → [Deploy to Azure]
```

### Node 1: Schedule Trigger (Cron)

**Type:** Schedule Trigger  
**Schedule:** 6 times daily at 00:00, 04:00, 08:00, 12:00, 16:00, 20:00 IST

**Settings:**
```
Trigger Interval: Cron
Cron Expression: 0 0,4,8,12,16,20 * * *
Timezone: Asia/Kolkata
```

### Node 2: AI Content Generation

**Type:** OpenAI / Google Gemini / Anthropic Claude

**Prompt Template:**
```
Generate a unique, newsworthy technology article for an Indian audience following Google News guidelines.

REQUIREMENTS:
- Topic: Choose from trending tech news in India (AI, startups, gadgets, cybersecurity, cloud, software)
- Angle: Indian perspective, local relevance
- Length: 1200-1500 words
- Tone: Professional, journalistic, factual
- Structure: Introduction, 3-4 main sections with headers, Key Takeaways, Conclusion
- SEO: Optimized title (50-60 chars), meta description (150-160 chars)
- Keywords: 5-7 relevant keywords naturally integrated

OUTPUT FORMAT (JSON):
{
  "title": "Engaging title with primary keyword",
  "title_hi": "हिंदी में शीर्षक",
  "excerpt": "Compelling 150-160 character summary for meta description",
  "excerpt_hi": "हिंदी में सारांश",
  "content": "Full markdown article with ## headers, bullet points, links",
  "content_hi": "पूर्ण हिंदी लेख markdown में",
  "category": "ai|technology|startups|cybersecurity|gadgets|software|cloud|data-science",
  "tags": "tag1, tag2, tag3, tag4, tag5",
  "keywords": "keyword1, keyword2, keyword3, keyword4, keyword5",
  "author": "rajesh-kumar",
  "image": "https://example.com/relevant-image.jpg"
}

Make each article unique and newsworthy. Focus on recent events (last 24-48 hours).
```

**Output:** Store in `{{ $json }}`

### Node 3: Create Post File (Code Node)

**Type:** Code (JavaScript)

```javascript
// Get current date for filename
const now = new Date();
const dateStr = now.toISOString().split('T')[0]; // YYYY-MM-DD

// Get article data from previous node
const article = $input.first().json;

// Create slug from title
function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

const slug = slugify(article.title);
const filename = `${dateStr}-${slug}.md`;

// Create frontmatter
const tags = article.tags.split(',').map(t => `  - ${t.trim()}`).join('\n');
const keywords = article.keywords.split(',').map(k => `  - ${k.trim()}`).join('\n');

const frontmatter = `---
layout: post
title: "${article.title}"
title_hi: "${article.title_hi}"
excerpt: "${article.excerpt}"
excerpt_hi: "${article.excerpt_hi}"
author: ${article.author}
date: ${now.toISOString().replace('T', ' ').substring(0, 19)} +0530
categories:
  - ${article.category}
tags:
${tags}
keywords:
${keywords}
${article.image ? `image: "${article.image}"` : ''}
lang: en
lang_alternate: hi
---

${article.content}

## हिंदी में (In Hindi)

${article.content_hi}
`;

return {
  json: {
    filename: filename,
    content: frontmatter,
    filepath: `_posts/${filename}`,
    ...article
  }
};
```

### Node 4: Save Post File (Execute Command)

**Type:** Execute Command

**Commands:**

```bash
#!/bin/bash
set -e

# Working directory for blog
WORK_DIR="/tmp/blog-site"
mkdir -p $WORK_DIR
cd $WORK_DIR

# Initialize if needed (first run)
if [ ! -f "_config.yml" ]; then
  echo "Setting up Jekyll site structure..."
  echo "Mount your Jekyll site at $WORK_DIR or copy files there"
  exit 1
fi

# Create _posts directory if not exists
mkdir -p _posts

# Save the new post
FILEPATH="{{ $json.filepath }}"
echo '{{ $json.content }}' > "$FILEPATH"

echo "✅ Post file created: $FILEPATH"
ls -lh "$FILEPATH"
```

**Important:** Mount your Jekyll site to `/tmp/blog-site` in N8N:
- Docker: `-v /path/to/your/jekyll/site:/tmp/blog-site`
- Or copy your Jekyll files to `/tmp/blog-site` before first run

### Node 5: Build Jekyll Site (Execute Command)

**Type:** Execute Command

**Commands:**

```bash
#!/bin/bash
set -e

WORK_DIR="/tmp/blog-site"
cd $WORK_DIR

echo "📦 Installing Jekyll dependencies..."
bundle install --quiet

echo "🔨 Building Jekyll site..."
JEKYLL_ENV=production bundle exec jekyll build

# Verify build
if [ -d "_site" ]; then
  FILE_COUNT=$(find _site -type f | wc -l)
  echo "✅ Jekyll build successful: $FILE_COUNT files generated"
else
  echo "❌ Jekyll build failed: _site directory not found"
  exit 1
fi
```

**Alternative: Using Docker**

If you prefer containerized builds:

```bash
docker run --rm \
  -v /tmp/blog-site:/srv/jekyll \
  jekyll/jekyll:4.3 \
  jekyll build
```

### Node 6: Deploy to Azure

### Node 6: Deploy to Azure

**Type:** Execute Command

**Commands:**

```bash
#!/bin/bash
set -e

WORK_DIR="/tmp/blog-site"
cd $WORK_DIR

echo "🚀 Deploying to Azure Static Web Apps..."

# Deploy using Azure Static Web Apps CLI
swa deploy _site \
  --deployment-token "{{ $env.AZURE_DEPLOYMENT_TOKEN }}" \
  --env production \
  --no-use-keychain

if [ $? -eq 0 ]; then
  echo "✅ Deployment to Azure successful!"
  echo "Site: https://{{ $env.AZURE_APP_NAME }}.azurestaticapps.net"
  echo "Custom domain: https://kbhaskar.tech"
else
  echo "❌ Deployment failed"
  exit 1
fi
```

**Environment Variables:**
- `AZURE_DEPLOYMENT_TOKEN`: Your Azure Static Web Apps deployment token
- `AZURE_APP_NAME`: Your Azure app name (e.g., kb-tech-news)

### Complete N8N Workflow Summary

```
┌─────────────────────┐
│  Cron Schedule      │  Every 4 hours (6x daily)
│  0,4,8,12,16,20h    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AI Content Gen     │  OpenAI/Gemini/Claude
│  Generate Article   │  JSON output
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Code Node          │  Create markdown file
│  Build frontmatter  │  Generate filename
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Execute Command    │  Git clone/pull
│  Git Operations     │  Commit & push
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Execute Command    │  bundle exec jekyll build
│  Build Jekyll       │  Creates _site/ folder
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Execute Command    │  swa deploy
│  Deploy to Azure    │  Direct upload
└──────────┬──────────┘
           │
           ▼
     ✅ Live Site Updated!
```

## Environment Variables in N8N

Set these in N8N Settings → Environments:

```bash
# Azure Static Web Apps
AZURE_DEPLOYMENT_TOKEN=your_azure_deployment_token_here
AZURE_APP_NAME=kb-tech-news

# AI API Keys (if not using built-in credentials)
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
ANTHROPIC_API_KEY=sk-ant-...
```
```

## Installation Steps

### Step 1: Install N8N

**Option A: N8N Cloud**
- Sign up at https://n8n.io
- No installation needed
- Limited execution time on free tier

**Option B: Self-Hosted (Docker)**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e TZ=Asia/Kolkata \
  docker.n8n.io/n8nio/n8n
```

**Option C: Self-Hosted (npm)**
```bash
npm install -g n8n
n8n start
```

### Step 2: Install System Dependencies

For self-hosted N8N, install on the host system:

```bash
# Ruby for Jekyll
sudo apt-get update
sudo apt-get install -y ruby-full build-essential zlib1g-dev git

# Jekyll and Bundler
sudo gem install jekyll bundler

# Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Verify installations
ruby --version
jekyll --version
swa --version
```

### Step 3: Import N8N Workflow

Download the complete workflow JSON (see below) and import into N8N:

1. Open N8N
2. Click "Import from File" or "Import from URL"
3. Upload the workflow JSON
4. Configure credentials and environment variables
5. Activate the workflow

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title` | String | Article title in English | "AI Breakthrough in Healthcare" |
| `title_hi` | String | Article title in Hindi | "स्वास्थ्य सेवा में एआई की बड़ी सफलता" |
| `excerpt` | String | Short summary (150-160 chars) | "New AI system detects diseases..." |
| `excerpt_hi` | String | Hindi summary | "नई एआई प्रणाली बीमारियों का पता..." |
| `content` | String | Full article in Markdown | "## Introduction\n\nThe new AI..." |
| `content_hi` | String | Full article in Hindi (Markdown) | "## परिचय\n\nनई एआई..." |
| `category` | String | Primary category | "ai", "technology", "startups" |
| `tags` | String | Comma-separated tags | "artificial intelligence, healthcare, innovation" |
| `keywords` | String | SEO keywords (comma-separated) | "AI, machine learning, medical AI" |
| `author` | String | Author slug | "rajesh-kumar" or "ananya-singh" |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `image` | String | Featured image URL |

## Categories

Available categories (must match one):
- `ai` - Artificial Intelligence
- `technology` - General Technology
- `startups` - Startup News
- `cybersecurity` - Security News
- `gadgets` - Hardware & Devices
- `software` - Software & Apps
- `cloud` - Cloud Computing
- `data-science` - Data & Analytics

## Content Guidelines for AI Generation

### SEO Optimization
1. **Title:** 50-60 characters, include primary keyword
2. **Excerpt:** 150-160 characters, compelling summary
3. **Keywords:** 5-8 relevant keywords
4. **Content:** 800-1500 words for optimal SEO
5. **Headers:** Use H2 (##) and H3 (###) for structure
6. **Links:** Include 2-3 internal/external links
7. **Images:** Use descriptive alt text

### Google News Compliance
1. **Originality:** Content must be unique
2. **Accuracy:** Fact-check all claims
3. **Attribution:** Cite sources for news
4. **Timeliness:** Focus on recent events (24-48 hours)
5. **No promotional content:** Focus on newsworthy information
6. **Author bylines:** Properly attributed (auto-added)
7. **Publish date:** Auto-generated (current timestamp)

### Content Structure (Markdown)
```markdown
## Introduction
Brief overview of the topic

## Main Content
### Subtopic 1
Details...

### Subtopic 2
More details...

## Key Takeaways
- Point 1
- Point 2
- Point 3

## Conclusion
Final thoughts
```

## N8N AI Prompt Template

```
Generate a news article about [TOPIC] following these requirements:

STRUCTURE:
- Title: Catchy, SEO-friendly, 50-60 characters
- Excerpt: Compelling summary in 150-160 characters
- Content: 1000-1200 words with Introduction, 3-4 main sections, Key Takeaways, Conclusion
- Use Markdown headers (## and ###)
- Include bullet points for readability

SEO:
- Primary keyword: [KEYWORD]
- Include 5-7 related keywords
- Natural keyword density (1-2%)
- Meta description optimized

LANGUAGE:
- Provide both English and Hindi versions
- Hindi should be natural translation, not literal
- Maintain professional, journalistic tone

CATEGORY: [Select from: ai, technology, startups, cybersecurity, gadgets, software, cloud, data-science]

TAGS: Suggest 5-7 relevant tags (comma-separated)

OUTPUT FORMAT: JSON with fields matching the schema above
```

## Sample N8N AI Node Output

```json
{
  "title": "Google Launches New AI-Powered Search Features in India",
  "title_hi": "गूगल ने भारत में नई एआई-संचालित खोज सुविधाएं लॉन्च कीं",
  "excerpt": "Google introduces AI-enhanced search capabilities specifically designed for Indian users, featuring multilingual support and local context understanding.",
  "excerpt_hi": "गूगल ने भारतीय उपयोगकर्ताओं के लिए विशेष रूप से डिज़ाइन की गई एआई-संवर्धित खोज क्षमताओं को पेश किया है।",
  "content": "## Introduction\n\nGoogle has announced a major update...",
  "content_hi": "## परिचय\n\nगूगल ने एक बड़े अपडेट की घोषणा की है...",
  "category": "ai",
  "tags": "Google, AI, Search, India, Machine Learning, NLP",
  "keywords": "Google AI, AI search India, multilingual search, Google India, AI features",
  "author": "rajesh-kumar",
  "image": "https://example.com/google-ai-search.jpg"
}
```

## Testing

### Test Individual Components

**1. Test AI Content Generation**
- Run workflow manually with Schedule node disabled
- Check AI output is valid JSON
- Verify all required fields present

**2. Test File Creation**
- Check Code node generates valid frontmatter
- Verify filename follows YYYY-MM-DD-slug.md format
- Ensure content is properly escaped

**3. Test Git Operations**
- Manually run Git commands in terminal
- Verify repository clones successfully
- Check file is committed and pushed

**4. Test Jekyll Build**
```bash
cd /tmp/blog-repo
bundle install
bundle exec jekyll build
ls -la _site/
```

**5. Test Azure Deployment**
```bash
cd /tmp/blog-repo
swa deploy _site --deployment-token YOUR_TOKEN --env production
```

### Full Workflow Test

**Option 1: Manual Trigger in N8N**
1. Open workflow in N8N
2. Click "Execute Workflow" button
3. Monitor each node's output
4. Check for errors in any step
5. Verify site updates in Azure

**Option 2: Test with Specific Article**

Modify AI node to use static content for testing:

```json
{
  "title": "Test Article: N8N Direct Azure Deployment",
  "title_hi": "परीक्षण लेख: N8N प्रत्यक्ष Azure तैनाती",
  "excerpt": "Testing the complete autonomous publishing workflow with direct Azure deployment from N8N.",
  "excerpt_hi": "N8N से सीधे Azure तैनाती के साथ पूर्ण स्वायत्त प्रकाशन वर्कफ़्लो का परीक्षण।",
  "content": "## Introduction\n\nThis is a test article to verify the N8N workflow.\n\n## Test Content\n\nThe workflow should:\n- Generate this markdown file\n- Commit to GitHub\n- Build Jekyll site\n- Deploy to Azure\n\n## Conclusion\n\nIf you see this article on the live site, the workflow is successful!",
  "content_hi": "## परिचय\n\nयह N8N वर्कफ़्लो को सत्यापित करने के लिए एक परीक्षण लेख है।\n\n## परीक्षण सामग्री\n\nवर्कफ़्लो को चाहिए:\n- इस markdown फ़ाइल को उत्पन्न करें\n- GitHub पर प्रतिबद्ध करें\n- Jekyll साइट बनाएं\n- Azure पर तैनात करें\n\n## निष्कर्ष\n\nयदि आप इस लेख को लाइव साइट पर देखते हैं, तो वर्कफ़्लो सफल है!",
  "category": "technology",
  "tags": "test, automation, n8n, azure",
  "keywords": "n8n, azure, automation, jekyll, deployment",
  "author": "rajesh-kumar",
  "image": "https://picsum.photos/1200/630"
}
```

## Scheduling Strategy

### 6 Posts Per Day Schedule (IST)
- **00:00** - Night readers, tech enthusiasts
- **04:00** - Early morning, international audience
- **08:00** - Morning commute, peak readership
- **12:00** - Lunch break, high engagement
- **16:00** - Afternoon, office readers
- **20:00** - Evening, leisure reading

### N8N Cron Expressions
```
0 0,4,8,12,16,20 * * *
```

Or individual schedules:
```
0 0 * * *   # Midnight
0 4 * * *   # 4 AM
0 8 * * *   # 8 AM
0 12 * * *  # Noon
0 16 * * *  # 4 PM
0 20 * * *  # 8 PM
```

## Monitoring & Logs

### N8N Execution Logs

**View in N8N:**
1. Executions tab in N8N
2. Click on any execution to see details
3. Check each node's output
4. View errors if any failed

**Execution History:**
- Success: Green checkmark ✅
- Failure: Red X ❌
- Running: Blue spinner 🔄

### Verify Deployment Success

**Check GitHub:**
```bash
# Clone repository
git clone https://github.com/kundan007b/bhaskar-daily-ai-news.git
cd bhaskar-daily-ai-news

# Check recent posts
ls -lt _posts/ | head -10

# View git log
git log --oneline -10
```

**Check Azure:**
- Azure Portal → Static Web Apps → Deployment History
- Or visit your live site: `https://kbhaskar.tech`

**Check Sitemaps:**
- https://kbhaskar.tech/sitemap.xml
- https://kbhaskar.tech/news-sitemap.xml
- https://kbhaskar.tech/feed.xml

### Error Handling

**Common Issues:**

| Error | Cause | Solution |
|-------|-------|----------|
| Git authentication failed | Invalid GITHUB_TOKEN | Regenerate token with `repo` scope |
| Jekyll build failed | Missing dependencies | Install Ruby, bundler, jekyll |
| Azure deployment failed | Invalid token | Get new deployment token from Azure Portal |
| AI response not JSON | API error or wrong prompt | Check AI model settings, verify prompt |
| File already exists | Duplicate slug | Add timestamp to filename |

### Alerts & Notifications

**Add Error Notification (Optional):**

Add an email/Slack node after each critical step:

```
[Node] → IF Error → [Send Alert] → Stop
         ELSE → [Continue to next node]
```

Example Slack notification:
```json
{
  "text": "❌ Blog deployment failed at step: {{ $node.name }}",
  "attachments": [
    {
      "color": "danger",
      "fields": [
        {
          "title": "Error",
          "value": "{{ $json.error }}",
          "short": false
        },
        {
          "title": "Article",
          "value": "{{ $json.title }}",
          "short": true
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Workflow Doesn't Execute
- **Check:** N8N workflow is activated
- **Check:** Cron schedule is correct (timezone: Asia/Kolkata)
- **Check:** N8N has sufficient execution credits (if cloud)
- **Solution:** Manually trigger to test

### AI Node Fails
- **Error:** Rate limit exceeded
  - **Solution:** Reduce frequency or upgrade API plan
- **Error:** Invalid JSON response
  - **Solution:** Add JSON parsing validation, retry logic
- **Error:** Timeout
  - **Solution:** Increase timeout in node settings

### Git Operations Fail
- **Error:** Authentication failed
  - **Solution:** Verify GITHUB_TOKEN is correct and has `repo` scope
- **Error:** Repository not found
  - **Solution:** Check repository name/URL
- **Error:** Merge conflict
  - **Solution:** Pull latest changes before commit

### Jekyll Build Fails
- **Error:** `bundle: command not found`
  - **Solution:** Install bundler: `gem install bundler`
- **Error:** Missing gem dependencies
  - **Solution:** Run `bundle install` in repository
- **Error:** Invalid frontmatter syntax
  - **Solution:** Check YAML formatting, escape quotes

### Azure Deployment Fails
- **Error:** Invalid deployment token
  - **Solution:** Regenerate token in Azure Portal
- **Error:** `swa: command not found`
  - **Solution:** Install Azure Static Web Apps CLI: `npm install -g @azure/static-web-apps-cli`
- **Error:** Upload timeout
  - **Solution:** Check network connectivity, retry deployment

### Posts Not Appearing on Site
- **Check:** File created in `_posts/` with correct date format
- **Check:** Jekyll build completed successfully
- **Check:** Azure deployment successful
- **Check:** Browser cache (hard refresh: Ctrl+F5)
- **Check:** Sitemap: https://kbhaskar.tech/sitemap.xml

### Performance Issues
- **Slow execution:** Each workflow takes 5-10 minutes
  - Normal for full build + deploy cycle
  - Optimize by caching bundle install
- **High CPU usage:** Jekyll build is CPU intensive
  - Consider using more powerful N8N host
  - Or use GitHub Actions for build (hybrid approach)

## Advanced: Content Variation

### Topic Rotation
Configure N8N to rotate through topics:
- Day 1: AI/ML focus
- Day 2: Startup news
- Day 3: Cybersecurity
- Day 4: Gadgets/Hardware
- Day 5: Cloud/Enterprise
- Day 6: Software/Apps
- Day 7: Data Science/Analytics

### Trending Topics Integration
Add N8N nodes to:
1. Fetch Google Trends API
2. Scrape tech news aggregators
3. Monitor Twitter/Reddit trending topics
4. Generate articles on trending subjects

### Quality Control
Add validation nodes:
- Plagiarism check (copyscape API)
- Grammar check (Grammarly API)
- Readability score (Flesch-Kincaid)
- Fact-checking prompts

## Security Best Practices

1. **Never commit tokens** to repository
2. **Use environment variables** in N8N
3. **Rotate tokens** every 90 days
4. **Monitor API usage** for anomalies
5. **Enable 2FA** on GitHub account
6. **Audit workflow runs** monthly

## Backup & Recovery

### Automatic Backups
All posts are in Git, so:
- Every commit is a backup point
- Can roll back to any previous state
- Clone repository for local backup

### Disaster Recovery
```bash
# Clone repository
git clone https://github.com/kundan007b/bhaskar-daily-ai-news.git

# Restore to specific date
git checkout $(git rev-list -n 1 --before="2026-01-01" main)
```

## Cost Estimation

### N8N Costs

**N8N Cloud:**
- Free: 5,000 workflow executions/month (not enough for 6x daily = 180/month)
- Starter: $20/month - 2,500 executions/month
- Pro: $50/month - Unlimited executions
- **Recommendation:** Self-host for free

**Self-Hosted N8N:**
- VPS cost: $5-10/month (DigitalOcean, Linode, Hetzner)
- 1 vCPU, 1-2GB RAM sufficient
- **Total: $5-10/month**

### AI API Costs (6 articles/day = 180/month)

**OpenAI GPT-4 Turbo:**
- Input: ~$0.01 per 1K tokens
- Output: ~$0.03 per 1K tokens
- Average per article: $0.10 (1500 words)
- **Monthly: ~$18**

**Google Gemini Pro:**
- Free tier: 60 requests/minute
- Paid: $0.00025 per 1K characters
- **Monthly: ~$5-10** (or free)

**Anthropic Claude:**
- Similar to GPT-4 pricing
- **Monthly: ~$15-20**

### Infrastructure Costs

**GitHub:**
- Public repository: Free
- Private repository: Free (for personal accounts)
- **Total: $0**

**Azure Static Web Apps:**
- Free tier: 100 GB bandwidth/month
- Standard: $9/month (if needed)
- **Total: $0** (free tier sufficient)

### Total Monthly Cost

| Component | Cost |
|-----------|------|
| N8N (self-hosted VPS) | $5-10 |
| AI API (Gemini Pro) | $0-10 |
| GitHub | $0 |
| Azure Static Web Apps | $0 |
| **TOTAL** | **$5-20/month** |

**Cost Optimization:**
- Use Gemini Pro (free tier) instead of GPT-4
- Self-host N8N on cheap VPS
- Stay within Azure free tier limits
- **Possible to run for $5/month!**

## Next Steps

1. Set up N8N instance (cloud or self-hosted)
2. Create GitHub Personal Access Token
3. Build N8N workflow following this guide
4. Test with manual workflow dispatch
5. Enable cron schedule for automation
6. Monitor for 1 week to ensure stability
7. Optimize based on analytics
