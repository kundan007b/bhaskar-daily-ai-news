# 📋 Post-Implementation Checklist

Use this checklist to ensure everything is set up correctly before going live.

---

## ⚙️ Pre-Deployment Setup

### GitHub Repository Configuration

- [ ] **Enable GitHub Pages**
  - Settings → Pages
  - Source: GitHub Actions
  - Click "Save"

- [ ] **Add Gemini API Secret**
  ```bash
  gh secret set GEMINI_API_KEY --repo kundan007b/bhaskar-daily-ai-news
  # Or via GitHub UI: Settings → Secrets and variables → Actions → New repository secret
  ```

- [ ] **Verify Workflow Permissions**
  - Settings → Actions → General
  - Workflow permissions: Read and write permissions
  - Check "Allow GitHub Actions to create and approve pull requests"

### Local Configuration

- [ ] **Test API Key Locally**
  ```bash
  export GEMINI_API_KEY="your-api-key-here"
  python scripts/validate_setup.py
  ```

- [ ] **Update AdSense Client ID** (if using ads)
  - Edit `_config.yml`
  - Replace: `adsense_client_id: "ca-pub-XXXXXXXXXXXX"`
  - With your actual Google AdSense publisher ID

- [ ] **Customize Site Metadata**
  - Edit `_config.yml`:
    - `title`
    - `description`
    - `url` (if different from kbhaskar.tech)
    - Social links (email, github_username, twitter_username)

- [ ] **Update Contact Information**
  - Edit `pages/contact.md`
  - Edit `pages/about.md`

---

## 🧪 Testing

### Local Testing

- [ ] **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Run Validation**
  ```bash
  python scripts/validate_setup.py
  ```
  Expected: All checks should pass (except API key if not set)

- [ ] **Generate Test Post**
  ```bash
  export GEMINI_API_KEY="your-key"
  python scripts/generate_post.py
  ```
  Check: `_posts/` folder should have new .md file

- [ ] **Verify Generated Content**
  - [ ] Post has valid front matter
  - [ ] English content is present
  - [ ] Hindi content is present
  - [ ] Image was generated in `assets/images/`
  - [ ] No placeholder text (TODO, XXX, etc.)

- [ ] **Test Jekyll Build** (optional, requires Ruby)
  ```bash
  bundle install
  bundle exec jekyll serve
  # Visit http://localhost:4000
  ```

### GitHub Actions Testing

- [ ] **Trigger Manual Workflow**
  - Go to: Actions → Auto Generate & Publish Posts
  - Click "Run workflow"
  - Select branch: main
  - Click "Run workflow"

- [ ] **Monitor Execution**
  - Watch the workflow run
  - Check for green checkmarks
  - Review logs if any errors occur

- [ ] **Verify Deployment**
  - Wait 2-3 minutes after workflow completes
  - Visit your GitHub Pages URL
  - Check if new post appears

---

## 🔍 Quality Checks

### Content Quality

- [ ] **Review Generated Post**
  - [ ] Title makes sense
  - [ ] Content is factual and balanced
  - [ ] No obvious errors or hallucinations
  - [ ] Hindi translation is accurate
  - [ ] Image is relevant

- [ ] **Check SEO Tags**
  - Right-click page → View Page Source
  - Verify presence of:
    - [ ] `<meta name="description">`
    - [ ] `<meta property="og:title">`
    - [ ] `<meta property="og:image">`
    - [ ] `<script type="application/ld+json">` (structured data)

### Functional Testing

- [ ] **Test Language Toggle**
  - [ ] Click "English" button
  - [ ] Click "हिन्दी" button
  - [ ] Verify content switches
  - [ ] Refresh page - preference should persist

- [ ] **Test on Mobile**
  - [ ] Visit on phone or use browser dev tools
  - [ ] Check responsive design
  - [ ] Verify images load
  - [ ] Test language toggle

- [ ] **Check Image Loading**
  - [ ] Featured image displays
  - [ ] No broken image icons
  - [ ] Images are properly sized
  - [ ] Alt text is present

---

## 🛡️ Security & Privacy

- [ ] **Verify Secret Management**
  ```bash
  # This should NOT print your API key
  gh secret list --repo kundan007b/bhaskar-daily-ai-news
  # Should show: GEMINI_API_KEY
  ```

- [ ] **Check Workflow Logs**
  - Go to recent workflow run
  - Verify API key is NOT visible in logs
  - Check for any exposed secrets

- [ ] **Review Privacy Policy**
  - Visit /privacy-policy page
  - Ensure it matches your use case
  - Update contact information

---

## 📊 Monitoring Setup

### Initial Monitoring

- [ ] **Set Up GitHub Notifications**
  - Watch repository (Watch → All Activity)
  - Enable email notifications for failed workflows

- [ ] **Check Workflow Schedule**
  - Workflow runs at: 00:30, 08:30, 16:30 UTC
  - Convert to your timezone
  - Set reminders to check first few runs

### Optional Enhancements

- [ ] **Set Up Google Analytics** (optional)
  - Create GA4 property
  - Add tracking code to `_includes/analytics.html`
  - Include in `_layouts/default.html`

- [ ] **Set Up Error Notifications** (optional)
  - Use GitHub Actions marketplace action
  - Send Slack/Discord/Email on failure

---

## 📈 Post-Launch

### First 24 Hours

- [ ] **Monitor First 3 Posts**
  - [ ] 00:30 UTC run
  - [ ] 08:30 UTC run
  - [ ] 16:30 UTC run

- [ ] **Check Deployment**
  - [ ] Posts appear on site
  - [ ] Images load correctly
  - [ ] No broken links

### First Week

- [ ] **Review Content Quality**
  - Read generated articles
  - Check for any patterns of errors
  - Verify factual accuracy

- [ ] **Monitor API Usage**
  - Check Gemini API quota at https://aistudio.google.com/
  - Verify you're within limits

- [ ] **Gather Feedback**
  - Share with friends/colleagues
  - Note any issues or suggestions

---

## 🐛 Troubleshooting Checklist

If something goes wrong, check:

### Workflow Fails

- [ ] Is GEMINI_API_KEY set in repository secrets?
- [ ] Is API key valid (test locally)?
- [ ] Check workflow logs for specific error
- [ ] Verify GitHub Pages is enabled
- [ ] Check repository permissions (write access)

### No New Posts

- [ ] Check if workflow ran (Actions tab)
- [ ] Look for "No changes" in commit
  - May happen if same topic generated twice
- [ ] Verify `_posts/` directory exists
- [ ] Check for collision (duplicate filename)

### Content Issues

- [ ] Review validation errors in logs
- [ ] Check if Hindi content is actually in Devanagari
- [ ] Verify image generation didn't fail
- [ ] Look for placeholder text that was rejected

### Image Problems

- [ ] Check if Imagen API is enabled in Google Cloud
- [ ] Verify API key has generativelanguage.googleapis.com access
- [ ] Look for image generation errors in logs
- [ ] Check `assets/images/` folder for files

### SEO Not Working

- [ ] View page source - are meta tags present?
- [ ] Check `_includes/seo.html` is included in layout
- [ ] Verify Jekyll build completed successfully
- [ ] Test with https://cards-dev.twitter.com/validator

---

## ✅ Final Sign-Off

Before considering deployment complete:

- [ ] All tests passed
- [ ] At least one successful automatic post
- [ ] No errors in workflow logs
- [ ] Site loads correctly on desktop
- [ ] Site loads correctly on mobile
- [ ] SEO tags validated
- [ ] Privacy policy reviewed
- [ ] Documentation read and understood
- [ ] Monitoring in place

---

## 📝 Notes

**Date Completed:** _______________

**Issues Encountered:**
- 
- 
- 

**Future Improvements:**
- 
- 
- 

---

## 🎉 Congratulations!

Your AI-powered bilingual news platform is now live!

**What's Next?**
1. Monitor first few automatic posts
2. Share your site with others
3. Consider adding analytics
4. Explore additional features from the roadmap

**Need Help?**
- Check README.md for detailed docs
- Review IMPLEMENTATION_SUMMARY.md for what changed
- Open issue on GitHub if stuck

---

*Checklist created: October 31, 2025*  
*Project: Bhaskar Daily AI News v2.0.0*
