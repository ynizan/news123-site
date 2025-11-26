# Cloudflare Worker Setup for Feedback Proxy

## Problem
The feedback form was returning 401 errors because GitHub's API requires authentication to create issues. We can't put a GitHub token in client-side JavaScript.

## Solution
A Cloudflare Worker acts as a secure proxy between the frontend and GitHub's API.

---

## Setup Steps

### 1. Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "News123 Feedback Worker"
4. Select scopes:
   - ✅ `public_repo` (if repo is public)
   - ✅ `repo` (if repo is private)
5. Click "Generate token"
6. **COPY THE TOKEN** - you won't see it again!

### 2. Install Wrangler CLI (if not already installed)

```bash
npm install -g wrangler
```

### 3. Login to Cloudflare

```bash
wrangler login
```

### 4. Deploy the Worker

From the `worker/` directory:

```bash
cd worker
wrangler deploy
```

This will output something like:
```
Published news123-feedback-proxy (0.01 sec)
  https://news123-feedback-proxy.your-subdomain.workers.dev
```

**COPY THIS URL** - you'll need it for the next step.

### 5. Add GitHub Token as Secret

```bash
wrangler secret put GITHUB_TOKEN
```

When prompted, paste your GitHub Personal Access Token.

### 6. Update the Frontend

Edit `templates/transaction_page.html` and find this line (around line 616):

```javascript
const response = await fetch('https://api.github.com/repos/ynizan/permitindex-site/issues', {
```

Replace it with:

```javascript
const response = await fetch('https://news123-feedback-proxy.YOUR-SUBDOMAIN.workers.dev', {
```

Replace `YOUR-SUBDOMAIN` with your actual Worker URL from step 4.

Also update the request body:

**BEFORE:**
```javascript
body: JSON.stringify({
    title: `User Feedback: {{ permit_slug }}`,
    body: `**Permit:** {{ permit_slug }}\n**Type:** ${feedbackType}\n**Feedback:**\n${feedbackText}`,
    labels: ['user-tip', feedbackType]
})
```

**AFTER:**
```javascript
body: JSON.stringify({
    permit_slug: '{{ permit_slug }}',
    feedback_type: feedbackType,
    feedback_text: feedbackText
})
```

### 7. Regenerate and Deploy

```bash
python3 generator.py
git add .
git commit -m "Update feedback form to use Cloudflare Worker proxy"
git push
```

---

## Testing

1. Visit any permit page: https://news123.info/california/contractor-license/
2. Fill out the feedback form
3. Submit
4. You should see: ✅ "Thank you! Your feedback has been submitted..."
5. Check GitHub Issues to confirm it was created

---

## Troubleshooting

### Error: "Failed to create issue"

- Check that GITHUB_TOKEN is set correctly:
  ```bash
  wrangler secret list
  ```

- Verify token has correct permissions (public_repo or repo scope)

### Error: "Method not allowed"

- Worker only accepts POST requests
- Check that you're using the correct Worker URL

### CORS errors

- Worker includes proper CORS headers
- If still getting CORS errors, check Worker logs:
  ```bash
  wrangler tail
  ```

---

## Optional: Custom Domain

Instead of `news123-feedback-proxy.workers.dev`, you can use:
`api.news123.info/feedback`

1. In Cloudflare dashboard: Workers → news123-feedback-proxy → Settings → Triggers
2. Add Custom Domain or Route:
   - Pattern: `news123.info/api/feedback`
   - Worker: news123-feedback-proxy

Then update the fetch URL in your template to:
```javascript
const response = await fetch('https://news123.info/api/feedback', {
```

---

## Security Notes

- ✅ GitHub token is stored securely in Worker secrets (not exposed)
- ✅ Worker validates all inputs before creating issues
- ✅ CORS headers allow requests from any origin (you can restrict this if needed)
- ✅ Rate limiting handled by GitHub (5000 req/hour with token)

---

## Cost

Cloudflare Workers Free Tier includes:
- 100,000 requests/day
- More than enough for feedback submissions

If you exceed this, it's $0.50 per million requests.
