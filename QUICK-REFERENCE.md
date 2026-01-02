# Direct N8N to Azure Deployment - Quick Reference

## System Architecture

**N8N → Build → Azure** (No GitHub!)

## Required Tokens

1. **Azure Deployment Token**
   - Azure Portal → Static Web App → Manage deployment token
   - Use: Direct deployment to Azure

2. **AI API Key**
   - OpenAI: `sk-...` OR
   - Google Gemini: `AIza...`
   - Use: Content generation

## N8N Environment Variables

```bash
AZURE_DEPLOYMENT_TOKEN=xxxxxxxxx
AZURE_APP_NAME=kb-tech-news
OPENAI_API_KEY=sk-xxxxx  # or GOOGLE_API_KEY
```

## N8N Workflow Import

1. Download: `.github/n8n-workflow-direct-azure.json`
2. N8N → Import from File
3. Set credentials (OpenAI/Gemini)
4. Set environment variables
5. Activate workflow

## System Requirements (Self-Hosted N8N)

```bash
# Install Ruby + Jekyll
sudo apt-get install -y ruby-full build-essential
sudo gem install jekyll bundler

# Install Azure CLI
npm install -g @azure/static-web-apps-cli

# Verify
ruby --version   # 3.0+
jekyll --version # 4.3+
swa --version    # Latest
```

## Testing Commands

```bash
# Test Jekyll build
cd /tmp/blog-site
bundle install
bundle exec jekyll build
ls -la _site/

# Test Azure deployment
swa deploy _site \
  --deployment-token YOUR_TOKEN \
  --env production
```

## Workflow Execution Flow

```
Schedule (Every 4h) 
  → AI (30-60s)
  → Build File (5s)
  → Save File (5s)
  → Jekyll Build (30-60s)
  → Azure Deploy (30-60s)
  → ✅ Live (Total: 2-3 min)
```

## Monitoring

**N8N:**
- Executions tab → View history
- Check each node's output
- Green = success, Red = failure

**File System:**
```bash
ls -lt /tmp/blog-site/_posts/ | head  # Recent posts
```

**Azure:**
- Portal → Static Web App → Overview
- Check deployment history
- Visit: https://kbhaskar.tech

**Sitemaps:**
- https://kbhaskar.tech/sitemap.xml
- https://kbhaskar.tech/news-sitemap.xml

## Common Issues

| Issue | Solution |
|-------|----------|
| Jekyll build failed | Run `bundle install` in /tmp/blog-site |
| Azure deploy failed | Verify AZURE_DEPLOYMENT_TOKEN |
| AI response invalid | Check API key, verify prompt |
| File not saved | Check /tmp/blog-site mount |

## Daily Checklist

- [ ] N8N workflow running (6 executions expected)
- [ ] 6 new posts in `_posts/`
- [ ] Site updated: https://kbhaskar.tech
- [ ] News sitemap updated (48h window)
- [ ] No errors in N8N executions

## Cost (Minimal Setup)

- VPS: $5-10/month (self-hosted N8N)
- AI: $0 (Gemini free tier)
- GitHub: $0
- Azure: $0
- **Total: $5-10/month**

## Documentation

- **Quick Setup:** [SETUP-GUIDE.md](SETUP-GUIDE.md)
- **Complete Setup:** [README-AUTONOMOUS-SETUP.md](README-AUTONOMOUS-SETUP.md)
- **N8N Details:** [.github/N8N-INTEGRATION.md](.github/N8N-INTEGRATION.md)

## Quick Deploy

```bash
# 1. Prepare Jekyll site
cp -r /path/to/bhaskar-daily-ai-news /tmp/blog-site
cd /tmp/blog-site
bundle install

# 2. Set up N8N (Docker)
docker run -d --name n8n -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v /tmp/blog-site:/tmp/blog-site \
  docker.n8n.io/n8nio/n8n

# 3. Install deps in N8N container
docker exec -it n8n sh -c "apk add ruby ruby-dev build-base && gem install jekyll bundler && npm install -g @azure/static-web-apps-cli"

# 4. Import workflow
# N8N UI → Import → n8n-workflow-direct-azure.json

# 5. Configure env vars & activate
# Done! 🚀
```

## Support

- N8N Docs: https://docs.n8n.io
- Azure Docs: https://learn.microsoft.com/azure/static-web-apps
