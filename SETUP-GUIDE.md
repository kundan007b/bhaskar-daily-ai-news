# N8N Autonomous Publishing - Setup Guide

## Quick Overview

**System:** N8N → Azure (No GitHub needed!)

```
N8N Workflow
  ↓
AI Generates Content
  ↓
Creates Markdown File Locally  
  ↓
Builds Jekyll Site
  ↓
Deploys to Azure
  ↓
Live Site!
```

## Requirements

- N8N (self-hosted or cloud)
- Azure Static Web App
- OpenAI/Gemini API key

## Setup Steps

### 1. Install N8N

**Docker (Recommended):**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v /path/to/jekyll/site:/tmp/blog-site \
  -e TZ=Asia/Kolkata \
  docker.n8n.io/n8nio/n8n
```

**Key:** Mount your Jekyll site to `/tmp/blog-site`

### 2. Install Dependencies (in N8N container)

```bash
# Enter N8N container
docker exec -it n8n /bin/sh

# Install Ruby + Jekyll
apk add ruby ruby-dev build-base
gem install jekyll bundler

# Install Azure CLI
npm install -g @azure/static-web-apps-cli

# Exit container
exit
```

### 3. Prepare Jekyll Site

Copy your entire Jekyll site to `/tmp/blog-site`:
```bash
cp -r /path/to/bhaskar-daily-ai-news /tmp/blog-site
```

### 4. Get Azure Deployment Token

1. Azure Portal → Your Static Web App
2. Click "Manage deployment token"
3. Copy the token

### 5. Import N8N Workflow

1. Download: `.github/n8n-workflow-direct-azure.json`
2. N8N UI → Import from File
3. Configure credentials (OpenAI or Gemini)
4. Set environment variables:
   ```
   AZURE_DEPLOYMENT_TOKEN=your_token
   AZURE_APP_NAME=kb-tech-news
   OPENAI_API_KEY=sk-... (or GOOGLE_API_KEY)
   ```
5. Activate workflow

### 6. Test

Click "Execute Workflow" in N8N and watch:
- AI generates article ✅
- File saved to `/tmp/blog-site/_posts/` ✅
- Jekyll builds site ✅
- Azure deployment succeeds ✅
- Visit https://kbhaskar.tech ✅

## Workflow Details

### Node 1: Schedule
Runs every 4 hours: 00:00, 04:00, 08:00, 12:00, 16:00, 20:00 IST

### Node 2: AI Content
OpenAI/Gemini generates article JSON with title, content, Hindi translation

### Node 3: Build File
JavaScript creates markdown with frontmatter

### Node 4: Save File
Saves to `/tmp/blog-site/_posts/YYYY-MM-DD-slug.md`

### Node 5: Jekyll Build
Runs `bundle exec jekyll build` → creates `_site/`

### Node 6: Azure Deploy
Runs `swa deploy _site` → pushes to Azure

## Monitoring

**N8N Executions Tab:**
- Green ✅ = Success
- Red ❌ = Failed (check logs)

**Check Live Site:**
- https://kbhaskar.tech
- https://kbhaskar.tech/news-sitemap.xml

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Jekyll build fails | Run `bundle install` in `/tmp/blog-site` |
| Azure deploy fails | Check AZURE_DEPLOYMENT_TOKEN is correct |
| AI returns invalid JSON | Check API key, verify prompt |
| File not created | Check `/tmp/blog-site` is mounted correctly |

## File Structure

```
/tmp/blog-site/          ← Your Jekyll site
├── _config.yml
├── _posts/              ← New articles go here
├── _site/               ← Built site (auto-generated)
├── Gemfile
└── ...other Jekyll files
```

## Cost

- N8N (self-hosted): $5-10/month (VPS)
- AI API (Gemini free tier): $0
- Azure Static Web Apps: $0
- **Total: $5-10/month**

## Backup

Files are only stored locally in `/tmp/blog-site`. To backup:

```bash
# Backup entire site
tar -czf blog-backup-$(date +%Y%m%d).tar.gz /tmp/blog-site

# Or use rsync to remote server
rsync -av /tmp/blog-site/ user@server:/backups/blog/
```

Consider setting up automated backups via cron or another N8N workflow.

## Support

- Full Documentation: [N8N-INTEGRATION.md](N8N-INTEGRATION.md)
- N8N Docs: https://docs.n8n.io
- Azure Docs: https://learn.microsoft.com/azure/static-web-apps
