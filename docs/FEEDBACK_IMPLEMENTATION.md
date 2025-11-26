# Feedback System Implementation Guide

## Overview
Fix the 401 authentication error on the feedback form by deploying a Cloudflare Worker proxy.

---

## Why This Is Needed

**Current Issue:**
- Feedback form shows: ❌ "Sorry, there was an error submitting your feedback"
- GitHub API returns 401 "Requires authentication"
- Can't put GitHub token in client-side JavaScript (security risk)

**Solution:**
- Cloudflare Worker acts as secure proxy
- Token stored safely on Cloudflare's servers
- Frontend → Worker → GitHub API

---

## Implementation Steps

### Step 1: Create GitHub Personal Access Token

1. Navigate to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Configure token:
   - **Note:** `News123 Feedback Worker`
   - **Expiration:** No expiration (or 1 year)
   - **Scopes:** Check ✅ `public_repo`
4. Click **"Generate token"**
5. **COPY THE TOKEN IMMEDIATELY** (you won't see it again)
   - Example: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### Step 2: Install Wrangler CLI

```bash
npm install -g wrangler
```

**Verify installation:**
```bash
wrangler --version
```

---

### Step 3: Login to Cloudflare

```bash
wrangler login
```

This will:
- Open browser window
- Ask you to authorize Wrangler
- Return to terminal when complete

---

### Step 4: Deploy the Worker

```bash
cd /Users/yanivnizan/Downloads/permit-index-site/worker
wrangler deploy
```

**Expected output:**
```
✨ Compiled Worker successfully
✨ Uploading Worker...
✨ Uploaded news123-feedback-proxy (0.65 sec)
✨ Published news123-feedback-proxy (0.32 sec)
  https://news123-feedback-proxy.yaniv-nizan-2e3.workers.dev

✨ Success! Your worker is live at:
   https://news123-feedback-proxy.yaniv-nizan-2e3.workers.dev
```

**COPY THIS URL** - you'll need it in Step 6.

Example: `https://news123-feedback-proxy.yaniv-nizan-2e3.workers.dev`

---

### Step 5: Add GitHub Token as Secret

```bash
wrangler secret put GITHUB_TOKEN
```

**You'll see:**
```
Enter a secret value:
```

**Paste your GitHub token** (the one from Step 1) and press Enter.

**Expected output:**
```
✨ Success! Uploaded secret GITHUB_TOKEN
```

**Verify it was added:**
```bash
wrangler secret list
```

You should see:
```
[
  {
    "name": "GITHUB_TOKEN",
    "type": "secret_text"
  }
]
```

---

### Step 6: Update Frontend Template

Edit: `/Users/yanivnizan/Downloads/permit-index-site/templates/transaction_page.html`

**Find line ~616:**
```javascript
const response = await fetch('https://api.github.com/repos/ynizan/permitindex-site/issues', {
```

**Replace with YOUR Worker URL from Step 4:**
```javascript
const response = await fetch('https://news123-feedback-proxy.yaniv-nizan-2e3.workers.dev', {
```

**Find line ~622-627 (the body parameter):**
```javascript
body: JSON.stringify({
    title: `User Feedback: {{ permit_slug }}`,
    body: `**Permit:** {{ permit_slug }}\n**Type:** ${feedbackType}\n**Feedback:**\n${feedbackText}`,
    labels: ['user-tip', feedbackType]
})
```

**Replace with:**
```javascript
body: JSON.stringify({
    permit_slug: '{{ permit_slug }}',
    feedback_type: feedbackType,
    feedback_text: feedbackText
})
```

**Remove these headers (lines ~618-621):**
```javascript
headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.github.v3+json'
},
```

**Replace with:**
```javascript
headers: {
    'Content-Type': 'application/json'
},
```

---

### Step 7: Regenerate Site

```bash
cd /Users/yanivnizan/Downloads/permit-index-site
python3 generator.py
```

**Expected output:**
```
✅ Site generation completed successfully!
```

---

### Step 8: Commit and Deploy

```bash
git add templates/transaction_page.html output/
git commit -m "Fix feedback form 401 error - use Cloudflare Worker proxy

- Update fetch URL to use Worker endpoint
- Simplify request body (Worker handles GitHub API format)
- Remove unnecessary GitHub-specific headers
- Fixes authentication error on feedback submissions"

git push origin main
```

**Wait 2-3 minutes** for Cloudflare Pages to rebuild.

---

### Step 9: Test It!

1. **Open:** https://news123.info/california/contractor-license/

2. **Fill out feedback form:**
   - Select: 💡 Helpful Tip
   - Enter: "Testing the new Worker proxy"
   - Click: Submit Feedback

3. **Expected result:**
   ```
   ✅ Thank you! Your feedback has been submitted and will
      appear on the site after review (usually within 24 hours).
   ```

4. **Verify on GitHub:**
   - Go to: https://github.com/ynizan/permitindex-site/issues
   - You should see a new issue titled: "User Feedback: contractor-license"
   - It should have labels: `user-tip` and `tip`

---

## Troubleshooting

### Error: "Failed to create issue"

**Check Worker logs:**
```bash
cd worker
wrangler tail
```

Then submit the form again. You'll see real-time logs showing what went wrong.

**Common fixes:**
- Verify GITHUB_TOKEN is set: `wrangler secret list`
- Regenerate GitHub token if it expired
- Check token has `public_repo` scope

---

### Error: "CORS policy" or "blocked by CORS"

**Check:**
- Worker URL is correct in template
- No typos in the fetch URL
- Worker is deployed: Visit the Worker URL directly, should return "Method not allowed" (that's good!)

---

### Form still shows old error

**Clear cache:**
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
- Or wait 5 minutes for Cloudflare cache to clear

---

## Architecture Diagram

```
┌─────────────────┐
│   User Browser  │
│  (JavaScript)   │
└────────┬────────┘
         │ POST /
         │ {permit_slug, feedback_type, feedback_text}
         ▼
┌─────────────────────────────────┐
│   Cloudflare Worker             │
│   news123-feedback-proxy    │
│                                 │
│   Secrets:                      │
│   - GITHUB_TOKEN (secure)       │
│                                 │
│   Validates input               │
│   Adds authentication           │
└────────┬────────────────────────┘
         │ POST /repos/.../issues
         │ Authorization: Bearer {token}
         │ {title, body, labels}
         ▼
┌─────────────────┐
│   GitHub API    │
│                 │
│   Creates Issue │
│   Returns #123  │
└─────────────────┘
```

---

## Cost

**Cloudflare Workers Free Tier:**
- 100,000 requests/day
- 10ms CPU time per request
- Free SSL/TLS

**More than enough for feedback submissions.**

If you exceed 100k requests/day (you won't), it's only $0.50 per million additional requests.

---

## Security

✅ **GitHub token never exposed to users**
✅ **Stored in Worker secrets (encrypted)**
✅ **Input validation on Worker**
✅ **CORS headers restrict access**
✅ **Rate limiting via GitHub API (5000 req/hour)**

---

## Next Steps After Deployment

### 1. Monitor Issues
Watch: https://github.com/ynizan/permitindex-site/issues

New feedback will appear as issues with label `user-tip`.

### 2. Approve Feedback
To approve and display on site:
1. Review the issue
2. Add label: `approved`
3. GitHub Action automatically updates CSV
4. Site rebuilds with approved feedback

### 3. Optional: Custom Domain
Instead of `.workers.dev` URL, use `api.news123.info/feedback`:

**In Cloudflare Dashboard:**
- Workers → news123-feedback-proxy → Settings → Triggers
- Add Route: `news123.info/api/feedback`
- Update template to use this URL

---

## Questions?

If anything doesn't work:

1. Check Worker logs: `wrangler tail`
2. Verify Worker URL in template matches deployed URL
3. Confirm GITHUB_TOKEN is set: `wrangler secret list`
4. Check GitHub token hasn't expired

**All files are in the repo under `/worker/` directory.**
