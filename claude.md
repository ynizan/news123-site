# PermitIndex - AI Assistant Guide

**Quick Reference for Claude Code and AI Assistants**

---

## 🚨 CRITICAL: Read This First

### Mandatory Pre-Commit Workflow

**NEVER commit code without following this process:**

1. Make your changes
2. Run `./scripts/pre_commit_tests.sh`
3. Fix any failures
4. Only commit when tests pass
5. After pushing, verify GitHub Actions pass

**Why?** Prevents broken builds, failed deployments, and wasted CI/CD cycles.

📖 **Full details**: `CLAUDE_CODE_WORKFLOW.md`

### 🔍 CRITICAL: Thin Content SEO Protection

**Every code change MUST pass thin content tests:**

Thin content pages (< 800 chars) are automatically protected from Google penalties by:
- **Noindex meta tags** - prevents indexing
- **Low sitemap priority (0.3)** - deprioritizes crawling
- **Follow directive** - preserves internal link equity

**The automated tests verify:**
1. ✅ Thin content pages have noindex tags
2. ✅ Thin content pages are deprioritized in sitemap
3. ✅ Quality pages (≥ 800 chars) are indexed normally
4. ✅ Noindex uses "follow" to maintain link equity

**When tests fail:**
- ❌ Thin content is exposed → Risk of Google penalty
- ❌ Quality content is noindexed → Loss of organic traffic
- ❌ Sitemap priorities wrong → Wasted crawl budget

**Tests run automatically:**
- Every commit (pre-commit hook)
- Every push to branch (CI)
- Every merge to main (CI)
- Weekly SEO test suite

📊 **View test code:** `tests/critical/test_thin_content.py` and `tests/seo/test_thin_content.py`

### Mandatory Git Sync Before Starting

**ALWAYS check for remote changes before starting any work:**

```bash
# Step 1: Check for remote changes (SAFE - doesn't change anything local)
git fetch origin

# Step 2: See what's different
git status

# Step 3: ONLY if you see "Your branch is behind", decide what to do:
# - If NO local changes: safe to pull
git pull origin <branch-name>

# - If you HAVE local changes: review differences first
git log HEAD..origin/<branch-name>  # See what's new on remote
git diff HEAD origin/<branch-name>  # See actual changes
# Then decide: merge, rebase, or ask user
```

**What is `git fetch`?**
- ✅ **SAFE**: Only downloads remote info, doesn't change your files
- ✅ **Non-destructive**: Your local changes stay untouched
- ✅ **Smart**: Lets you review differences before applying changes

**When to check for remote changes:**
- ✅ **Every time Claude Code starts a new conversation with you**
- ✅ **Before making any code changes**
- ✅ **When user mentions they worked on their MacBook**
- ✅ **When you see "unpushed commits" warnings**

**Red flags that mean you need to sync:**
- Stop hook warning: "There are X unpushed commit(s)"
- User says "I just pushed some changes"
- Git push fails with "rejected" or "non-fast-forward"
- User mentions working locally

---

## 📁 Project Overview

**PermitIndex** is a static site generator for US government permits and licenses.

### Tech Stack
- **Generator**: Python 3.11+ with Jinja2 templates
- **Data**: CSV files (27-column schema)
- **Output**: Static HTML (deployed to Cloudflare Pages)
- **Testing**: Pytest + Playwright
- **Search**: Pagefind (static search)

### Key Files
```
permitindex-site/
├── generator.py              # Main site generator
├── data/
│   ├── permits.csv          # 27-column permit data (see CSV_SCHEMA.md)
│   ├── contributors.csv     # Contributor database
│   └── user_feedback.csv    # Approved user feedback
├── templates/               # Jinja2 templates
│   ├── index.html          # Homepage
│   ├── jurisdiction_hub.html
│   └── transaction_page.html
├── output/                  # Generated site (git-ignored)
├── tests/                   # Pytest test suites
│   ├── critical/           # Run on every commit
│   ├── data/               # CSV validation
│   ├── seo/                # Weekly SEO tests
│   └── visual/             # Daily visual tests
└── scripts/
    └── pre_commit_tests.sh  # Mandatory pre-commit script
```

---

## 🎨 Brand System (CRITICAL)

### CSS Variables Only

**ALWAYS use CSS variables** from `static/css/variables.css`:

```css
/* Correct */
color: var(--primary);           /* #003366 - Primary Blue */
background: var(--accent);       /* #FF6B35 - Accent Orange */
color: var(--text);              /* #1a1a1a - Body text */
background: var(--bg-light);     /* #f8f9fa - Page background */
```

### Common Mistakes

```html
<!-- ❌ WRONG: Tailwind color classes -->
<div class="text-blue-600 bg-gray-50">

<!-- ❌ WRONG: Hardcoded hex values -->
<div style="color: #003366;">

<!-- ✅ CORRECT: CSS variables -->
<div style="color: var(--primary); background: var(--bg-light);">
```

### Complete Color Palette

| Variable | Hex | Usage |
|----------|-----|-------|
| `--primary` | #003366 | Headers, links, primary buttons |
| `--accent` | #FF6B35 | CTAs, highlights (use sparingly) |
| `--text` | #1a1a1a | Body text |
| `--text-light` | #666666 | Secondary text, labels |
| `--bg` | #FFFFFF | Card backgrounds |
| `--bg-light` | #F8F9FA | Page background |
| `--border` | #E0E0E0 | Borders, dividers |
| `--success` | #10B981 | Success badges |

📖 **Full guidelines**: `docs/BRAND_GUIDELINES.md`, `docs/DEVELOPER.md`

---

## 📊 Data Schema

### permits.csv - 27 Columns

**8 Required columns** (cannot be empty):
- `agency_short`, `agency_full`, `request_type`
- `cost`, `location_applicability`, `effort_hours`
- `online_available`, `api_available`

**19 Optional columns** for rich content:
- Contact info: `agency_phone`, `agency_email`, `agency_address`, `agency_hours`
- Community content: `common_mistakes`, `community_feedback`, `user_tips`, `faqs`
- Metadata: `related_pages`, `date_extracted`, `source_url`, `verified_by`

**JSON fields** (must be valid JSON arrays):
- `community_feedback`: `["Feedback 1", "Feedback 2"]`
- `user_tips`: `["Tip 1", "Tip 2"]`
- `faqs`: `[{"question": "Q?", "answer": "A."}]`

📖 **Full schema**: `CSV_SCHEMA.md`

---

## 🧪 Testing

### Pre-Commit (Mandatory)
```bash
./scripts/pre_commit_tests.sh
```

Runs:
1. CSV schema validation
2. Data quality checks
3. Site generation
4. Build output validation
5. Workflow validation

**Time**: ~15 seconds
**Mandatory**: YES - never skip this

### Test Suites
```bash
# Critical tests (run on every push)
pytest tests/critical/ -m critical

# All tests
pytest tests/

# Specific suite
pytest tests/seo/ -m seo
pytest tests/visual/ -m visual
```

### GitHub Actions

After pushing, **ALWAYS verify** GitHub Actions pass:
```bash
# Check latest workflow status
gh run list --limit 1
gh run view --log
```

Or visit: https://github.com/ynizan/permitindex-site/actions

📖 **Full testing guide**: `docs/TESTING_IMPLEMENTATION_GUIDE.md`

---

## 🌿 Feature Branch Workflow

**ALWAYS use feature branches for new work. NEVER commit directly to main.**

### Creating a Feature Branch

```bash
# 1. Start from latest main
git fetch origin
git checkout main
git pull origin main

# 2. Create feature branch (use descriptive name)
git checkout -b claude/<short-description>-<session-id>

# Examples:
# claude/add-search-feature-01XyZ123
# claude/fix-css-variables-02AbC456
# claude/update-csv-schema-03DeF789
```

### Working on Feature Branch

```bash
# 1. Make your changes
# 2. Run pre-commit tests
./scripts/pre_commit_tests.sh

# 3. Commit (can make multiple commits)
git add .
git commit -m "Clear description of change"

# 4. Push to remote
git push -u origin claude/<branch-name>
```

### Merging to Main

**Option 1: From MacBook (Direct Merge)**
```bash
# On MacBook after Claude pushes feature branch
git fetch origin
git checkout main
git merge origin/claude/<branch-name>
git push origin main

# Clean up
git branch -d claude/<branch-name>
git push origin --delete claude/<branch-name>
```

**Option 2: Pull Request (Preferred for review)**

**A. Using Claude Code Web** (generates clickable PR links):
```bash
# Generate PR URL
BRANCH=$(git branch --show-current)
echo "🔗 PR Link: https://github.com/ynizan/permitindex-site/pull/new/$BRANCH"

# Or open directly in browser (macOS):
open "https://github.com/ynizan/permitindex-site/pull/new/$BRANCH"
```

**B. Using CLI/Terminal on local machine:**
```bash
# Use GitHub CLI (no manual URL needed)
gh pr create --fill  # Auto-generates title/body from commits
gh pr create         # Interactive mode with prompts
```

**URL Pattern** (for manual browser access):
```
https://github.com/ynizan/permitindex-site/pull/new/<branch-name>
```

### When to Use Feature Branches

✅ **Always use for:**
- New features
- Bug fixes
- Documentation updates
- Refactoring
- Any change that could break things

❌ **Never use for:**
- Nothing! Always use feature branches

### Branch Naming Convention

```
claude/<description>-<session-id>
```

**Examples:**
- `claude/cleanup-project-folder-01AbSfWKC4B9pEyY8qgXvkhK`
- `claude/add-pagefind-search-02XyZ789`
- `claude/fix-brand-colors-03DeF456`

**Why this format?**
- `claude/` prefix: Identifies AI-generated branches
- `<description>`: Clear, kebab-case description
- `<session-id>`: Unique identifier prevents conflicts

---

## 🚀 Common Tasks

### Add a New Permit

1. Edit `data/permits/permits.csv`:
   - Follow 27-column schema
   - Fill 8 required fields
   - Validate JSON fields if using them

2. Run pre-commit tests:
   ```bash
   ./scripts/pre_commit_tests.sh
   ```

3. Fix any failures, repeat until all pass

4. Generate and preview:
   ```bash
   python3 generator.py
   cd output && python3 -m http.server 8000
   # Visit http://localhost:8000
   ```

5. Commit and push:
   ```bash
   git add data/permits/permits.csv output/
   git commit -m "Add new permit: [description]"
   git push origin main
   ```

6. Verify GitHub Actions pass

### Modify Templates

1. Edit files in `templates/`:
   - Use CSS variables, NEVER Tailwind color classes
   - Use `data-pagefind-body` for searchable content
   - Follow brand guidelines

2. Run pre-commit tests:
   ```bash
   ./scripts/pre_commit_tests.sh
   ```

3. Check generated output in `output/`

4. Commit and push

### Add a New Contributor

1. Edit `data/contributors/contributors.csv`:
   ```csv
   contributor_id,name,city,state,expertise,website,bio,date_added
   john-doe,John Doe,Boston,MA,"Business Licenses",https://example.com,Bio text,2025-11-18
   ```

2. Assign permits in `data/permits/permits.csv`:
   - Set `verified_by` column to `john-doe`

3. Run pre-commit tests and deploy

---

## ⚠️ Common Pitfalls

### NEVER Do This

❌ **Commit directly to main** → Always use feature branches
❌ **Start work without checking remote** (`git fetch origin`) → Creates merge conflicts
❌ **Blindly pull without checking differences** → Can override important changes
❌ **Skip pre-commit tests** → Causes build failures, wastes time
❌ **Use Tailwind color classes** (`text-blue-600`) → Breaks brand consistency
❌ **Hardcode hex colors** (`#003366`) → Should use `var(--primary)`
❌ **Ignore GitHub Actions failures** → Leaves broken code in production
❌ **Edit output/ directly** → Gets overwritten by generator
❌ **Invalid JSON in CSV** → Breaks site generation
❌ **Empty required CSV columns** → Validation fails
❌ **Commit without verifying tests** → Breaks CI/CD pipeline

### Always Do This

✅ **Create feature branch** for all new work (`git checkout -b claude/<description>-<session-id>`)
✅ **Check for remote changes** (`git fetch origin`) at start of each conversation
✅ **Review differences** before pulling if you have local changes
✅ **Ask user** if you find conflicts between local and remote
✅ **Run `./scripts/pre_commit_tests.sh`** before every commit
✅ **Use CSS variables** for all colors
✅ **Verify GitHub Actions pass** after pushing
✅ **Test locally** before committing (use http.server)
✅ **Follow CSV schema** exactly (27 columns, correct types)
✅ **Validate JSON fields** using jsonlint.com
✅ **Read error messages carefully** and fix root cause

---

## 📚 Documentation Reference

### Essential (Read First)
- **README.md** - Project overview and setup
- **CLAUDE_CODE_WORKFLOW.md** - Mandatory pre-commit workflow
- **CSV_SCHEMA.md** - Complete data schema (27 columns)

### Brand & Design
- **docs/BRAND_GUIDELINES.md** - Complete brand system
- **docs/DEVELOPER.md** - Color usage and accessibility
- **docs/BRAND_IMPLEMENTATION_GUIDE.md** - Technical implementation

### Development
- **docs/TESTING_IMPLEMENTATION_GUIDE.md** - Test suite setup
- **docs/BUILD_TEST_PLAN.md** - CI/CD and deployment
- **docs/FEEDBACK_IMPLEMENTATION.md** - User feedback system

---

## 🔧 Quick Reference

### Generate Site
```bash
python3 generator.py
```

### Run Pre-Commit Tests
```bash
./scripts/pre_commit_tests.sh
```

### Create Pull Request (Claude Code Web only)
```bash
# Generate PR link for current branch (use when working in Claude Code Web)
BRANCH=$(git branch --show-current)
echo "🔗 https://github.com/ynizan/permitindex-site/pull/new/$BRANCH"

# Or open directly in browser (macOS):
open "https://github.com/ynizan/permitindex-site/pull/new/$BRANCH"
```
**Note:** When using CLI/terminal on local machine, use `gh` CLI instead:
```bash
gh pr create --fill  # Creates PR with auto-generated title/body
```

### Test Locally
```bash
cd output
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Run Specific Tests
```bash
pytest tests/critical/ -m critical  # Critical only
pytest tests/data/ -v               # Data validation
pytest tests/seo/ -m seo           # SEO tests
pytest tests/                      # All tests
```

### Check GitHub Actions
```bash
gh run list --limit 1              # Latest run
gh run view --log                  # View logs
```

---

## 🎯 Success Checklist

Before considering any task complete:

- [ ] Pre-commit tests pass locally
- [ ] Code follows brand guidelines (CSS variables)
- [ ] Changes committed with clear message
- [ ] Pushed to GitHub
- [ ] GitHub Actions workflow passes
- [ ] Spot-checked output in browser
- [ ] No console errors in browser DevTools

---

## 🆘 Troubleshooting

### Pre-Commit Tests Fail
1. Read error message carefully
2. Check which test failed (CSV, generator, etc.)
3. Fix the root cause
4. Run tests again
5. Repeat until all pass

### GitHub Actions Fail
1. Visit https://github.com/ynizan/permitindex-site/actions
2. Click on failed workflow
3. Expand failed step
4. Read error logs
5. Fix locally, run pre-commit tests
6. Push fix

### CSV Validation Errors
1. Check column count: `head -1 data/permits/permits.csv | awk -F',' '{print NF}'` (should be 27)
2. Validate JSON fields at jsonlint.com
3. Verify required fields not empty
4. Check for trailing commas or quotes

### Brand Violations
1. Search for Tailwind classes: `grep -r "text-blue-" templates/`
2. Search for hex colors: `grep -r "#[0-9A-Fa-f]\{6\}" templates/`
3. Replace with CSS variables
4. See `docs/DEVELOPER.md` for mapping guide

---

## 📞 Getting Help

- **GitHub Issues**: https://github.com/ynizan/permitindex-site/issues
- **Workflow Errors**: Check `CLAUDE_CODE_WORKFLOW.md`
- **Schema Questions**: Check `CSV_SCHEMA.md`
- **Brand Questions**: Check `docs/BRAND_GUIDELINES.md`

---

**Last Updated**: 2025-11-18
**Version**: 1.0
**Status**: Production
