# Re-test Issue #6 After Workflow Fix

## Current Status
- Issue #6 is OPEN (should have been closed)
- Has label: "approved"
- NOT in CSV (workflow failed before adding it)
- Previous workflow failed with: `cannot pull with rebase: You have unstaged changes`

## Fix Applied
Changed line order in `.github/workflows/approve-feedback.yml`:
```yaml
# BEFORE (failed):
git pull --rebase origin main
git add data/feedback/user_feedback.csv

# AFTER (fixed):
git add data/feedback/user_feedback.csv
git pull --rebase origin main
```

## How to Re-test

### Method 1: Re-run Failed Workflow
1. Visit: https://github.com/ynizan/permitindex-site/actions
2. Look for failed "Approve User Feedback" run
3. Click on the workflow run
4. Click "Re-run all jobs" (top right corner)
5. Monitor the workflow - should complete successfully now

### Method 2: Remove and Re-add Label
1. Visit: https://github.com/ynizan/permitindex-site/issues/6
2. Click the X on the "approved" label to remove it
3. Wait 2 seconds
4. Click "Labels" and add "approved" back
5. Go to Actions tab to monitor the new workflow run

## Expected Results

After re-running the workflow:

1. **Workflow completes successfully** ✅
   - All steps green
   - No git errors

2. **CSV is updated** ✅
   ```csv
   contractor-license,tip,Second validation test - checking workflow improvements,0,2025-11-16,yes,6
   ```

3. **Issue #6 is closed** ✅
   - State changes to CLOSED
   - Bot comment added: "✅ This feedback has been approved..."

4. **Cloudflare Pages rebuilds** ✅
   - Check deployments tab
   - Wait 2-3 minutes

5. **Feedback appears on live site** ✅
   - Visit: https://news123.info/california/contractor-license/
   - Look for "Community Contributions" section
   - Should show: "Second validation test - checking workflow improvements"

## Verification Commands

```bash
# Check if Issue #6 is in CSV
curl -s https://raw.githubusercontent.com/ynizan/permitindex-site/main/data/feedback/user_feedback.csv | grep ",6$"

# Check issue status
curl -s https://api.github.com/repos/ynizan/permitindex-site/issues/6 | python3 -c "import sys, json; i = json.load(sys.stdin); print(f'State: {i[\"state\"]}, Labels: {[l[\"name\"] for l in i[\"labels\"]]}')"

# Check recent workflow runs
curl -s https://api.github.com/repos/ynizan/permitindex-site/actions/runs?per_page=3 | python3 -c "import sys, json; runs = json.load(sys.stdin)['workflow_runs']; [print(f'{r[\"name\"]}: {r[\"status\"]} - {r[\"conclusion\"]}') for r in runs]"
```

## Timeline

| Time | Event |
|------|-------|
| 0:00 | Re-run workflow or re-add label |
| 0:10 | Workflow starts |
| 0:30 | Workflow completes ✅ |
| 0:31 | CSV updated with Issue #6 |
| 0:32 | Issue #6 closed |
| 0:45 | Cloudflare Pages rebuild starts |
| 3:00 | Site deployed with new feedback |

## If It Still Fails

Check workflow logs for:
- Specific git error message
- Python parsing errors
- CSV file conflicts

The fix ensures that CSV changes are staged BEFORE pulling, which should prevent all "unstaged changes" errors.
