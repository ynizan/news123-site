# Quick Test Guide - Approval Workflow

## For Manual Testing (You)

### Option 1: Run the Automated Test Script

```bash
cd /Users/yanivnizan/Downloads/permit-index-site
python3 tests/test_approval_workflow.py
```

**The script will:**
1. Prompt you to add the "approved" label to Issue #4
2. Monitor GitHub Actions workflow every 10 seconds
3. Check CSV file for updates
4. Verify issue gets closed
5. Check if feedback appears on live site
6. Report success/failure with detailed status

**Runtime**: 3-5 minutes (includes 2-minute wait for Cloudflare Pages)

---

### Option 2: Manual Step-by-Step Testing

1. **Add label**:
   - Go to https://github.com/ynizan/permitindex-site/issues/4
   - Add label: `approved`

2. **Check workflow**:
   - Go to https://github.com/ynizan/permitindex-site/actions
   - Verify "Approve User Feedback" workflow runs successfully

3. **Verify CSV**:
   ```bash
   curl https://raw.githubusercontent.com/ynizan/permitindex-site/main/data/feedback/user_feedback.csv | grep ",4$"
   ```
   Should show: `approved='yes'` for issue #4

4. **Check issue**:
   - Go to https://github.com/ynizan/permitindex-site/issues/4
   - Should be CLOSED with bot comment

5. **Check live site** (wait 2-3 min for rebuild):
   - Visit https://permitindex.com/california/contractor-license/
   - Look for "Community Contributions" section
   - Should show: "Testing from Comet - validation check"

---

## For Comet (AI Browser)

**Full instructions**: See `COMET_TEST_INSTRUCTIONS.md`

**Quick version**:
1. Navigate to Issue #4 and add "approved" label
2. Take 8 screenshots as you verify each step
3. Provide test report with results

---

## Expected Timeline

| Time | Event |
|------|-------|
| 0:00 | Add "approved" label to Issue #4 |
| 0:10 | GitHub Actions workflow starts |
| 0:30 | Workflow completes, CSV updated, issue closed |
| 0:45 | Cloudflare Pages rebuild starts |
| 3:00 | Cloudflare Pages deployment complete |
| 3:30 | Feedback visible on live site (after cache clears) |

---

## Success Checklist

- [ ] Issue #4 is closed
- [ ] Issue has bot comment about approval
- [ ] CSV shows `contractor-license,tip,Testing from Comet - validation check,0,2025-11-16,yes,4`
- [ ] Only ONE entry for issue #4 (no duplicates)
- [ ] Workflow "Approve User Feedback" completed successfully
- [ ] No merge conflicts in workflow logs
- [ ] Feedback appears in "Community Contributions" on https://permitindex.com/california/contractor-license/

---

## Troubleshooting

### Workflow Fails with Git Error
**Problem**: `error: failed to push some refs`
**Solution**: The `git pull --rebase` should prevent this. If it still happens, check workflow logs.

### CSV Not Updated
**Problem**: Workflow succeeds but CSV unchanged
**Solution**: Check workflow logs for "already exists" message. May indicate duplicate detection.

### Feedback Not on Site
**Problem**: CSV updated, but site doesn't show feedback
**Solution**:
- Wait 5 minutes for Cloudflare Pages rebuild
- Hard refresh browser (Cmd+Shift+R)
- Check if `approved='yes'` in CSV
- Verify generator.py filters for `approved='yes'`

---

## Files Created

- `tests/test_approval_workflow.py` - Automated monitoring script
- `COMET_TEST_INSTRUCTIONS.md` - Detailed instructions for Comet
- `tests/QUICK_TEST_GUIDE.md` - This file
