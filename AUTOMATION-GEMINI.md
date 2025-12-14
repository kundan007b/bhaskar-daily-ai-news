# 🤖 KB Tech News - n8n Automation with Google Gemini

Automated viral news detection with **FREE Google Gemini AI** for content generation.

---

## 🎯 Why Gemini?

| Feature | Gemini 1.5 Pro | GPT-4o |
|---------|----------------|--------|
| **Cost** | FREE (1500 requests/day) | $10-30/day |
| **Context** | 2M tokens | 128K tokens |
| **Speed** | 3-5 seconds | 5-10 seconds |
| **Quality** | Excellent for news | Excellent |
| **Hindi Support** | Native multilingual | Good but slower |

**Bottom line:** Gemini saves you ~$300-900/month while matching GPT-4 quality! 🎉

---

## 🚀 Quick Setup

### 1. Get Google Gemini API Key (FREE)

1. Visit: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy your key: `AIzaSy...`

**Free tier limits:**
- 1500 requests/day
- 1 million tokens/minute
- Perfect for 12-15 articles/day!

---

### 2. Configure n8n Credentials

Since you have n8n hosted on cloud, configure these credentials:

#### **A. Google Gemini API**

In your n8n instance:
1. Go to **Credentials** → **Create New** → **HTTP Query Auth**
2. Set:
   - **Name:** `Google Gemini API`
   - **Parameter Name:** `key`
   - **Parameter Value:** `AIzaSy...` (your API key from step 1)

#### **B. NewsAPI (News Source)**

1. Get free API key: https://newsapi.org/register
2. In n8n: **Credentials** → **HTTP Header Auth**
   - **Header Name:** `X-Api-Key`
   - **Header Value:** `YOUR_NEWSAPI_KEY`

#### **C. GitHub (Auto-Publishing)**

1. Create GitHub token: https://github.com/settings/tokens/new
2. Select scopes: `repo` (full control of private repositories)
3. In n8n: **Credentials** → **GitHub OAuth2 API** or **GitHub API**
   - **Access Token:** `ghp_...`

#### **D. Slack (Optional Notifications)**

1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Two options:
   - **Option A:** Set environment variable `SLACK_WEBHOOK_URL` in your n8n instance
   - **Option B:** Update the "Send Slack Notification" node URL directly in the workflow

---

### 3. Import Workflow

1. Download or copy the JSON from `.n8n/workflows/viral-news-publisher-gemini.json`
2. In your n8n cloud instance:
   - Go to **Workflows** → **Import from File**
   - Paste the JSON content
3. Link credentials to nodes:
   - "Generate English Article (Gemini)" → Select "Google Gemini API"
   - "Generate Hindi Article (Gemini)" → Select "Google Gemini API"
   - "Fetch Viral Tech News" → Select "NewsAPI" credential
   - All GitHub nodes → Select "GitHub OAuth2"
4. **Activate the workflow** (toggle in top-right corner)

---

### 4. Test the Workflow

1. Click **"Execute Workflow"** button
2. Watch nodes execute in real-time
3. Expected output:
   - ✅ Fetch news → 20 articles
   - ✅ Viral score → 2-5 articles above threshold (score ≥50)
   - ✅ Gemini generates English article (3-5 seconds)
   - ✅ Gemini generates Hindi article (3-5 seconds)
   - ✅ Downloads featured image
   - ✅ Commits 3 files to GitHub (EN post, HI post, image)
   - ✅ Slack notification sent

---

## 📊 Viral Score Algorithm

Each news item is scored (0-100+) based on:

| Factor | Points | Examples |
|--------|--------|----------|
| **Viral Keywords** | 20 each | "breaking", "exclusive", "billion", "hack", "unicorn", "leaked" |
| **India Relevance** | 30 | "India", "Bengaluru", "Delhi", "Mumbai" |
| **Tech Categories** | 15 each | AI, Startups, Cybersecurity, Gadgets, Cloud |
| **Recency** | 0-25 | <2hrs: 25pts, <6hrs: 15pts, <12hrs: 5pts |
| **Has Image** | 10 | Featured image available |

**Minimum threshold:** 50 points (only high-quality viral content gets published)

---

## 🎛️ Customization Options

### Adjust Viral Threshold

In the "Calculate Viral Score & Deduplicate" node, modify line:
```javascript
.filter(item => item.viralScore >= 50) // Change to 60, 70, or 40
```

**Recommendations:**
- **50-60:** High-quality viral content (default)
- **40-50:** More content, moderate viral potential
- **30-40:** Maximum content output

---

### Change Publishing Frequency

In "Schedule Every 2 Hours" node:
```json
"hoursInterval": 2  // Change to 1, 4, 6, 12
```

**Recommendations:**
- **1-2 hours:** Maximum freshness (high API usage)
- **4-6 hours:** Balanced approach
- **12 hours:** Conservative, low API usage

---

### Modify Author Assignment

In "Format Jekyll Posts" node, update the `authorMap`:
```javascript
const authorMap = {
  'AI': 'rajesh-kumar',
  'Startups': 'rajesh-kumar',
  'Cloud': 'rajesh-kumar',
  'Cybersecurity': 'ananya-singh',
  'Gadgets': 'ananya-singh'
};
```

Add more authors as you create them in `_authors/`.

---

### Use Gemini 1.5 Flash (Faster & Free)

For even faster generation, change both Gemini nodes URL from:
```
https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent
```
to:
```
https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
```

**Flash benefits:**
- 2x faster (1-2 seconds vs 3-5 seconds)
- Same quality for news articles
- Higher free tier limits (15 RPM vs 2 RPM)

---

### Adjust AI Creativity

In both Gemini nodes, modify the `generationConfig`:
```json
"generationConfig": {
  "temperature": 0.7,    // 0 = factual, 1 = creative
  "topK": 40,
  "topP": 0.95,
  "maxOutputTokens": 2048
}
```

**For strict news:** `temperature: 0.5`  
**For feature stories:** `temperature: 0.9`

---

## 🔍 How It Works

### Workflow Steps

1. **Schedule Trigger** → Runs every 2 hours
2. **Fetch Viral Tech News** → NewsAPI searches 20 recent articles
3. **Calculate Viral Score** → Scores each article (0-100+)
4. **Deduplicate** → Removes already-published URLs
5. **Generate English Article** → Gemini writes 400-600 word article
6. **Generate Hindi Article** → Gemini translates + localizes
7. **Format Jekyll Posts** → Creates front matter + markdown
8. **Download Image** → Fetches featured image
9. **Commit to GitHub** → Pushes 3 files (EN, HI, image)
10. **Notify Slack** → Success message with details

---

## 📝 Article Structure (Auto-Generated)

### Front Matter
```yaml
---
layout: post
title: "Article Title"
author: rajesh-kumar  # Auto-assigned by category
categories: ["AI", "Startups"]
image: /assets/images/posts/article-slug.jpg
lang: en  # or "hi" for Hindi
date: 2025-12-14
news_keywords: "ai, startup, funding, india"
description: "SEO meta description (155 chars)"
source_name: "TechCrunch"
source_url: "https://source-url.com"
---
```

### Article Body
Gemini generates:
1. **Lead Paragraph** - Who, what, when, where, why
2. **Context** - Background and significance
3. **Details** - Key facts, quotes, data
4. **Impact** - Why it matters to readers
5. **Closing** - Future outlook
6. **Attribution** - Link to original source

---

## 💰 Cost Estimate

### Monthly Costs (10 articles/day for 30 days)

| Service | Usage | Cost |
|---------|-------|------|
| **Gemini API** | 600 requests (300 EN + 300 HI) | **$0** (free tier) |
| **NewsAPI** | 360 requests | **$0** (free tier) |
| **GitHub Pages** | Static hosting | **$0** |
| **n8n Cloud** | Self-hosted | **$0-20/mo** |
| **Total** | | **$0-20/month** |

**Savings vs GPT-4:** $450/month → **$5,400/year saved!** 🤑

---

## 🧪 Testing & Validation

### Manual Test

In n8n, click **"Execute Workflow"** and verify:

- [ ] News articles fetched (should see 20 items)
- [ ] Viral scores calculated (2-5 items above threshold)
- [ ] English article generated (400-600 words)
- [ ] Hindi article generated (proper Devanagari)
- [ ] Jekyll front matter correct
- [ ] Image downloaded successfully
- [ ] Files committed to GitHub
- [ ] Site rebuilt at https://www.kbhaskar.tech
- [ ] Slack notification received

### Check GitHub Commits

Visit: https://github.com/kundan007b/bhaskar-daily-ai-news/commits/main

You should see commits like:
```
feat(post): publish [Article Title] (EN)
feat(post): publish [Article Title] (HI)
chore(assets): add featured image [slug]
```

### Verify Live Site

Check your published articles at:
- English: https://www.kbhaskar.tech
- Specific post: https://www.kbhaskar.tech/[category]/[slug]/

---

## 🚨 Troubleshooting

### Error: "API key not valid"

**Fix:**
1. Verify credential in n8n: Parameter Name = `key` (lowercase)
2. Test API directly:
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

### Error: "Resource exhausted" (Gemini)

**Fix:** You hit the free tier limit (1500 requests/day)
- Reduce frequency (check every 4-6 hours instead of 2)
- Use Gemini Flash (higher limits: 15 RPM)
- Upgrade to paid tier ($0.001/1K tokens)

### Error: GitHub file already exists

**Fix:** Workflow already published this article
- Check deduplication logic in "Calculate Viral Score" node
- Clear static data: Delete workflow → Reimport → Activate

### Empty or Poor Quality Article

**Fix:** Adjust Gemini prompt or temperature
- Lower temperature for more factual: `0.5`
- Add more context in prompt
- Use Gemini Pro instead of Flash

### Hindi Text Not Rendering

**Fix:** Ensure UTF-8 encoding
- Check font loaded: Noto Sans Devanagari
- Verify `lang: hi` in front matter
- Test locally: `bundle exec jekyll serve`

### Images Not Loading on Site

**Fix:**
- Verify image URL in source (not 404)
- Check GitHub commit includes image file
- Ensure `_config.yml` has: `url: "https://www.kbhaskar.tech"`

---

## 📊 Monitoring & Analytics

### n8n Execution History

In your n8n cloud instance:
1. Go to **Executions** tab
2. Filter by:
   - Status: Success, Error, Running
   - Date range
   - Workflow name
3. Click any execution to see detailed logs

### GitHub Actions

Monitor build status:
- https://github.com/kundan007b/bhaskar-daily-ai-news/actions
- Build time: ~30-60 seconds
- Check for build errors

### Google Search Console

Track indexing:
1. https://search.google.com/search-console
2. Check **Coverage** report
3. Verify **news-sitemap.xml** submitted

---

## 🔐 Security Best Practices

1. **API Keys** - Store in n8n credentials, never in workflow JSON
2. **GitHub Token** - Use fine-grained tokens with minimum permissions
3. **Webhook URLs** - Use HTTPS only for Slack
4. **Rotate Keys** - Change API keys every 90 days
5. **Backup** - Export workflow JSON regularly

---

## 📈 Expected Results

Once configured and activated:

**Every 2 hours:**
- ✅ n8n scans 20 tech news sources
- ✅ Finds 2-5 viral stories (score ≥50)
- ✅ Gemini writes English articles (3-5 seconds each)
- ✅ Gemini writes Hindi translations (3-5 seconds each)
- ✅ Downloads featured images
- ✅ Commits 6-15 files to GitHub
- ✅ GitHub Pages rebuilds site (~30 sec)
- ✅ Articles live at www.kbhaskar.tech

**Daily Output:**
- **10-15 articles** (5-8 per run × 2 runs)
- **English + Hindi** versions
- **Google News compliant**
- **Fully automated** 24/7

---

## 🎯 Advanced Optimizations

### Add More News Sources

Replace or supplement NewsAPI with:

**RSS Feeds:**
- TechCrunch: `https://techcrunch.com/feed/`
- YourStory: `https://yourstory.com/feed`
- Inc42: `https://inc42.com/feed/`

**Google News RSS:**
```
https://news.google.com/rss/search?q=technology+india&hl=en-IN&gl=IN&ceid=IN:en
```

Add **RSS Read** node instead of HTTP Request.

### Fact-Checking Layer

Insert after Gemini generation:
```json
{
  "name": "Fact-Check with Gemini",
  "parameters": {
    "jsonBody": {
      "contents": [{
        "parts": [{
          "text": "Fact-check this article for accuracy. Flag any unverified claims:\n\n{{ $json.englishArticle }}"
        }]
      }]
    }
  }
}
```

### Social Media Auto-Post

Add nodes to post to:
- **Twitter:** Use Twitter API node
- **LinkedIn:** Use LinkedIn API node
- **Telegram:** Use Telegram node

---

## 📚 Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **n8n Documentation:** https://docs.n8n.io
- **Jekyll Docs:** https://jekyllrb.com/docs/
- **Google News Guidelines:** https://support.google.com/news/publisher-center/answer/9606710
- **NewsAPI Docs:** https://newsapi.org/docs

---

## 🆘 Support

- **GitHub Issues:** https://github.com/kundan007b/bhaskar-daily-ai-news/issues
- **Email:** contact@kbhaskar.tech
- **n8n Community:** https://community.n8n.io

---

## ✅ Quick Reference

### API Keys Needed

| Service | Free Tier | Where to Get | Where to Add in n8n |
|---------|-----------|--------------|---------------------|
| **Gemini** | 1500 req/day | https://aistudio.google.com/app/apikey | HTTP Query Auth |
| **NewsAPI** | 100 req/day | https://newsapi.org/register | HTTP Header Auth |
| **GitHub** | Unlimited | https://github.com/settings/tokens/new | GitHub OAuth2 |
| **Slack** | Unlimited | https://api.slack.com/messaging/webhooks | Environment Var |

### Workflow Files

- **Workflow JSON:** `.n8n/workflows/viral-news-publisher-gemini.json`
- **Documentation:** This file (`AUTOMATION-GEMINI.md`)

### Import Workflow

1. Open your n8n cloud instance
2. Workflows → Import from File
3. Paste JSON from `.n8n/workflows/viral-news-publisher-gemini.json`
4. Link all credentials
5. Activate workflow

---

**🎉 You're all set! Your site will now auto-publish viral tech news 24/7 using FREE Gemini AI.**
