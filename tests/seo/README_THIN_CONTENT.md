# Thin Content SEO Protection Tests

## Overview

These automated tests ensure that pages with thin content are properly protected from Google penalties. They run on every commit and merge to prevent regressions.

## What is Thin Content?

Thin content is defined as pages with minimal unique text that provide little value to users. Google penalizes sites with excessive thin content.

### Our Definition

A page is considered "thin content" if:
1. Generic "Apply for a business license" **AND** < 800 chars total content
2. **OR** any page with < 800 chars **AND** missing common mistakes **AND** no community content
3. **OR** pages with description < 200 chars

### Content Calculation

Total content = `description` + `eligibility` + `how_to_description` + `common_mistakes`

## Protection Strategy

Thin content pages are protected by:

1. **Noindex meta tag** - `<meta name="robots" content="noindex, follow">`
   - Prevents Google from indexing the page
   - Uses "follow" to preserve internal link equity

2. **Low sitemap priority** - `<priority>0.3</priority>`
   - Deprioritizes crawling by search engines
   - Conserves crawl budget for quality content

3. **Monthly crawl frequency** - `<changefreq>monthly</changefreq>`
   - Reduces how often bots recrawl thin pages

## Test Suite

### Critical Tests (tests/critical/test_thin_content.py)

**Purpose:** Fast smoke tests that run on every commit

**Tests:**
- ✅ `test_thin_content_has_noindex_protection` - Samples 5 business license pages
- ✅ `test_sitemap_has_proper_priorities` - Verifies low priority for thin pages
- ✅ `test_noindex_uses_follow_directive` - Ensures link equity preservation
- ✅ `test_robots_txt_exists_with_sitemap` - Validates robots.txt

**Runtime:** ~2-5 seconds
**Runs:** Every commit, every merge

### Comprehensive SEO Tests (tests/seo/test_thin_content.py)

**Purpose:** Thorough validation for weekly SEO audits

**Tests:**
- 📊 `test_thin_content_detection_logic` - Validates detection algorithm
- 🔍 `test_thin_content_pages_have_noindex` - 90% coverage threshold
- 📉 `test_sitemap_deprioritizes_thin_content` - 70% threshold for business licenses
- ✅ `test_quality_pages_are_indexed_normally` - No false positives
- 🤖 `test_robots_txt_has_crawl_optimization` - Crawl-delay and disallow rules
- 🔗 `test_thin_content_noindex_follows` - 95% "follow" directive coverage

**Runtime:** ~30-60 seconds
**Runs:** Weekly, on-demand

## How Tests Work

### 1. Detection Logic Validation

```python
# Matches generator.py should_noindex_page() logic
total_chars = (desc_len + elig_len + how_len + mistakes_len)

is_thin = (
    (is_generic_business_license and total_chars < 800) or
    (total_chars < 800 and missing_mistakes and no_community) or
    (desc_len < 200)
)
```

### 2. File System Validation

Tests read generated HTML files in `output/` directory and verify:
- Presence of `<meta name="robots" content="noindex, follow">`
- Absence of noindex on quality content pages

### 3. Sitemap Validation

Tests parse `output/sitemap.xml` and verify:
- Priority values (0.3 for thin, 0.8 for quality)
- Change frequency (monthly for thin, weekly for quality)

## Running Tests

### Pre-Commit (Required)

```bash
./scripts/pre_commit_tests.sh
```

This runs the critical test suite, including thin content tests.

### Critical Tests Only

```bash
pytest tests/critical/test_thin_content.py -v
```

### Comprehensive SEO Tests

```bash
pytest tests/seo/test_thin_content.py -v
```

### All SEO Tests

```bash
pytest tests/seo/ -v
```

## Test Failures

### Common Failures

#### ❌ "Thin content pages are missing noindex tag"

**Cause:** The `should_noindex_page()` function in `generator.py` returned False for pages that should be noindexed.

**Fix:**
1. Check if content calculation logic changed in `generator.py`
2. Verify template has `{% if should_noindex %}` section
3. Regenerate site: `python3 generator.py`

#### ❌ "Business license pages have high priority in sitemap"

**Cause:** Sitemap generation is not using the thin content detection logic.

**Fix:**
1. Check `generate_sitemap()` function in `generator.py`
2. Verify it calls `should_noindex_page()` to determine priorities
3. Regenerate site: `python3 generator.py`

#### ❌ "Quality pages are incorrectly noindexed"

**Cause:** Detection logic is too aggressive (false positives).

**Fix:**
1. Review detection thresholds in `generator.py:should_noindex_page()`
2. Consider adjusting the 800-char threshold
3. Check if FAQs/feedback are being counted properly

### Debugging Tests

Enable verbose output:

```bash
pytest tests/critical/test_thin_content.py -v -s
```

See detailed statistics:

```bash
pytest tests/seo/test_thin_content.py::test_thin_content_detection_logic -v -s
```

## CI/CD Integration

### Automatic Execution

Tests run automatically on:

1. **Every commit** - via `scripts/pre_commit_tests.sh`
2. **Every push** - via `.github/workflows/ci-critical-tests.yml`
3. **Every PR** - via GitHub Actions
4. **Every merge to main** - via GitHub Actions
5. **Weekly schedule** - via `.github/workflows/weekly-seo-tests.yml`

### Failure Notifications

When tests fail in CI:
- ❌ Build marked as failed
- 🔔 Slack notification sent (if on main branch)
- 📊 Test report artifact uploaded
- 🚫 Deployment blocked

## Maintenance

### When to Update Tests

Update these tests when:

1. **Changing thin content definition** - Update thresholds in both test files
2. **Adding new content fields** - Update content calculation logic
3. **Changing noindex strategy** - Update validation logic
4. **Adding new page types** - Add coverage for new templates

### Test Coverage Goals

- **Critical tests:** 100% pass rate (blocking)
- **Thin content noindex:** ≥ 90% coverage
- **Business license deprioritization:** ≥ 70%
- **Quality content indexed:** ≥ 90%
- **Noindex "follow" usage:** ≥ 95%

## Related Documentation

- `generator.py:732-776` - `should_noindex_page()` function
- `templates/transaction_page.html:31-34` - Noindex template logic
- `generator.py:1635-1665` - Sitemap priority logic
- `claude.md` - Critical SEO requirements
- `docs/SEO_STRATEGY.md` - Overall SEO approach (if exists)

## Questions?

- **How do I know if a page should be noindexed?** Run the detection logic manually:
  ```python
  python3 -c "from generator import PermitIndexGenerator; g = PermitIndexGenerator(); print(g.should_noindex_page({'description': 'test', ...}))"
  ```

- **Can I disable these tests?** No. They are critical for SEO health. If you need to bypass temporarily (e.g., debugging), use `pytest -k "not thin_content"`.

- **Why 800 characters?** This threshold balances quality vs. quantity. Pages under 800 chars typically lack sufficient unique value for users.

- **What if I want to improve a thin page?** Add more content to the permit's JSON data fields (description, eligibility, how_to_description, common_mistakes). Once above 800 chars, it will automatically be indexed.
