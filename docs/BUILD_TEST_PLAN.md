# Build & Test Plan for News123

This document outlines the automated testing strategy for the News123 static site generator.

## Pre-Build Checks

### 1. Code Quality
```bash
# Check Python syntax
python3 -m py_compile generator.py

# Lint templates (optional)
# pip install jinjalint
# jinjalint templates/
```

## Build Process

### 1. Generate Site
```bash
python3 generator.py
```

**Expected output:**
- ✅ 0 errors
- ✅ All pages generated successfully
- ✅ Sitemap.xml created
- ✅ Robots.txt created

## Post-Build Tests

### 1. Link Validation (Local Build)
**Purpose:** Ensure all internal links point to existing files

```bash
python3 validate_links.py --local
```

**What it checks:**
- ✅ All `<a href="">` links in all HTML files
- ✅ Links in navigation menus
- ✅ Breadcrumb links
- ✅ "Related permits" links
- ✅ Homepage "Popular Permits" links
- ✅ Jurisdiction hub links

**Success criteria:**
- All permit-to-permit links valid
- Hub page links valid
- Homepage links valid

**Expected failures (acceptable):**
- `/about`, `/contact`, `/faq`, `/privacy`, `/terms` - Placeholder pages
- `/states`, `/agencies` - Not yet implemented
- Related permits that don't exist in sample data

### 2. SEO Validation (Local Build)
**Purpose:** Verify SEO best practices are implemented

```bash
# Check meta tags
grep -r "meta name=\"description\"" output/ | wc -l
# Should match number of HTML pages

# Check canonical tags
grep -r "rel=\"canonical\"" output/ | wc -l
# Should match number of HTML pages

# Check H1 tags (should be exactly 1 per page)
for file in output/**/*.html; do
    h1_count=$(grep -o "<h1" "$file" | wc -l)
    if [ $h1_count -ne 1 ]; then
        echo "❌ $file has $h1_count H1 tags (should be 1)"
    fi
done

# Check structured data
grep -r "application/ld+json" output/ | wc -l
# Should have multiple schemas per page
```

### 3. Content Quality Checks
**Purpose:** Ensure content meets minimum standards

```bash
# Check word count for main permit pages
for file in output/california/*/index.html; do
    words=$(cat "$file" | wc -w)
    if [ $words -lt 1000 ]; then
        echo "⚠️  $file has only $words words (target: 1000+)"
    fi
done

# Check for required sections
required_sections=(
    "Frequently Asked Questions"
    "What People Are Saying"
    "Tips from the Community"
    "Contact Information"
)

for section in "${required_sections[@]}"; do
    count=$(grep -r "$section" output/california/*/index.html | wc -l)
    echo "   $section: $count pages"
done
```

### 4. Sitemap Validation
**Purpose:** Ensure sitemap is complete and valid

```bash
# Check sitemap exists
test -f output/sitemap.xml && echo "✅ Sitemap exists" || echo "❌ Sitemap missing"

# Validate XML structure
xmllint --noout output/sitemap.xml 2>&1
# Should output nothing if valid

# Check all pages are in sitemap
page_count=$(find output -name "index.html" | wc -l)
sitemap_count=$(grep -o "<loc>" output/sitemap.xml | wc -l)
echo "Pages generated: $page_count"
echo "URLs in sitemap: $sitemap_count"
```

### 5. Structured Data Validation
**Purpose:** Ensure JSON-LD schemas are valid

```bash
# Extract and validate JSON-LD schemas
for file in output/california/*/index.html; do
    echo "Checking: $file"
    # Extract JSON-LD blocks and validate
    grep -Pzo '(?s)<script type="application/ld\+json">.*?</script>' "$file" | \
        python3 -c "import sys, json; [json.loads(block.split('>',1)[1].rsplit('<',1)[0]) for block in sys.stdin.read().split('<script type=\"application/ld+json\">')[1:]]"
done
```

## Pre-Deployment Tests (Production)

### 1. Production Link Validation
**Purpose:** Verify all links work on deployed site

```bash
python3 validate_links.py --production
```

**What it checks:**
- ✅ All links on homepage
- ✅ All links on hub pages
- ✅ All links on permit pages
- ✅ Returns HTTP 200 for all internal links

**Success criteria:**
- 0 broken permit/hub links
- All critical navigation working

### 2. Full SEO Validation (Production)
**Purpose:** Comprehensive SEO check on live site

```bash
python3 validate_seo.py
```

**What it checks:**
- ✅ URL structure (hierarchical, no double slashes)
- ✅ Canonical tags (correct and matching)
- ✅ Meta descriptions (optimal length)
- ✅ H1 tags (exactly one per page)
- ✅ Above-the-fold summary
- ✅ FAQ section with FAQPage schema
- ✅ Community feedback section
- ✅ User tips section
- ✅ Common mistakes section
- ✅ Agency contact information
- ✅ WTP widget functionality
- ✅ Hub pages with statistics
- ✅ Breadcrumb navigation
- ✅ Content depth (word count)
- ✅ Sitemap accessibility
- ✅ Mobile responsiveness

**Success criteria:**
- ✅ 17/18 critical tests pass
- ⚠️  0-1 warnings acceptable

## Continuous Integration (CI/CD)

### GitHub Actions Workflow (`.github/workflows/test.yml`)

```yaml
name: Build and Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Generate site
      run: |
        python3 generator.py

    - name: Validate local links
      run: |
        python3 validate_links.py --local

    - name: Check word count
      run: |
        for file in output/california/*/index.html; do
          words=$(cat "$file" | wc -w)
          if [ $words -lt 1000 ]; then
            echo "⚠️  $file has only $words words"
          fi
        done

    - name: Install Playwright (for production tests)
      if: github.ref == 'refs/heads/main'
      run: |
        pip install playwright
        playwright install chromium

    - name: Validate production (main branch only)
      if: github.ref == 'refs/heads/main'
      run: |
        python3 validate_links.py --production
        python3 validate_seo.py

    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: site-output
        path: output/
```

## Cloudflare Pages Build Settings

```bash
# Build command:
python3 generator.py && python3 validate_links.py --local

# Build output directory:
output

# Environment variables:
PYTHON_VERSION=3.11
```

## Manual Testing Checklist

Before each release, manually verify:

- [ ] Homepage loads and displays statistics
- [ ] "Browse by State" links work
- [ ] "Popular Permits" links work
- [ ] Hub page shows all permits
- [ ] Permit page shows all sections
- [ ] FAQ accordion works (if implemented)
- [ ] WTP slider is interactive
- [ ] Phone/email links are clickable
- [ ] Breadcrumbs navigate correctly
- [ ] Related permits links work
- [ ] Mobile view is responsive
- [ ] Search functionality (when implemented)

## Performance Testing (Optional)

```bash
# Using Lighthouse CI
npm install -g @lhci/cli
lhci autorun --collect.url=https://news123.info/california/food-truck-operating-permit/

# Target scores:
# Performance: 90+
# Accessibility: 95+
# Best Practices: 95+
# SEO: 100
```

## Error Handling

### If build fails:
1. Check CSV file syntax
2. Verify all required columns present
3. Check for malformed JSON in JSON fields
4. Review generator.py error messages

### If link validation fails:
1. Check template href attributes
2. Verify URL generation in generator.py
3. Ensure file paths match URL structure
4. Review related_pages field in CSV

### If SEO validation fails:
1. Check meta tag templates
2. Verify structured data JSON-LD
3. Confirm canonical URLs match file structure
4. Review word count and content sections

## Deployment Checklist

- [ ] All tests pass locally
- [ ] Changes committed to git
- [ ] Version bumped (if applicable)
- [ ] Pushed to GitHub
- [ ] Cloudflare build succeeds
- [ ] Production link validation passes
- [ ] Production SEO validation passes
- [ ] Spot check 3-5 random pages
- [ ] Submit updated sitemap to Google Search Console

## Monitoring (Post-Deployment)

- [ ] Check Google Search Console for errors
- [ ] Monitor Cloudflare analytics
- [ ] Check for 404s in logs
- [ ] Verify FAQ rich snippets appearing (1-2 weeks)
- [ ] Monitor page rankings
- [ ] Check Core Web Vitals

---

**Last Updated:** 2024-11-13
**Version:** 1.0
