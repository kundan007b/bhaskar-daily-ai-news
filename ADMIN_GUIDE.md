# 📝 Admin Panel Guide

## Access

**URL:** https://www.kbhaskar.tech/admin/

**Login Credentials:**
- Username: `kb007`
- Password: `Kundan@20`

**GitHub Token Required:**
- Create a Personal Access Token with **Contents: Read and write** permission
- Go to: GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
- Or use classic token with `repo` scope

---

## Features Overview

### 1️⃣ Post Manager Tab

**View All Posts:**
- Lists all posts from `_posts/` directory
- Shows date, title, and filename
- Sorted by date (newest first)

**Actions:**
- **✏️ Edit** - Load post into editor for modifications
- **🗑️ Delete** - Remove post permanently (with confirmation)
- **🔄 Refresh** - Reload posts list

### 2️⃣ New/Edit Post Tab

**Create New Post:**
1. Click **➕ New Post** to clear form
2. Fill in required fields (Title EN, Body EN)
3. Upload image (optional but recommended)
4. Click **Publish Post**

**Edit Existing Post:**
1. In Post Manager, click **✏️ Edit** on any post
2. Form auto-fills with current content
3. Current image shown (if exists)
4. Upload new image to replace, or keep existing
5. Click **Publish Post** to save changes

**Form Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| Title (English) | ✅ Yes | Main headline, used for SEO |
| Title (Hindi) | ❌ Optional | Hindi translation of title |
| Body (English) | ✅ Yes | Main article in Markdown |
| Body (Hindi) | ❌ Optional | Hindi version of article |
| Meta Description (EN) | ❌ Recommended | SEO description, max 160 chars |
| Meta Description (HI) | ❌ Optional | Hindi meta description |
| Keywords (EN) | ❌ Recommended | Comma-separated keywords |
| Keywords (HI) | ❌ Optional | Hindi keywords |
| Category | ✅ Yes | Technology/Business/Politics/Finance/Startups |
| Date | ✅ Auto-filled | Post date (YYYY-MM-DD) |
| Featured Image | ❌ Recommended | Upload image (auto-compressed) |
| Image Alt Text | ❌ Recommended | Accessibility description |

**Image Handling:**
- Uploaded images are automatically:
  - Resized to 1200px width (maintains aspect ratio)
  - Compressed to 85% quality JPEG
  - Saved to `assets/images/`
- When editing, you can:
  - Keep existing image (don't upload new one)
  - Replace image (upload new file)
  - Remove image (click **Remove** button)

### 3️⃣ Preview Tab

**Live Preview:**
- Renders markdown as HTML
- Updates as you type in Title/Body EN
- Click tab to see current preview

### 4️⃣ Options Tab

**Publish Mode:**
- **Commit to main** (default) - Direct push to main branch
- **Create PR** - Opens pull request for review

**Auto-fallback:**
- If main push is blocked, automatically creates PR

---

## Workflows

### ✏️ Edit Any Post and Add/Change Image

**Step-by-step:**

1. **Login to Admin Panel**
   - Enter username/password
   - Paste GitHub token

2. **Go to Post Manager Tab**
   - Click **🔄 Refresh** to load latest posts
   - Browse list of all posts

3. **Click ✏️ Edit on Post**
   - Form auto-fills with current content
   - Existing image shows with preview
   - Editor title updates: "Editing: filename.md"

4. **Modify Content**
   - Edit any field (title, body, keywords, etc.)
   - Current date pre-filled

5. **Change/Add Image**
   - **To add new image:** Click "Choose File", select image
   - **To keep current:** Leave file input empty
   - **To remove:** Click **Remove** button on current image preview
   - Images auto-compress client-side

6. **Save Changes**
   - Click **Publish Post**
   - Status shows progress:
     - "Compressing image..." (if new image)
     - "Uploading image..."
     - "Updating post..."
     - "Success. Post updated on main."

7. **Verify**
   - Post refreshes in manager
   - Live site updates in ~1 minute
   - Check: https://www.kbhaskar.tech/

---

## Tips & Best Practices

### 📸 Image Management

**Best practices:**
- Use high-quality images (min 800px width source)
- Relevant to article topic
- Proper alt text for accessibility and SEO
- Keep file sizes reasonable (system auto-optimizes)

**Image sources:**
- AI-generated (DALL·E, Midjourney, etc.)
- Stock photos (Unsplash, Pexels, Pixabay)
- News agency photos (with attribution)
- Original photos

### 📝 Content Quality

**SEO Optimization:**
- Write compelling titles (50-60 chars)
- Fill meta descriptions (140-160 chars)
- Use relevant keywords (4-6 per post)
- Include both EN/HI keywords for bilingual reach

**Markdown Formatting:**
```markdown
# Main Heading
## Subheading
**Bold text**
*Italic text*
- Bullet point
1. Numbered list
[Link text](https://example.com)
![Image alt](image-url.jpg)
```

**Hindi Content:**
- Use Devanagari script (हिन्दी)
- Keep it concise (200-400 words if provided)
- Match English content structure

### 🔒 Security

**Token Safety:**
- Never share your GitHub token
- Tokens are NOT stored (browser-only)
- Regenerate if compromised
- Use fine-grained tokens with minimal permissions

**Access Control:**
- Admin page is `noindex` (not in search engines)
- Blocked in `robots.txt`
- Change password regularly

### ⚡ Workflow Shortcuts

**Local Draft Save:**
- Click **Save Draft** to store locally
- Survives browser refresh
- Useful for long-form content

**Quick Edits:**
1. Post Manager → Edit
2. Change image/text
3. Publish → Done in 30 seconds

**Bulk Edits:**
- Edit multiple posts one after another
- Click **New Post** between edits to clear form

---

## Troubleshooting

### ❌ "Token invalid" error
- Regenerate token with correct permissions
- Ensure `Contents: Read and write` enabled
- Check token not expired

### ❌ "Failed to load posts"
- Check internet connection
- Verify token permissions
- Try **🔄 Refresh** again

### ❌ "Image upload failed"
- Check file size (max ~10MB recommended)
- Ensure valid image format (JPG, PNG, WebP)
- Try smaller/compressed source image

### ❌ "Post not appearing on site"
- Wait 1-2 minutes for GitHub Pages build
- Check date isn't in the future
- Verify commit succeeded (check GitHub repo)
- Force-refresh browser (Ctrl+Shift+R)

### ❌ "Main push blocked"
- System auto-creates PR instead
- Check GitHub for new pull request
- Merge PR manually to publish

---

## Advanced: Manual Post Editing

**Direct file editing (GitHub web UI):**

1. Go to: https://github.com/kundan007b/bhaskar-daily-ai-news/tree/main/_posts
2. Click on any `.md` file
3. Click ✏️ pencil icon to edit
4. Modify front matter or content
5. Commit changes
6. Site auto-deploys

**Front matter format:**
```yaml
---
layout: post
title: "Article Title"
title_hi: "हिंदी शीर्षक"
category: "Technology"
description: "SEO description"
meta_desc_hi: "हिंदी विवरण"
keywords: "ai, india, tech, कृत्रिम बुद्धिमत्ता"
image: /assets/images/filename.jpg
image_alt: "Image description"
body_hi: |
  हिंदी सामग्री यहाँ
  कई पंक्तियाँ
---

English article content here in Markdown...
```

---

## Quick Reference

| Task | Steps |
|------|-------|
| **Add image to existing post** | Post Manager → Edit → Upload image → Publish |
| **Change post title** | Post Manager → Edit → Modify title → Publish |
| **Delete old post** | Post Manager → Delete (🗑️) → Confirm |
| **Create new post** | New Post button → Fill form → Upload image → Publish |
| **Preview before publish** | Fill form → Preview tab → Check rendering |
| **Update meta description** | Edit post → Meta Description field → Publish |

---

## Support

**Issues:**
- Open GitHub issue: https://github.com/kundan007b/bhaskar-daily-ai-news/issues

**Documentation:**
- Main README: https://github.com/kundan007b/bhaskar-daily-ai-news/blob/main/README.md
- Tier 1 workflows: See README section on GitHub Issues workflows

**Logs:**
- GitHub Actions runs: https://github.com/kundan007b/bhaskar-daily-ai-news/actions

---

**Last Updated:** November 2025  
**Version:** 2.0 (Post Manager Edition)
