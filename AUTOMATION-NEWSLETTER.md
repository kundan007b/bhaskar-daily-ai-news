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
  if (!e || !e.postData || !e.postData.contents) {
    return _jsonResponse({ success: false, message: 'No payload supplied.' }, 400);
  }

  let data;
  try {
    data = JSON.parse(e.postData.contents);
  } catch (error) {
    return _jsonResponse({ success: false, message: 'Invalid JSON.', detail: error.message }, 400);
  }

  const email = (data.email || '').trim().toLowerCase();
  if (!email) {
    return _jsonResponse({ success: false, message: 'Email is required.' }, 422);
  }

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  sheet.appendRow([
    new Date(),
    email,
    data.page || '',
    data.userAgent || ''
  ]);

  return _jsonResponse({ success: true, message: 'Subscriber added.' });
}

function _jsonResponse(payload, statusCode) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON)
    .setStatusCode(statusCode || 200);
}
```

3. Press **Ctrl+S** and name the project (e.g., `Newsletter Webhook`).

## 3. Deploy as a Web App
1. Click **Deploy → Test deployments → Select type → Web app** (or **Deploy → New Deployment** in the new UI).
2. Set **Execute as**: `Me`.
3. Set **Who has access**: `Anyone` (or `Anyone with the link`).
4. Click **Deploy** and authorize the script when prompted.
5. Copy the **Web App URL**; it should look like `https://script.google.com/macros/s/DEPLOYMENT_ID/exec`.

## 4. Wire the site
1. Update `_config.yml` → `forms.newsletter_endpoint` with the Web App URL you copied.
2. Commit and redeploy the site. The value is exposed globally via `window.NEWSLETTER_ENDPOINT`, so no further code changes are required.

## 5. Verify
1. Open any site page, enter an email, and click **Subscribe**.
2. Confirm the success toast appears and a new row is recorded in the `Subscribers` sheet.
3. Optionally, build an Apps Script trigger to send yourself an email notification per signup.

> Note: Google Apps Script quotas (per-minute executions, daily writes) easily cover typical newsletter volumes. If you expect heavy traffic, consider enabling an external service (Make/Zapier, Cloud Run, etc.) and simply update the endpoint value.
