# 🔐 Secret Verification Guide

## How to Verify Your GEMINI_API_KEY is Set Correctly

### Method 1: Check via GitHub Web UI (Recommended)

1. **Go to your repository on GitHub:**
   ```
   https://github.com/kundan007b/bhaskar-daily-ai-news
   ```

2. **Navigate to Settings:**
   - Click the "Settings" tab at the top
   
3. **Go to Secrets and Variables:**
   - In the left sidebar, click "Secrets and variables"
   - Click "Actions"

4. **Verify the secret exists:**
   - You should see `GEMINI_API_KEY` in the list
   - It will show when it was last updated
   - You cannot view the actual value (for security)

### Method 2: Test with a Workflow Run

The best way to verify it works is to trigger a test run:

1. **Go to Actions tab:**
   ```
   https://github.com/kundan007b/bhaskar-daily-ai-news/actions
   ```

2. **Select the workflow:**
   - Click "Auto Generate & Publish Posts"

3. **Run workflow manually:**
   - Click "Run workflow" button (top right)
   - Select branch: `main`
   - Click the green "Run workflow" button

4. **Watch the execution:**
   - Click on the running workflow
   - Click on the "generate" job
   - Watch the logs in real-time

5. **Check for success:**
   - ✅ If the secret is correct: You'll see successful post generation
   - ❌ If the secret is missing/wrong: You'll see an API authentication error

### Method 3: Check Recent Workflow Runs

If workflows have already run:

1. **Go to Actions tab:**
   ```
   https://github.com/kundan007b/bhaskar-daily-ai-news/actions
   ```

2. **Look at recent runs:**
   - Green checkmark ✅ = Secret is working
   - Red X ❌ = Check the logs for errors

3. **Click on a run to see details:**
   - Expand the "Generate post" step
   - Look for error messages about API keys

### Expected Behavior

#### ✅ Secret is Correctly Set:
```
📰 Generating post for topic: India political news...
Generating text content...
  ✓ Text generated successfully
  ✓ JSON schema validated
  ✓ Content quality validated
Generating image...
  ✓ Image generated and saved: abc123.jpg
🎉 Post generation completed successfully!
```

#### ❌ Secret is Missing/Invalid:
```
ERROR - GEMINI_API_KEY environment variable not set
```
or
```
ERROR - Gemini API request error: 401 Unauthorized
```

### How to Update the Secret (if needed)

#### Via GitHub Web UI:
1. Go to: Settings → Secrets and variables → Actions
2. Click on `GEMINI_API_KEY`
3. Click "Update secret"
4. Paste your new API key
5. Click "Update secret"

#### Via GitHub CLI (if you have proper auth):
```bash
gh secret set GEMINI_API_KEY --repo kundan007b/bhaskar-daily-ai-news
# Paste your API key when prompted
```

### Security Checks

✅ **Good Signs:**
- Secret only visible in Settings, not in code
- Workflow logs show `***` instead of actual key
- Only repository collaborators can view/edit secrets

❌ **Bad Signs:**
- API key visible in workflow logs (if this happens, rotate your key immediately)
- Commits contain hardcoded keys (never commit secrets!)

### Getting a Gemini API Key

If you need to get or regenerate your API key:

1. **Go to Google AI Studio:**
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **Sign in** with your Google account

3. **Create API Key:**
   - Click "Create API Key"
   - Select a Google Cloud project (or create new)
   - Copy the key (starts with `AIza...`)

4. **Add to GitHub:**
   - Follow the "How to Update the Secret" steps above

### Troubleshooting

**Problem:** Workflow fails with "Resource not accessible"
- **Solution:** Check repository permissions and that GitHub Actions is enabled

**Problem:** "API quota exceeded" error
- **Solution:** Check your usage at https://aistudio.google.com/
- Consider upgrading to a paid plan if needed

**Problem:** "Invalid API key" error
- **Solution:** Regenerate your key at https://aistudio.google.com/app/apikey
- Update the secret in GitHub

**Problem:** Workflow doesn't run at scheduled times
- **Solution:** Check if repository has recent activity
- GitHub may disable scheduled workflows on inactive repos

---

## ✅ Quick Verification Checklist

- [ ] Can see `GEMINI_API_KEY` in repository Settings → Secrets
- [ ] Workflow runs without "API key not set" errors
- [ ] Posts are being generated successfully
- [ ] No API authentication errors in logs
- [ ] Secret value not visible anywhere in public logs

If all checkboxes are ✅, your secret is correctly configured!

---

**Current Status Check:** Go to https://github.com/kundan007b/bhaskar-daily-ai-news/settings/secrets/actions
