# Google AdSense Setup Guide

## ✅ AdSense Integration Complete!

Your website now has Google AdSense ads configured and ready. Follow these steps to activate them:

## 📋 Step 1: Sign Up for Google AdSense

1. Go to https://www.google.com/adsense
2. Click "Get Started"
3. Sign in with your Google account
4. Fill in your website details:
   - Website URL: `https://kbhaskar.tech`
   - Country: India
   - Accept terms and conditions

## 📝 Step 2: Add Your Site

1. In AdSense dashboard, add your website
2. Wait for approval (usually 1-2 weeks)
3. You'll receive an email when approved

## 🔑 Step 3: Get Your Publisher ID

Once approved:
1. Log into AdSense
2. Go to Account → Settings
3. Copy your Publisher ID (format: `ca-pub-XXXXXXXXXXXXXXXX`)

## ⚙️ Step 4: Update Your Website Config

1. Open `_config.yml` in your repository
2. Find this line:
   ```yaml
   adsense_client_id: "ca-pub-XXXXXXXXXXXX"
   ```
3. Replace `ca-pub-XXXXXXXXXXXX` with your actual Publisher ID
4. Save and commit the file

## 🎯 Step 5: Create Ad Units (Optional)

For better targeting, create specific ad units:

1. In AdSense, go to Ads → By ad unit
2. Create these ad units:
   - **Header Banner** (Responsive Display)
   - **In-Article** (In-article ads)
   - **Sidebar** (Responsive Display)
   - **Footer** (Responsive Display)

3. Copy the ad slot IDs for each unit

4. Update the ad includes in `_includes/`:
   - `ad-header.html` → Replace `data-ad-slot="XXXXXXXXXX"`
   - `ad-in-article.html` → Replace `data-ad-slot="XXXXXXXXXX"`
   - `ad-sidebar.html` → Replace `data-ad-slot="XXXXXXXXXX"`
   - `ad-footer.html` → Replace `data-ad-slot="XXXXXXXXXX"`

## 📍 Ad Placements Already Configured

Your website now has ads in these locations:

### Homepage (index.html)
- ✅ Header banner ad (above posts)
- ✅ In-feed ads (after every 4 posts)

### Article Pages (post.html)
- ✅ Top article ad (after featured image)
- ✅ Bottom article ad (after content)

### All Pages
- ✅ AdSense script loaded in `<head>`
- ✅ Responsive ad sizes
- ✅ Mobile-friendly placement

## 🎨 Ad Styling

Ads are styled with:
- Responsive containers
- "Advertisement" label
- Proper spacing
- Mobile optimization
- Print media hidden

## ⚠️ Before Going Live

**Current Status:**
- ✅ AdSense code integrated
- ⏳ Publisher ID: Placeholder (needs your actual ID)
- ⏳ Ad slots: Using auto ads (can be customized)

**To Activate:**
1. Replace placeholder ID with your real Publisher ID
2. Optionally add specific ad slot IDs
3. Commit and push changes
4. Wait for AdSense approval

## 🚀 Quick Activation

Edit `_config.yml`:
```yaml
# Replace this:
adsense_client_id: "ca-pub-XXXXXXXXXXXX"

# With your actual ID:
adsense_client_id: "ca-pub-1234567890123456"
```

Then commit:
```bash
git add _config.yml
git commit -m "Add Google AdSense Publisher ID"
git push origin main
```

## 💡 Tips for AdSense Approval

1. **Content Quality**: You have 5 posts - add more for better approval chances
2. **Privacy Policy**: Already configured ✅
3. **Contact Page**: Already configured ✅
4. **Original Content**: Using AI-generated content - ensure it's unique
5. **Traffic**: Some traffic helps (100+ visitors/day)
6. **Domain Age**: Custom domain helps (kbhaskar.tech ✅)

## 📊 Expected Revenue

With hourly posts (120 posts/day):
- More content = more ad impressions
- Bilingual content = wider audience
- Multiple ad placements = higher revenue

## 🔍 Monitoring

After activation:
1. Check AdSense dashboard for impressions/clicks
2. Monitor revenue in real-time
3. Optimize ad placements based on performance

## 🎉 You're All Set!

Your website is AdSense-ready. Just need to:
1. Sign up for AdSense
2. Get approved
3. Add your Publisher ID
4. Start earning!
