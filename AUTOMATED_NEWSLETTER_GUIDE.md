# Automated Newsletter System - Implementation Guide

Send new blog posts automatically to your subscribers via email!

## Overview

When you publish a new post, this system will:
1. Detect the new post
2. Get list of subscribers from GitHub Issues
3. Send personalized email to each subscriber via EmailJS
4. Track sent newsletters

## Prerequisites

- ✅ EmailJS account (you have this)
- ✅ Subscribers stored in GitHub Issues with `subscribe` label
- ⏳ New EmailJS template for newsletters

## Step 1: Create Newsletter Email Template

1. Go to [EmailJS Dashboard](https://dashboard.emailjs.com/admin/templates)
2. Click **Create New Template**
3. **Template ID**: `template_newsletter` (you'll use this in code)

### Template Configuration

**Subject:**
```
{{site_name}}: {{post_title}}
```

**Message Body (HTML):**
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
        .content { padding: 30px 20px; background: #fff; }
        .post-image { width: 100%; max-width: 600px; height: auto; border-radius: 8px; margin: 20px 0; }
        .cta-button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 New Post from {{site_name}}</h1>
        </div>
        <div class="content">
            <h2>{{post_title}}</h2>
            
            <p style="color: #666; font-size: 14px;">
                <strong>Category:</strong> {{post_category}} | 
                <strong>Date:</strong> {{post_date}}
            </p>
            
            {{#post_image}}
            <img src="{{post_image}}" alt="{{post_title}}" class="post-image" />
            {{/post_image}}
            
            <p>{{post_summary}}</p>
            
            <a href="{{post_url}}" class="cta-button">Read Full Article →</a>
            
            <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                This is an automated newsletter from Bhaskar Daily News. 
                You're receiving this because you subscribed at {{site_url}}.
            </p>
        </div>
        <div class="footer">
            <p>© Bhaskar Daily News • Written by KB</p>
            <p>
                <a href="{{site_url}}/about" style="color: #667eea; text-decoration: none;">About</a> | 
                <a href="{{site_url}}/contact" style="color: #667eea; text-decoration: none;">Contact</a> | 
                <a href="mailto:{{site_email}}?subject=Unsubscribe" style="color: #667eea; text-decoration: none;">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>
```

**Template Variables:**
- `{{to_email}}` - Recipient email
- `{{site_name}}` - Bhaskar Daily News
- `{{site_url}}` - https://www.kbhaskar.tech
- `{{site_email}}` - contact@kbhaskar.tech
- `{{post_title}}` - Article title
- `{{post_category}}` - Article category
- `{{post_date}}` - Publication date
- `{{post_summary}}` - Article summary/excerpt
- `{{post_url}}` - Full URL to article
- `{{post_image}}` - Article featured image URL

4. Click **Save**

## Step 2: Create GitHub Action Workflow

Create `.github/workflows/send-newsletter.yml`:

```yaml
name: Send Newsletter

on:
  push:
    branches: [ main ]
    paths:
      - '_posts/**'
  workflow_dispatch:

jobs:
  send-newsletter:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, 'post:') || github.event_name == 'workflow_dispatch'
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 2
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install @emailjs/nodejs node-fetch
      
      - name: Get new/modified posts
        id: get-posts
        run: |
          # Get list of new or modified posts
          git diff --name-only HEAD~1 HEAD -- _posts/ > changed_files.txt
          echo "Changed files:"
          cat changed_files.txt
      
      - name: Send newsletters
        env:
          EMAILJS_PUBLIC_KEY: ${{ secrets.EMAILJS_PUBLIC_KEY }}
          EMAILJS_PRIVATE_KEY: ${{ secrets.EMAILJS_PRIVATE_KEY }}
          EMAILJS_SERVICE_ID: ${{ secrets.EMAILJS_SERVICE_ID }}
          EMAILJS_TEMPLATE_ID: ${{ secrets.EMAILJS_TEMPLATE_ID }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: node .github/scripts/send-newsletter.js
```

## Step 3: Create Newsletter Script

Create `.github/scripts/send-newsletter.js`:

```javascript
const fs = require('fs');
const path = require('path');
const emailjs = require('@emailjs/nodejs');
const fetch = require('node-fetch');

// Initialize EmailJS
emailjs.init({
  publicKey: process.env.EMAILJS_PUBLIC_KEY,
  privateKey: process.env.EMAILJS_PRIVATE_KEY,
});

// Configuration
const CONFIG = {
  serviceId: process.env.EMAILJS_SERVICE_ID,
  templateId: process.env.EMAILJS_TEMPLATE_ID,
  siteUrl: 'https://www.kbhaskar.tech',
  siteName: 'Bhaskar Daily News',
  siteEmail: 'contact@kbhaskar.tech',
};

// Get subscribers from GitHub Issues
async function getSubscribers() {
  const response = await fetch(
    `https://api.github.com/repos/kundan007b/bhaskar-daily-ai-news/issues?labels=subscribe&state=closed`,
    {
      headers: {
        'Authorization': `token ${process.env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
      },
    }
  );
  
  const issues = await response.json();
  const subscribers = [];
  
  for (const issue of issues) {
    // Extract email from issue body
    const emailMatch = issue.body.match(/\*\*Email:\*\*\s*([^\s]+@[^\s]+)/);
    if (emailMatch && emailMatch[1]) {
      subscribers.push(emailMatch[1]);
    }
  }
  
  return [...new Set(subscribers)]; // Remove duplicates
}

// Parse post front matter
function parsePost(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  
  if (!match) return null;
  
  const frontMatter = match[1];
  const data = {};
  
  frontMatter.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length) {
      const value = valueParts.join(':').trim().replace(/^["']|["']$/g, '');
      data[key.trim()] = value;
    }
  });
  
  // Extract summary from content
  const bodyContent = content.substring(match[0].length);
  const summary = bodyContent
    .replace(/[#*`]/g, '')
    .split('\n\n')[0]
    .substring(0, 300) + '...';
  
  return {
    title: data.title,
    category: data.category,
    date: data.date,
    image: data.image,
    summary: data.description || summary,
    fileName: path.basename(filePath),
  };
}

// Send email to subscriber
async function sendEmail(subscriber, post) {
  const postSlug = post.fileName.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace('.md', '');
  const postUrl = `${CONFIG.siteUrl}/${post.category.toLowerCase()}/${postSlug}`;
  
  const templateParams = {
    to_email: subscriber,
    site_name: CONFIG.siteName,
    site_url: CONFIG.siteUrl,
    site_email: CONFIG.siteEmail,
    post_title: post.title,
    post_category: post.category,
    post_date: post.date,
    post_summary: post.summary,
    post_url: postUrl,
    post_image: post.image ? `${CONFIG.siteUrl}${post.image}` : '',
  };
  
  try {
    await emailjs.send(CONFIG.serviceId, CONFIG.templateId, templateParams);
    console.log(`✅ Email sent to ${subscriber}`);
    return true;
  } catch (error) {
    console.error(`❌ Failed to send to ${subscriber}:`, error);
    return false;
  }
}

// Main function
async function main() {
  try {
    // Get changed post files
    const changedFiles = fs.readFileSync('changed_files.txt', 'utf8')
      .split('\n')
      .filter(f => f.trim() && f.endsWith('.md'));
    
    if (changedFiles.length === 0) {
      console.log('No new posts to send');
      return;
    }
    
    console.log(`📬 Processing ${changedFiles.length} new post(s)`);
    
    // Get subscribers
    const subscribers = await getSubscribers();
    console.log(`📧 Found ${subscribers.length} subscriber(s)`);
    
    if (subscribers.length === 0) {
      console.log('No subscribers found');
      return;
    }
    
    // Process each new post
    for (const postFile of changedFiles) {
      const post = parsePost(postFile);
      if (!post) {
        console.log(`⚠️  Could not parse ${postFile}`);
        continue;
      }
      
      console.log(`\n📰 Sending newsletter for: ${post.title}`);
      
      let sent = 0;
      let failed = 0;
      
      // Send to all subscribers with rate limiting
      for (const subscriber of subscribers) {
        const success = await sendEmail(subscriber, post);
        if (success) sent++;
        else failed++;
        
        // Rate limit: 1 email per second
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      console.log(`\n✅ Newsletter sent: ${sent} successful, ${failed} failed`);
    }
  } catch (error) {
    console.error('Error sending newsletters:', error);
    process.exit(1);
  }
}

main();
```

## Step 4: Add GitHub Secrets

1. Go to your repo: https://github.com/kundan007b/bhaskar-daily-ai-news
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these secrets:

- **Name**: `EMAILJS_PUBLIC_KEY`  
  **Value**: `k1oKk9CNKGs_h7FW5`

- **Name**: `EMAILJS_PRIVATE_KEY`  
  **Value**: Get from [EmailJS Account](https://dashboard.emailjs.com/admin/account) → API Keys

- **Name**: `EMAILJS_SERVICE_ID`  
  **Value**: `service_0b5fbrq`

- **Name**: `EMAILJS_TEMPLATE_ID`  
  **Value**: `template_newsletter` (or your actual template ID)

## Step 5: Test

1. Commit the workflow and script:
   ```bash
   git add .github/workflows/send-newsletter.yml .github/scripts/send-newsletter.js
   git commit -m "feat: add automated newsletter system"
   git push origin main
   ```

2. Create a test post via admin panel
3. Check GitHub Actions to see if workflow runs
4. Check your email (if you're subscribed)

## How It Works

1. **Trigger**: When you push a new post to `_posts/`
2. **Detection**: Workflow detects new/modified posts
3. **Fetch Subscribers**: Gets emails from GitHub Issues with `subscribe` label
4. **Send Emails**: Sends personalized email to each subscriber via EmailJS
5. **Rate Limiting**: 1 email per second to avoid hitting EmailJS limits

## Free Tier Limits

EmailJS free tier:
- **200 emails/month**
- If you have 50 subscribers and publish 4 posts/month = 200 emails ✅
- Upgrade to paid plan ($15/month) for 2,000 emails if needed

## Best Practices

### Timing
- Don't publish all posts at once
- Space out publications to stay within limits
- Consider weekly digests instead of per-post emails

### Testing
- Test with your own email first
- Use workflow_dispatch to manually trigger
- Check email deliverability and spam folder

### Unsubscribe
- Include unsubscribe link in every email
- Process unsubscribe requests manually
- Close GitHub Issue to remove subscriber

## Advanced: Weekly Digest

Instead of sending per-post, send weekly digest:

1. Modify workflow to run on schedule:
   ```yaml
   on:
     schedule:
       - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
   ```

2. Modify script to collect all posts from past week
3. Send one email with multiple posts
4. Saves email quota!

## Troubleshooting

### Emails not sending
- Check GitHub Actions logs
- Verify EmailJS secrets are correct
- Check EmailJS dashboard for errors
- Ensure template exists and is active

### Rate limit exceeded
- Reduce number of posts
- Implement weekly digest
- Upgrade EmailJS plan

### Subscribers not found
- Check GitHub Issues have `subscribe` label
- Verify email format in issue body
- Check GITHUB_TOKEN has read permissions

## Alternative: Manual Newsletter

If automation is too complex:

1. Export subscribers from GitHub Issues
2. Use email service (Mailchimp, SendGrid, etc.)
3. Create newsletter manually
4. Send when you publish important posts

## Support

- **EmailJS Docs**: https://www.emailjs.com/docs/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Our Contact**: contact@kbhaskar.tech

---

**Status**: This is a guide only. Implementation requires creating the workflow files and adding secrets. Let me know if you want me to create the actual files!
