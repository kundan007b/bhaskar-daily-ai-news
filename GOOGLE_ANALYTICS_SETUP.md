# Google Analytics Setup Guide

## Quick Setup (5 minutes)

### Step 1: Create Google Analytics Account

1. Go to [Google Analytics](https://analytics.google.com/)
2. Click **"Start measuring"** or **"Admin"** (gear icon)
3. Click **"Create Account"**
4. Fill in:
   - **Account Name**: `Bhaskar Daily AI News`
   - Check the boxes for data sharing settings (optional)
   - Click **"Next"**

### Step 2: Create Property

1. **Property Details**:
   - **Property name**: `Bhaskar Daily AI News`
   - **Reporting time zone**: `India (GMT+5:30)`
   - **Currency**: `Indian Rupee (INR)`
   - Click **"Next"**

2. **Business Information**:
   - **Industry category**: `News & Media Publishers`
   - **Business size**: Select your size
   - Click **"Next"**

3. **Business Objectives**:
   - Select: `Examine user behavior`
   - Click **"Create"**

4. Accept the **Terms of Service**

### Step 3: Set Up Data Stream

1. Choose platform: **Web**
2. Fill in:
   - **Website URL**: `https://kbhaskar.tech`
   - **Stream name**: `Bhaskar Daily AI News Website`
   - Click **"Create stream"**

3. **Copy your Measurement ID**
   - Format: `G-XXXXXXXXXX`
   - You'll see it at the top of the stream details page

### Step 4: Add Tracking ID to Your Site

1. Open `_config.yml` in your repository
2. Find this line:
   ```yaml
   google_analytics: ""
   ```
3. Replace with your Measurement ID:
   ```yaml
   google_analytics: "G-XXXXXXXXXX"
   ```
4. Commit and push:
   ```bash
   git add _config.yml
   git commit -m "feat: Add Google Analytics tracking ID"
   git push origin main
   ```

### Step 5: Verify Installation

1. Visit your website: https://kbhaskar.tech
2. Open Google Analytics
3. Go to **Reports** → **Realtime**
4. You should see yourself as an active user!

---

## What You'll Track

### 📊 Automatic Metrics

Once enabled, Google Analytics will automatically track:

- **Users & Sessions**: How many people visit your site
- **Page Views**: Which articles are most popular
- **Traffic Sources**: Where visitors come from (Google, social media, direct)
- **Geographic Data**: Where your readers are located
- **Device Types**: Mobile vs Desktop usage
- **Engagement**: Time on page, bounce rate
- **Real-time Activity**: Live visitor count

### 📈 Key Reports to Monitor

1. **Realtime Overview**
   - See current active users
   - What pages they're viewing now

2. **Acquisition Overview**
   - How users find your site
   - Organic search vs social vs direct

3. **Engagement Overview**
   - Most popular articles
   - Average time on page
   - Scroll depth

4. **User Attributes**
   - Demographics (age, gender)
   - Interests
   - Geographic location

---

## Advanced Configuration (Optional)

### Custom Events

Add event tracking for specific actions:

```javascript
// Track social share clicks
gtag('event', 'share', {
  'method': 'Twitter',
  'content_type': 'article',
  'item_id': '{{ page.title }}'
});

// Track newsletter signups
gtag('event', 'newsletter_signup', {
  'method': 'footer_form'
});

// Track language toggle
gtag('event', 'language_change', {
  'language': 'hindi'
});
```

### Enhanced Measurement (Recommended)

Enable in Google Analytics Admin:

1. Go to **Admin** → **Data Streams** → Your stream
2. Click **"Enhanced measurement"**
3. Toggle ON these features:
   - ✅ Page views
   - ✅ Scrolls (tracks 90% scroll depth)
   - ✅ Outbound clicks
   - ✅ Site search
   - ✅ Video engagement
   - ✅ File downloads

### Privacy Settings

Our implementation includes:

```javascript
gtag('config', 'G-XXXXXXXXXX', {
  'anonymize_ip': true,        // GDPR compliant
  'cookie_flags': 'SameSite=None;Secure'  // Modern cookie security
});
```

These settings:
- Anonymize visitor IP addresses (GDPR/privacy compliant)
- Use secure cookie flags
- Respect Do Not Track preferences

---

## Troubleshooting

### Not Seeing Data?

1. **Wait 24-48 hours**: Initial data may take time to appear
2. **Check Realtime**: Should show immediate activity
3. **Verify ID**: Make sure `G-XXXXXXXXXX` is correct in `_config.yml`
4. **Check Browser**: Disable ad blockers when testing
5. **Inspect Page**: Right-click → View Source, search for `gtag`

### Common Issues

**Issue**: "Analytics not loading"
- **Solution**: Clear browser cache, rebuild Jekyll site

**Issue**: "No data in reports"
- **Solution**: Visit your site from different browser/device

**Issue**: "Tag not found in source code"
- **Solution**: Ensure `google_analytics` is set in `_config.yml` (not empty)

### Test Installation

```bash
# Visit your site and check browser console
curl -s https://kbhaskar.tech | grep -o "gtag.js?id=G-[A-Z0-9]*"

# Should output: gtag.js?id=G-XXXXXXXXXX
```

---

## Best Practices

### 1. Set Up Goals & Conversions

Track important actions:

- Newsletter signups
- Social shares
- Contact form submissions
- Article completion (90% scroll)

### 2. Create Custom Dashboards

Build dashboards for:

- Daily traffic overview
- Top 10 articles
- Traffic sources breakdown
- Mobile vs Desktop engagement

### 3. Monitor Weekly

Check these metrics weekly:

- Total users (is traffic growing?)
- Top articles (what content works?)
- Traffic sources (where to focus promotion?)
- Bounce rate (is content engaging?)

### 4. Analyze Monthly

Monthly deep dives:

- Content performance trends
- User retention rates
- Conversion funnel analysis
- Geographic expansion opportunities

---

## Privacy Compliance

### GDPR (Europe)

✅ IP anonymization enabled  
✅ Cookie consent banner (add separately)  
⚠️ Add privacy policy link (already have `/privacy-policy/`)

### CCPA (California)

✅ Data collection transparency  
⚠️ Add "Do Not Sell My Info" link if needed

### India

✅ Compliant with IT Act 2000  
✅ Privacy policy available

---

## Next Steps After Setup

1. ✅ **Install Tracking Code** (Already done!)
2. 📝 **Set up Goals** (Newsletter, shares, engagement)
3. 🔗 **Link Google Search Console** (for SEO data)
4. 📊 **Create Custom Reports** (for your specific needs)
5. 🔔 **Set up Alerts** (traffic spikes, anomalies)
6. 🎯 **Define KPIs** (users/day, avg time, bounce rate)

---

## Resources

- [Google Analytics Help Center](https://support.google.com/analytics)
- [GA4 Setup Guide](https://support.google.com/analytics/answer/9304153)
- [Analytics Academy](https://analytics.google.com/analytics/academy/)
- [GA4 vs Universal Analytics](https://support.google.com/analytics/answer/11583528)

---

## Support

Need help? Contact: **contact@kbhaskar.tech**

**Estimated Setup Time**: 5-10 minutes  
**Data Availability**: Realtime (immediate), Reports (24-48 hours)  
**Cost**: FREE (up to 10M events/month)
