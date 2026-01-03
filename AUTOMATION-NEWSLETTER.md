# Newsletter to Google Sheets Automation

These steps provision a free Google Apps Script endpoint that accepts the JSON payload sent by `/assets/js/newsletter.js`, stores each submission in a Google Sheet, and returns a JSON response consumed by the site.

## 1. Prepare the Google Sheet
1. Create a new Google Sheet (e.g., `KB Tech News Subscribers`).
2. Rename the first sheet to `Subscribers`.
3. Add headings in row 1: `Timestamp`, `Email`, `Page`, `User Agent`.

## 2. Add the Apps Script
1. In the Google Sheet, click **Extensions → Apps Script**.
2. Delete any placeholder code and paste the script below:

```javascript
const SHEET_NAME = 'Subscribers';

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return _jsonResponse({ success: false, message: 'No payload supplied.' });
    }

    let data;
    try {
      data = JSON.parse(e.postData.contents);
    } catch (error) {
      return _jsonResponse({ success: false, message: 'Invalid JSON.', detail: error.message });
    }

    const email = (data.email || '').trim().toLowerCase();
    if (!email) {
      return _jsonResponse({ success: false, message: 'Email is required.' });
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return _jsonResponse({ success: false, message: 'Invalid email format.' });
    }

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sheet) {
      return _jsonResponse({ success: false, message: 'Sheet not found. Ensure a sheet named "Subscribers" exists.' });
    }

    sheet.appendRow([
      new Date(),
      email,
      data.page || '',
      data.userAgent || ''
    ]);

    return _jsonResponse({ success: true, message: 'Thanks for subscribing!' });
  } catch (error) {
    return _jsonResponse({ success: false, message: 'Server error.', detail: error.toString() });
  }
}

function _jsonResponse(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3. Press **Ctrl+S** and name the project (e.g., `Newsletter Webhook`).

## 3. Deploy as a Web App
1. Click **Deploy → New deployment** (blue button in top right).
2. Click the **Select type** gear icon → choose **Web app**.
3. Configure the deployment:
   - **Description**: `Newsletter subscriber endpoint`
   - **Execute as**: `Me` (your account)
   - **Who has access**: **Anyone** (NOT "Anyone with Google account")
4. Click **Deploy**.
5. **Authorize** the script when prompted:
   - Click "Authorize access"
   - Select your Google account
   - Click "Advanced" → "Go to [Project Name] (unsafe)"
   - Click "Allow"
6. Copy the **Web app URL** (ends with `/exec`).
7. **Test immediately** by running this command (replace URL):
   ```bash
   curl -L "YOUR_WEB_APP_URL" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","page":"/","userAgent":"curl"}'
   ```
   Should return: `{"success":true,"message":"Thanks for subscribing!"}`

## 4. Wire the site
1. Update `_config.yml` → `forms.newsletter_endpoint` with the Web App URL you copied.
2. Commit and redeploy the site. The value is exposed globally via `window.NEWSLETTER_ENDPOINT`, so no further code changes are required.

## 5. Verify
1. **Test from command line first** (see step 3 above) - if this fails, the web app won't work either.
2. Open any site page, enter an email, and click **Subscribe**.
3. Confirm the success toast appears and a new row is recorded in the `Subscribers` sheet.
4. If you see "Subscription failed":
   - Open browser DevTools (F12) → Console tab
   - Try subscribing again and check for CORS errors
   - Verify the deployment URL in `_config.yml` matches exactly (including `/exec`)
   - Redeploy the script as a **new version** (Deploy → Manage deployments → Edit → Version: New version)

## Troubleshooting

**"Page not found" or redirect errors**:
- The deployment URL is wrong or the script isn't properly deployed
- Redeploy: Deploy → New deployment → Web app
- Ensure "Who has access" is set to **Anyone** (not "Anyone with Google account")

**CORS errors in browser**:
- Apps Script must be deployed with "Execute as: Me" and "Who has access: Anyone"
- Try creating a completely new deployment instead of updating existing one

**Empty endpoint / button disabled**:
- Check `_config.yml` has `forms.newsletter_endpoint` set
- Rebuild site: `bundle exec jekyll build`
- Push changes: `git push origin main`

> Note: Google Apps Script quotas (per-minute executions, daily writes) easily cover typical newsletter volumes. If you expect heavy traffic, consider enabling an external service (Make/Zapier, Cloud Run, etc.) and simply update the endpoint value.
