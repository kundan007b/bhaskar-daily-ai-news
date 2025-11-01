# Email Subscription Setup Guide

This guide will help you set up email subscriptions using EmailJS (free service).

## Step 1: Create EmailJS Account

1. Go to [EmailJS](https://www.emailjs.com/)
2. Click **Sign Up** and create a free account
3. Verify your email address

## Step 2: Set Up Email Service

1. After logging in, click **Add New Service**
2. Choose your email provider:
   - **Gmail** (recommended for personal use)
   - **Outlook**
   - Or any other SMTP service
3. Click **Connect Account** and authorize EmailJS
4. Note down your **Service ID** (e.g., `service_bhaskar`)

### Gmail Setup (Recommended)
- Click on Gmail
- Click "Connect Account"
- Sign in with your Google account
- Allow EmailJS permissions
- Your Service ID will be automatically created

## Step 3: Create Email Template

1. Go to **Email Templates** in EmailJS dashboard
2. Click **Create New Template**
3. Use this template for subscription confirmation:

### Template Name
`template_subscribe`

### Template Content

**Subject:**
```
Welcome to Bhaskar Daily News! 🎉
```

**Body (HTML):**
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome to {{site_name}}!</h1>
        </div>
        <div class="content">
            <p>Hi there!</p>
            
            <p>Thank you for subscribing to <strong>{{site_name}}</strong>! We're excited to have you on board.</p>
            
            <p>You'll now receive:</p>
            <ul>
                <li>📰 Daily news updates in English & Hindi</li>
                <li>🚀 Latest startup & technology stories</li>
                <li>💰 Business & finance insights</li>
                <li>🏛️ Political developments</li>
            </ul>
            
            <p>Your subscription is confirmed for: <strong>{{subscriber_email}}</strong></p>
            
            <a href="{{site_url}}" class="button">Visit Bhaskar Daily News</a>
            
            <p style="margin-top: 30px;">If you ever want to unsubscribe, simply reply to this email with "Unsubscribe".</p>
        </div>
        <div class="footer">
            <p>© {{date}} Bhaskar Daily News • Written by KB</p>
            <p>You received this email because you subscribed at {{site_url}}</p>
        </div>
    </div>
</body>
</html>
```

**Template Variables:**
- `{{to_email}}` - Recipient email
- `{{subscriber_email}}` - Subscriber's email (for confirmation)
- `{{site_name}}` - Your site name
- `{{site_url}}` - Your site URL
- `{{date}}` - Subscription date

4. Click **Save**

## Step 4: Get Your Public Key

1. Go to **Account** → **General** in EmailJS dashboard
2. Find your **Public Key** (starts with something like `user_xxxxx` or similar)
3. Copy this key

## Step 5: Update Your Website

1. Open `/workspaces/bhaskar-daily-ai-news/_layouts/default.html`
2. Find this line near the bottom:
   ```javascript
   emailjs.init("YOUR_PUBLIC_KEY");
   ```
3. Replace `YOUR_PUBLIC_KEY` with your actual EmailJS public key
4. Find this line:
   ```javascript
   emailjs.send('service_bhaskar', 'template_subscribe', {
   ```
5. Replace `service_bhaskar` with your actual Service ID
6. Replace `template_subscribe` with your actual Template ID

## Step 6: Update _config.yml

Make sure your `_config.yml` has the correct URL:
```yaml
url: "https://www.kbhaskar.tech"
title: "Bhaskar Daily News"
```

## Step 7: Test the Subscription

1. Commit and push your changes:
   ```bash
   git add -A
   git commit -m "feat: add EmailJS subscription with confirmation emails"
   git push origin main
   ```

2. Wait for deployment (~1-2 minutes)

3. Visit your website: https://www.kbhaskar.tech

4. Scroll to the footer or find the newsletter widget

5. Enter your email and click **Subscribe**

6. Check your email inbox for the confirmation email

## Troubleshooting

### Emails Not Sending
- Verify your EmailJS Service is connected properly
- Check that your Public Key is correct in `default.html`
- Check browser console for errors (F12 → Console)
- Verify Service ID and Template ID match your EmailJS dashboard

### Gmail Blocking Emails
- Check your Spam folder
- Make sure your Gmail account has "Less secure app access" enabled (if needed)
- Or use Gmail with OAuth (recommended)

### Template Not Found
- Make sure Template ID exactly matches what's in your code
- Template must be saved and active in EmailJS

## Subscriber Management

Subscribers are automatically stored in GitHub Issues with the `subscribe` label. To view all subscribers:

1. Go to your GitHub repo: https://github.com/kundan007b/bhaskar-daily-ai-news
2. Click **Issues**
3. Filter by label: `subscribe`

You can export this list for use with email marketing tools.

## Free Tier Limits

EmailJS free tier includes:
- ✅ **200 emails/month**
- ✅ Unlimited templates
- ✅ Unlimited services
- ✅ Email support

This should be sufficient for starting out. If you need more, upgrade to their paid plan ($15/month for 2,000 emails).

## Alternative: Formspree

If you prefer Formspree (simpler but different approach):

1. Go to [Formspree](https://formspree.io/)
2. Sign up for free (50 submissions/month)
3. Create a new form
4. Update the form action in your HTML:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

## Next Steps

- Consider setting up automated newsletter emails when you publish new posts
- Create a welcome series (multiple emails over time)
- Build an email list management system
- Set up analytics to track open rates

---

**Need Help?** Check the [EmailJS Documentation](https://www.emailjs.com/docs/) or create an issue on GitHub.
