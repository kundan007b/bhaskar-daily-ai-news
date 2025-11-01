# Comments System Setup Guide (Giscus)

This guide will help you set up the giscus comment system powered by GitHub Discussions.

## What is Giscus?

Giscus is a comments system powered by GitHub Discussions. Benefits:

- ✅ **100% Free** - No cost, no limits
- ✅ **Privacy-Friendly** - No tracking, no ads
- ✅ **Moderation** - Full control via GitHub Discussions
- ✅ **Open Source** - Transparent and trustworthy
- ✅ **GitHub Integration** - Users comment with GitHub accounts
- ✅ **Reactions** - Like, love, celebrate comments
- ✅ **Markdown Support** - Rich formatting in comments

## Prerequisites

- GitHub repository (you have this ✅)
- GitHub Discussions enabled on your repo

## Step 1: Enable GitHub Discussions

1. Go to your repo: https://github.com/kundan007b/bhaskar-daily-ai-news
2. Click **Settings** tab
3. Scroll to **Features** section
4. Check ✅ **Discussions**
5. Click **Set up discussions**
6. GitHub will create a welcome discussion

## Step 2: Create Comments Category

1. Go to **Discussions** tab in your repo
2. Click **Categories** (or the ⚙️ icon)
3. Click **New category**
4. **Name**: `Comments`
5. **Description**: `Blog post comments powered by giscus`
6. **Discussion format**: Choose **Announcement** (only maintainers can create, users can comment)
7. Click **Create**

## Step 3: Configure Giscus

1. Go to https://giscus.app/
2. **Configuration** section:
   
   - **Repository**: `kundan007b/bhaskar-daily-ai-news`
   - **Page ↔️ Discussions Mapping**: Choose `pathname`
   - **Discussion Category**: Select `Comments`
   - **Features**:
     - ✅ Enable reactions for the main post
     - ✅ Emit discussion metadata
     - Choose: Place the comment box above the comments
   - **Theme**: `light` (or `preferred_color_scheme` for auto dark/light)

3. **Get your configuration**:
   - Giscus will show you `data-repo-id` and `data-category-id`
   - Copy these values

## Step 4: Update Your Site

1. Open `_includes/comments.html`
2. Find these lines:
   ```html
   data-repo-id="YOUR_REPO_ID"
   data-category-id="YOUR_CATEGORY_ID"
   ```
3. Replace with your actual IDs from giscus.app
4. Save the file

## Step 5: Deploy

```bash
git add _includes/comments.html _layouts/post.html
git commit -m "feat: add giscus comment system"
git push origin main
```

Wait 1-2 minutes for deployment.

## Step 6: Test

1. Visit any blog post: https://www.kbhaskar.tech/
2. Scroll to the bottom
3. You should see the comments section
4. Sign in with GitHub to test commenting

## Finding Your IDs

### Repo ID

Visit: https://giscus.app/

Enter your repo: `kundan007b/bhaskar-daily-ai-news`

Giscus will automatically find and display your `data-repo-id`.

### Category ID

After enabling Discussions and creating the "Comments" category, giscus will show the `data-category-id` when you select it.

## Customization Options

### Theme

You can use different themes:

- `light` - Light theme (default)
- `dark` - Dark theme
- `preferred_color_scheme` - Auto dark/light based on user's system
- `dark_dimmed` - GitHub dark dimmed
- `transparent_dark` - Transparent dark
- Many more on giscus.app

### Language

Change `data-lang="en"` to:
- `hi` - Hindi
- `es` - Spanish
- `fr` - French
- See full list on giscus.app

### Reactions

Disable reactions by setting:
```html
data-reactions-enabled="0"
```

### Comment Input Position

- `bottom` - Comment box below existing comments (default)
- `top` - Comment box above existing comments

## Moderation

All comments go to GitHub Discussions where you can:

- ✅ **Moderate** - Edit, delete, lock, hide spam
- ✅ **Reply** - Respond to comments
- ✅ **Get Notifications** - Email alerts for new comments
- ✅ **Label** - Organize discussions
- ✅ **Pin** - Highlight important comments

Access moderation:
https://github.com/kundan007b/bhaskar-daily-ai-news/discussions

## Privacy

Giscus is privacy-friendly:

- ❌ No tracking cookies
- ❌ No ads
- ❌ No analytics (unless you add them)
- ✅ Comments stored on GitHub (your control)
- ✅ Open source and transparent

## Troubleshooting

### Comments not loading

- **Enable Discussions** on your repo
- **Check repo-id** and **category-id** are correct
- **Public repo** required (private repos won't work)
- **Wait for deployment** (~2 minutes after push)

### "Error: Discussion category not found"

- Create "Comments" category in Discussions
- Use the exact category-id from giscus.app
- Category must be **Announcement** type

### Users can't comment

- Ensure repository is **public**
- Users must have GitHub account
- Check Discussions are enabled

## Benefits for Your Site

1. **Engagement** - Readers can discuss articles
2. **Community** - Build a community around your content
3. **SEO** - User-generated content helps SEO
4. **Feedback** - Get direct feedback on articles
5. **Free** - No cost, no limits
6. **Control** - Full moderation via GitHub

## Alternative: Other Comment Systems

If you prefer alternatives:

### Disqus
- Popular but has ads and tracking
- Free plan available
- More features but less privacy

### Utterances
- Similar to giscus but uses GitHub Issues
- Simpler but less features
- Good alternative

### Facebook Comments
- Requires Facebook account
- Privacy concerns
- More mainstream audience

**Recommendation**: Stick with giscus for privacy and control!

## Next Steps

After setup:

1. **Test commenting** on a few posts
2. **Moderate** your first comments
3. **Enable email notifications** in GitHub settings
4. **Promote engagement** - Encourage readers to comment
5. **Respond** to comments to build community

## Support

- **Giscus Docs**: https://giscus.app/
- **GitHub Discussions**: https://docs.github.com/en/discussions
- **Our Contact**: contact@kbhaskar.tech

---

**Pro Tip**: Pin your first comment on popular posts to start discussions and welcome readers!
