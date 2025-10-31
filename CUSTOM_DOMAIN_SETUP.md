# 🌐 Custom Domain Setup Guide - kbhaskar.tech

## Step 1: Configure DNS Records (Do this first!)

Go to your domain registrar's DNS management panel (where you bought `kbhaskar.tech`) and add these DNS records:

### Option A: Using Apex Domain (kbhaskar.tech)

Add these **A Records**:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 185.199.108.153 | 3600 |
| A | @ | 185.199.109.153 | 3600 |
| A | @ | 185.199.110.153 | 3600 |
| A | @ | 185.199.111.153 | 3600 |

### Option B: Using www Subdomain (Recommended)

Add this **CNAME Record**:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | www | kundan007b.github.io | 3600 |

**PLUS** add these **A Records** for the apex domain:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 185.199.108.153 | 3600 |
| A | @ | 185.199.109.153 | 3600 |
| A | @ | 185.199.110.153 | 3600 |
| A | @ | 185.199.111.153 | 3600 |

### Common DNS Providers

**Namecheap:**
1. Login → Domain List → Manage
2. Advanced DNS tab
3. Add records as shown above

**GoDaddy:**
1. Login → My Products → DNS
2. Add records as shown above

**Cloudflare:**
1. Login → Select domain → DNS
2. Add records (set Proxy status to "DNS only" initially)

**Google Domains:**
1. Login → My Domains → DNS
2. Add records as shown above

## Step 2: Configure GitHub Pages

1. **Go to GitHub Pages settings:**
   ```
   https://github.com/kundan007b/bhaskar-daily-ai-news/settings/pages
   ```

2. **Enable GitHub Pages:**
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
   - Click **Save**

3. **Add Custom Domain:**
   - In the "Custom domain" field, enter: `kbhaskar.tech`
   - Click **Save**
   - Wait for DNS check (may take a few minutes)

4. **Enable HTTPS:**
   - After DNS check passes, check the box: ✅ **Enforce HTTPS**
   - This provides SSL certificate (takes a few minutes)

## Step 3: Verify DNS Configuration

Use these tools to check if your DNS is configured correctly:

1. **DNS Checker:**
   ```
   https://dnschecker.org/#A/kbhaskar.tech
   ```
   Should show GitHub's IP addresses (185.199.108-111.153)

2. **Command Line (Terminal):**
   ```bash
   # Check A records
   dig kbhaskar.tech +short
   
   # Should return:
   # 185.199.108.153
   # 185.199.109.153
   # 185.199.110.153
   # 185.199.111.153
   
   # Check CNAME record (if using www)
   dig www.kbhaskar.tech +short
   # Should return: kundan007b.github.io
   ```

## Step 4: Wait for Propagation

⏱️ **DNS propagation can take:**
- Minimum: 5-30 minutes
- Average: 2-4 hours
- Maximum: 48 hours

**During this time:**
- Some locations may see the new site
- Others may see the old configuration
- This is normal!

## Step 5: Test Your Domain

Once DNS has propagated, visit:
- http://kbhaskar.tech (should redirect to https)
- https://kbhaskar.tech
- https://www.kbhaskar.tech

All should show your AI news site!

## Troubleshooting

### Issue: "Domain's DNS record could not be retrieved"
**Solution:** 
- Wait 10-15 minutes for DNS to propagate
- Verify DNS records are correct
- Try removing and re-adding the custom domain

### Issue: "CNAME already in use"
**Solution:**
- Someone else is using this domain on GitHub Pages
- Verify you own the domain
- Check if there are conflicting CNAME records

### Issue: "Not served over HTTPS"
**Solution:**
- Wait 15-30 minutes after DNS verification
- Uncheck "Enforce HTTPS", wait 5 minutes, then re-check it
- GitHub needs time to provision SSL certificate

### Issue: Site shows 404 error
**Solution:**
- Check that CNAME file contains: `kbhaskar.tech`
- Verify `_config.yml` has correct URL
- Wait for GitHub Pages to rebuild (2-3 minutes)
- Clear browser cache

### Issue: Images or CSS not loading
**Solution:**
- If using apex domain (kbhaskar.tech), update `_config.yml`:
  ```yaml
  url: "https://kbhaskar.tech"
  baseurl: ""
  ```
- If using www subdomain, update to:
  ```yaml
  url: "https://www.kbhaskar.tech"
  baseurl: ""
  ```

## Current Configuration

✅ **CNAME file:** `kbhaskar.tech`
✅ **_config.yml:** `https://www.kbhaskar.tech`

## Recommended Setup

For best results, use **both** apex and www:

1. **Set GitHub custom domain to:** `kbhaskar.tech` (without www)
2. **Add all DNS records** (both A records and CNAME for www)
3. **GitHub will automatically redirect** www to apex domain

## Security Best Practices

1. ✅ **Always use HTTPS** - Enforce it in GitHub Pages settings
2. ✅ **Enable DNSSEC** - If your registrar supports it
3. ✅ **Use CAA records** (optional) - Restrict SSL certificate issuance
   ```
   kbhaskar.tech. CAA 0 issue "letsencrypt.org"
   kbhaskar.tech. CAA 0 issue "pki.goog"
   ```

## Final Checklist

- [ ] DNS A records added (4 records pointing to GitHub IPs)
- [ ] CNAME record for www added (if using www subdomain)
- [ ] GitHub Pages enabled (Deploy from branch: main)
- [ ] Custom domain added in GitHub Pages settings
- [ ] DNS check passed (green checkmark in GitHub)
- [ ] HTTPS enforced (enabled in GitHub Pages settings)
- [ ] Site accessible at https://kbhaskar.tech
- [ ] Site accessible at https://www.kbhaskar.tech

## What Happens After Setup

Once configured, your site will be accessible at:

- ✅ https://kbhaskar.tech - **Your custom domain!**
- ✅ https://www.kbhaskar.tech - **Also works!**
- ❌ https://kundan007b.github.io/bhaskar-daily-ai-news/ - **Redirects to custom domain**

---

## Need Help?

Common DNS providers' documentation:
- [GitHub Pages Custom Domain Guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Namecheap DNS Setup](https://www.namecheap.com/support/knowledgebase/article.aspx/9645/2208/how-do-i-link-my-domain-to-github-pages/)
- [GoDaddy DNS Setup](https://www.godaddy.com/help/manage-dns-records-680)
- [Cloudflare DNS Setup](https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records/)

**Your site will be live at https://kbhaskar.tech in 5-30 minutes after DNS propagation!** 🚀
