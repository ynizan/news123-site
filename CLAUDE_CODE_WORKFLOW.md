# Claude Code Workflow - MANDATORY

## ⚠️ CRITICAL: Always Run Tests Before Committing

**Every time you make changes to code, data, or templates, you MUST run the pre-commit test suite BEFORE creating any git commits.**

---

## 🔴 Mandatory Pre-Commit Workflow

### Step 1: Make Your Changes
Edit files as requested by the user.

### Step 2: Run Pre-Commit Tests
**REQUIRED - DO NOT SKIP THIS STEP**

```bash
./scripts/pre_commit_tests.sh
```

This script runs:
1. ✅ CSV schema validation
2. ✅ Data quality checks
3. ✅ Site generator
4. ✅ Build output validation
5. ✅ Workflow validation

### Step 3: Fix Any Failures
If tests fail:
- **DO NOT commit**
- Read the test failure messages
- Fix the issues
- Run `./scripts/pre_commit_tests.sh` again
- Repeat until all tests pass

### Step 4: Only Commit When Tests Pass
Once you see:
```
✅ ALL PRE-COMMIT TESTS PASSED
✓ Safe to commit and push
```

Then and ONLY then:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### Step 5: Verify GitHub Actions Pass
**REQUIRED - DO NOT SKIP THIS STEP**

After pushing, ALWAYS verify GitHub Actions tests pass.

#### Method 1: Using GitHub CLI (if available)

```bash
gh run list --limit 1
gh run view --log
```

#### Method 2: Using Bash/Curl (always works)

**Check workflow status:**
```bash
curl -s "https://api.github.com/repos/ynizan/permitindex-site/actions/runs?per_page=1" | \
python3 -c "
import json, sys
data = json.load(sys.stdin)
run = data['workflow_runs'][0]
print(f'Workflow: {run[\"name\"]}')
print(f'Status: {run[\"status\"]}')
print(f'Conclusion: {run[\"conclusion\"]}')
print(f'URL: {run[\"html_url\"]}')
"
```

**Wait for completion (use this after pushing):**
```bash
sleep 120  # Wait 2 minutes for workflow to run
curl -s "https://api.github.com/repos/ynizan/permitindex-site/actions/runs?per_page=1" | \
python3 -c "
import json, sys
data = json.load(sys.stdin)
run = data['workflow_runs'][0]
print(f'Status: {run[\"status\"]}')
print(f'Conclusion: {run[\"conclusion\"]}')
print(f'URL: {run[\"html_url\"]}')
exit(0 if run['conclusion'] == 'success' else 1)
"
```

**Get job details if failed:**
```bash
# First, get the run ID from the URL or status check above
RUN_ID=<run_id_from_above>

# Get job details
curl -s "https://api.github.com/repos/ynizan/permitindex-site/actions/runs/${RUN_ID}/jobs" | \
python3 -c "
import json, sys
data = json.load(sys.stdin)
for job in data['jobs']:
    if job['conclusion'] == 'failure':
        print(f'Failed Job: {job[\"name\"]}')
        print(f'Job URL: {job[\"html_url\"]}')
        for step in job['steps']:
            if step['conclusion'] == 'failure':
                print(f'  Failed Step: {step[\"name\"]}')
"
```

**Access the logs via browser:**
- Visit the URL from the status check
- Click on the failed job
- Expand the failed step to see error details

#### What to do if GitHub Actions fail:

1. **DO NOT ignore it** - this is a real failure
2. Check the logs using one of the methods above
3. Read the error messages carefully
4. Fix the issues locally
5. Run `./scripts/pre_commit_tests.sh` to verify fix
6. Commit and push the fixes
7. Verify again until GitHub Actions pass

**CRITICAL**: Only consider your work complete when BOTH local tests AND GitHub Actions pass.

---

## ❌ What NOT to Do

**NEVER:**
- Commit without running `./scripts/pre_commit_tests.sh`
- Push code that fails local tests
- Assume "it will work in CI/CD"
- Skip tests because "the change is small"

**WHY:**
- Failed builds on Cloudflare Pages block deployment
- Failed GitHub Actions waste time and send error emails
- User has to manually ask you to fix failures
- Breaks the development workflow

---

## ✅ What TO Do

**ALWAYS:**
1. Make changes
2. Run `./scripts/pre_commit_tests.sh`
3. Fix failures if any
4. Commit and push when tests pass

**This ensures:**
- ✅ Cloudflare deployments succeed
- ✅ GitHub Actions tests pass
- ✅ No error emails sent
- ✅ Smooth development workflow

---

## 🎯 Quick Reference

**Before Every Commit:**
```bash
# 1. Test
./scripts/pre_commit_tests.sh

# 2. Only if tests pass:
git add .
git commit -m "Description"
git push origin main
```

---

## 📋 Example Session

```bash
# User asks to add a new permit
$ [Make changes to data/permits/permits.csv]

# MANDATORY: Test before committing
$ ./scripts/pre_commit_tests.sh
❌ SOME TESTS FAILED
  - CSV has invalid URL format in row 5

# Fix the issue
$ [Fix URL in row 5]

# Test again
$ ./scripts/pre_commit_tests.sh
✅ ALL PRE-COMMIT TESTS PASSED

# Now safe to commit
$ git add data/permits/permits.csv
$ git commit -m "Add new permit with valid data"
$ git push origin main
```

---

## 🚨 Emergency: Tests Failing in CI/CD

If GitHub Actions or Cloudflare builds are failing:

1. Pull the latest code: `git pull origin main`
2. Run pre-commit tests: `./scripts/pre_commit_tests.sh`
3. Fix all failures locally
4. Commit the fixes: `git add . && git commit -m "Fix test failures" && git push`

**Never commit fixes without running local tests first!**

---

## 📊 Test Categories

The pre-commit suite runs these critical tests:

| Test | Catches | Time |
|------|---------|------|
| CSV Schema | Wrong columns, missing fields | 2s |
| Data Quality | Invalid URLs, dates, values | 3s |
| Generator | Template errors, syntax issues | 5s |
| Build Output | Missing files, broken builds | 2s |
| Workflows | Invalid YAML, missing configs | 2s |

**Total Time:** ~15 seconds

**Worth It?** YES - Prevents hours of debugging failed deployments

---

## 🎓 Remember

**The Golden Rule:**
> If `./scripts/pre_commit_tests.sh` doesn't pass, don't commit.

**No exceptions. Ever.**
