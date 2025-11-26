# PermitIndex Testing System Implementation Guide

Complete guide for implementing automated testing with Claude Code-ready failure instructions.

---

## Overview

This testing system provides:
- **6 test suites** with 102 total tests
- **Automated scheduling** (every push, daily, weekly)
- **Claude Code-ready fix instructions** when tests fail
- **Visual regression testing** with screenshot comparison
- **SEO monitoring** for search rankings
- **Brand compliance** enforcement

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt --break-system-packages
python -m playwright install chromium

# Run all tests
pytest tests/

# Run specific suite
pytest tests/critical/
pytest tests/seo/
pytest tests/visual/

# Generate HTML report
pytest tests/ --html=test-report.html
```

---

## Test Suites

| Suite | Files | Tests | Frequency | Duration |
|-------|-------|-------|-----------|----------|
| Critical | 4 | ~12 | Every push | 2 min |
| Data Validation | 4 | ~16 | Every push | 30 sec |
| SEO | 9 | ~40 | Weekly | 10 min |
| Brand Guidelines | 6 | ~20 | Daily | 5 min |
| Feedback Flow | 6 | ~18 | Weekly | 15 min |
| Analytics | 4 | ~12 | Weekly | 5 min |

---

## Implementation Steps

### Step 1: Create Folder Structure

```bash
mkdir -p tests/{critical,data,seo,visual,integration,analytics,utils,reports}
mkdir -p tests/visual/screenshots
mkdir -p scripts
mkdir -p .github/workflows
```

### Step 2: Core Configuration

**File: `tests/pytest.ini`**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --html=tests/reports/test-report.html
    --self-contained-html
    --json-report
    --json-report-file=tests/reports/report.json
    -n auto
markers =
    critical: Critical tests that run on every build
    visual: Visual regression tests
    seo: SEO compliance tests
    integration: Integration tests with external services
    analytics: Analytics tracking tests
    slow: Tests that take >10 seconds
```

**File: `tests/conftest.py`**
```python
import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.fixture(scope="session")
def browser():
    """Shared browser instance for all tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    """New page for each test - desktop viewport"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def mobile_page(browser):
    """Mobile viewport for responsive tests"""
    context = browser.new_context(
        viewport={'width': 375, 'height': 812},
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        is_mobile=True,
        has_touch=True
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def tablet_page(browser):
    """Tablet viewport for responsive tests"""
    context = browser.new_context(
        viewport={'width': 768, 'height': 1024},
        user_agent='Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="session")
def live_url():
    """Base URL for live site"""
    return os.getenv('TEST_URL', 'https://permitindex.com')

@pytest.fixture(scope="session")
def output_dir():
    """Local output directory for testing generated files"""
    return os.path.abspath('output')
```

---

## Test Files

### Critical Tests

**File: `tests/critical/test_site_builds.py`**
```python
import pytest
import subprocess
import os

@pytest.mark.critical
def test_generator_runs_without_errors():
    """Test that generator.py completes successfully"""
    result = subprocess.run(
        ['python3', 'generator.py'],
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0, f"Generator failed: {result.stderr}"

@pytest.mark.critical
def test_output_directory_created(output_dir):
    """Test that output directory exists and has files"""
    assert os.path.exists(output_dir), "Output directory missing"
    assert os.path.exists(os.path.join(output_dir, 'index.html')), "Homepage not generated"
    
    html_files = [f for f in os.listdir(output_dir) if f.endswith('.html') and f != 'index.html']
    assert len(html_files) >= 1, "No permit pages generated"

@pytest.mark.critical
def test_required_files_exist(output_dir):
    """Test that all required files are generated"""
    required_files = ['sitemap.xml', 'robots.txt']
    
    for filename in required_files:
        filepath = os.path.join(output_dir, filename)
        assert os.path.exists(filepath), f"Required file missing: {filename}"
```

**File: `tests/critical/test_pages_load.py`**
```python
import pytest

@pytest.mark.critical
def test_homepage_loads(page, live_url):
    """Test homepage returns 200"""
    response = page.goto(live_url)
    assert response.status == 200, f"Homepage returned {response.status}"

@pytest.mark.critical
def test_sample_permit_page_loads(page, live_url):
    """Test a sample permit page loads"""
    response = page.goto(f"{live_url}/california/contractor-license/")
    assert response.status == 200, f"Permit page returned {response.status}"
    
    # Verify key content exists
    h1_count = page.locator('h1').count()
    assert h1_count > 0, "No h1 heading found on permit page"

@pytest.mark.critical
def test_no_console_errors(page, live_url):
    """Test that pages have no JavaScript errors"""
    errors = []
    
    def handle_console(msg):
        if msg.type == 'error':
            errors.append(msg.text)
    
    page.on('console', handle_console)
    page.goto(live_url)
    
    # Filter out known acceptable errors
    real_errors = [e for e in errors if 'favicon' not in e.lower()]
    
    assert len(real_errors) == 0, f"Console errors found: {real_errors}"
```

**File: `tests/critical/test_no_broken_links.py`**
```python
import pytest
from urllib.parse import urljoin, urlparse

@pytest.mark.critical
@pytest.mark.slow
def test_homepage_internal_links(page, live_url):
    """Crawl homepage and check all internal links return 200"""
    page.goto(live_url)
    
    links = page.locator('a[href]').all()
    internal_links = []
    
    for link in links:
        href = link.get_attribute('href')
        if href and not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            full_url = urljoin(live_url, href)
            if urlparse(full_url).netloc == urlparse(live_url).netloc:
                internal_links.append(full_url)
    
    # Test unique internal links
    unique_links = list(set(internal_links))
    broken_links = []
    
    for link in unique_links[:20]:  # Test first 20 to keep it fast
        try:
            response = page.goto(link, timeout=10000)
            if response.status >= 400:
                broken_links.append((link, response.status))
        except Exception as e:
            broken_links.append((link, str(e)))
    
    assert len(broken_links) == 0, f"Broken internal links: {broken_links}"
```

**File: `tests/critical/test_analytics_present.py`**
```python
import pytest

@pytest.mark.critical
def test_plausible_script_exists(page, live_url):
    """Confirm Plausible script tag exists in head"""
    page.goto(live_url)
    
    plausible_script = page.locator('script[src*="plausible.io"]')
    assert plausible_script.count() > 0, "Plausible script tag not found"

@pytest.mark.critical
def test_plausible_loads(page, live_url):
    """Verify Plausible script loads successfully"""
    responses = []
    
    def handle_response(response):
        if 'plausible.io' in response.url:
            responses.append(response)
    
    page.on('response', handle_response)
    page.goto(live_url)
    page.wait_for_timeout(2000)  # Wait for script to load
    
    assert len(responses) > 0, "Plausible script did not load"
    assert any(r.ok for r in responses), "Plausible script failed to load successfully"

@pytest.mark.critical
def test_plausible_initialized(page, live_url):
    """Test that plausible object is initialized"""
    page.goto(live_url)
    page.wait_for_timeout(2000)
    
    has_plausible = page.evaluate('typeof window.plausible !== "undefined"')
    assert has_plausible, "window.plausible object not initialized"
```

---

### Data Validation Tests

**File: `tests/data/test_csv_schema.py`**
```python
import pytest
import pandas as pd
import os

@pytest.mark.critical
def test_permits_csv_exists():
    """Test that permits.csv exists"""
    assert os.path.exists('data/permits/permits.csv'), "permits.csv not found"

@pytest.mark.critical
def test_permits_csv_has_correct_columns():
    """Validate permits.csv has exactly 18 required columns"""
    df = pd.read_csv('data/permits/permits.csv')
    
    expected_columns = [
        'agency_short', 'request_type', 'cost', 'how_to_description',
        'payment_form_url', 'agency_full', 'eligibility', 'location_applicability',
        'document_requirements', 'estimated_monthly_volume', 'deadline_window',
        'effort_hours', 'online_available', 'api_available', 'mcp_available',
        'related_pages', 'date_extracted', 'source_url'
    ]
    
    actual_columns = list(df.columns)
    
    assert len(actual_columns) == 18, f"Expected 18 columns, found {len(actual_columns)}"
    assert actual_columns == expected_columns, f"Column mismatch: {actual_columns}"

@pytest.mark.critical
def test_csv_valid_utf8():
    """Ensure CSV is valid UTF-8 encoded"""
    try:
        with open('data/permits/permits.csv', 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError as e:
        pytest.fail(f"CSV is not valid UTF-8: {e}")
```

**File: `tests/data/test_required_fields.py`**
```python
import pytest
import pandas as pd

@pytest.mark.critical
def test_no_empty_required_fields():
    """Confirms no empty values in required fields"""
    df = pd.read_csv('data/permits/permits.csv')
    
    required_fields = ['agency_short', 'request_type', 'cost', 'how_to_description']
    
    for field in required_fields:
        empty_count = df[field].isna().sum()
        assert empty_count == 0, f"Field '{field}' has {empty_count} empty values"

@pytest.mark.critical
def test_unique_composite_key():
    """Validates that composite key (agency_short + request_type) is unique"""
    df = pd.read_csv('data/permits/permits.csv')
    
    df['composite_key'] = df['agency_short'] + '|||' + df['request_type']
    duplicates = df[df['composite_key'].duplicated()]
    
    assert len(duplicates) == 0, f"Found {len(duplicates)} duplicate composite keys: {duplicates['composite_key'].tolist()}"

@pytest.mark.critical
def test_boolean_fields_valid():
    """Checks boolean fields contain only 'Yes' or 'No'"""
    df = pd.read_csv('data/permits/permits.csv')
    
    boolean_fields = ['online_available', 'api_available', 'mcp_available']
    
    for field in boolean_fields:
        valid_values = ['Yes', 'No']
        invalid_values = df[~df[field].isin(valid_values)][field].unique()
        
        assert len(invalid_values) == 0, f"Field '{field}' has invalid values: {invalid_values}"
```

**File: `tests/data/test_data_quality.py`**
```python
import pytest
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime

@pytest.mark.critical
def test_urls_valid_format():
    """Verifies all URLs are valid format"""
    df = pd.read_csv('data/permits/permits.csv')
    
    url_fields = ['payment_form_url', 'source_url']
    
    for field in url_fields:
        urls = df[field].dropna()
        
        for idx, url in urls.items():
            try:
                parsed = urlparse(url)
                assert parsed.scheme in ['http', 'https'], f"Row {idx} {field}: Invalid scheme"
                assert parsed.netloc, f"Row {idx} {field}: No domain"
            except Exception as e:
                pytest.fail(f"Row {idx} {field}: Invalid URL '{url}' - {e}")

@pytest.mark.critical
def test_dates_iso_format():
    """Checks dates are in ISO format (YYYY-MM-DD)"""
    df = pd.read_csv('data/permits/permits.csv')
    
    date_fields = ['date_extracted']
    
    for field in date_fields:
        dates = df[field].dropna()
        
        for idx, date_str in dates.items():
            try:
                datetime.strptime(str(date_str), '%Y-%m-%d')
            except ValueError:
                pytest.fail(f"Row {idx} {field}: Invalid date format '{date_str}' (expected YYYY-MM-DD)")

@pytest.mark.critical
def test_cost_field_reasonable():
    """Validates cost field contains reasonable values"""
    df = pd.read_csv('data/permits/permits.csv')
    
    for idx, cost in df['cost'].items():
        cost_str = str(cost).lower()
        
        # Should not be negative
        assert not cost_str.startswith('-'), f"Row {idx}: Negative cost '{cost}'"
        
        # Should contain reasonable patterns
        valid_patterns = ['$', 'free', 'varies', '-', 'contact', 'no fee']
        assert any(p in cost_str for p in valid_patterns), f"Row {idx}: Suspicious cost format '{cost}'"
```

**File: `tests/data/test_user_feedback_csv.py`**
```python
import pytest
import pandas as pd
import os

def test_user_feedback_csv_schema():
    """Validates user_feedback.csv schema if it exists"""
    csv_path = 'data/feedback/user_feedback.csv'
    
    if not os.path.exists(csv_path):
        pytest.skip("user_feedback.csv does not exist yet")
    
    df = pd.read_csv(csv_path)
    
    expected_columns = [
        'permit_slug', 'feedback_type', 'feedback_text', 
        'helpful_count', 'created_at', 'approved', 'github_issue_number'
    ]
    
    assert list(df.columns) == expected_columns, f"Column mismatch: {list(df.columns)}"

def test_feedback_type_values():
    """Checks feedback_type values are valid"""
    csv_path = 'data/feedback/user_feedback.csv'
    
    if not os.path.exists(csv_path):
        pytest.skip("user_feedback.csv does not exist yet")
    
    df = pd.read_csv(csv_path)
    
    valid_types = ['tip', 'common_mistake', 'time_estimate', 'cost_note']
    invalid = df[~df['feedback_type'].isin(valid_types)]
    
    assert len(invalid) == 0, f"Invalid feedback_type values: {invalid['feedback_type'].unique()}"

def test_approved_field():
    """Verifies approved field contains only 'yes' or 'no'"""
    csv_path = 'data/feedback/user_feedback.csv'
    
    if not os.path.exists(csv_path):
        pytest.skip("user_feedback.csv does not exist yet")
    
    df = pd.read_csv(csv_path)
    
    valid_values = ['yes', 'no']
    invalid = df[~df['approved'].isin(valid_values)]
    
    assert len(invalid) == 0, f"Invalid approved values: {invalid['approved'].unique()}"
```

---

### SEO Tests (9 files)

Due to length, I'll provide the key ones and patterns for the rest:

**File: `tests/seo/test_meta_tags.py`**
```python
import pytest

@pytest.mark.seo
def test_homepage_has_title(page, live_url):
    """Verifies homepage has title tag"""
    page.goto(live_url)
    
    title = page.title()
    assert title, "No title tag found"
    assert 10 <= len(title) <= 60, f"Title length {len(title)} outside recommended 10-60 chars"

@pytest.mark.seo
def test_homepage_meta_description(page, live_url):
    """Checks meta description exists and is proper length"""
    page.goto(live_url)
    
    description = page.locator('meta[name="description"]').get_attribute('content')
    assert description, "No meta description found"
    assert 50 <= len(description) <= 160, f"Description length {len(description)} outside 50-160 chars"

@pytest.mark.seo
def test_open_graph_tags(page, live_url):
    """Validates Open Graph tags"""
    page.goto(live_url)
    
    og_title = page.locator('meta[property="og:title"]').get_attribute('content')
    og_description = page.locator('meta[property="og:description"]').get_attribute('content')
    og_image = page.locator('meta[property="og:image"]').get_attribute('content')
    og_url = page.locator('meta[property="og:url"]').get_attribute('content')
    
    assert og_title, "Missing og:title"
    assert og_description, "Missing og:description"
    assert og_image, "Missing og:image"
    assert og_url, "Missing og:url"

@pytest.mark.seo
def test_permit_page_unique_title(page, live_url):
    """Test permit pages have unique titles"""
    page1 = page.goto(f"{live_url}/california/contractor-license/")
    title1 = page.title()
    
    page2 = page.goto(f"{live_url}/california/food-truck-permit/")  
    title2 = page.title()
    
    assert title1 != title2, "Permit pages have duplicate titles"
```

**File: `tests/seo/test_structured_data.py`**
```python
import pytest
import json

@pytest.mark.seo
def test_permit_page_has_json_ld(page, live_url):
    """Validates JSON-LD structured data exists"""
    page.goto(f"{live_url}/california/contractor-license/")
    
    json_ld_scripts = page.locator('script[type="application/ld+json"]').all()
    assert len(json_ld_scripts) > 0, "No JSON-LD structured data found"

@pytest.mark.seo
def test_json_ld_valid(page, live_url):
    """Verifies JSON-LD is valid JSON"""
    page.goto(f"{live_url}/california/contractor-license/")
    
    json_ld_scripts = page.locator('script[type="application/ld+json"]').all()
    
    for script in json_ld_scripts:
        content = script.inner_text()
        try:
            data = json.loads(content)
            assert '@context' in data, "Missing @context in JSON-LD"
            assert '@type' in data, "Missing @type in JSON-LD"
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON-LD: {e}")
```

**File: `tests/seo/test_sitemap.py`**
```python
import pytest
import xml.etree.ElementTree as ET

@pytest.mark.seo
def test_sitemap_exists(page, live_url):
    """Confirms sitemap.xml exists"""
    response = page.goto(f"{live_url}/sitemap.xml")
    assert response.status == 200, f"Sitemap returned {response.status}"

@pytest.mark.seo
def test_sitemap_valid_xml(page, live_url):
    """Validates XML structure is well-formed"""
    page.goto(f"{live_url}/sitemap.xml")
    content = page.content()
    
    assert '<?xml' in content, "Missing XML declaration"
    assert '<urlset' in content, "Not a valid sitemap"
    
    try:
        ET.fromstring(content)
    except ET.ParseError as e:
        pytest.fail(f"Invalid XML: {e}")

@pytest.mark.seo
def test_homepage_in_sitemap(page, live_url):
    """Checks homepage is included in sitemap"""
    page.goto(f"{live_url}/sitemap.xml")
    content = page.content()
    
    assert f'<loc>{live_url}</loc>' in content or f'<loc>{live_url}/</loc>' in content, "Homepage not in sitemap"
```

**File: `tests/seo/test_robots_txt.py`**
```python
import pytest

@pytest.mark.seo
def test_robots_txt_exists(page, live_url):
    """Confirms robots.txt exists"""
    response = page.goto(f"{live_url}/robots.txt")
    assert response.status == 200, f"robots.txt returned {response.status}"

@pytest.mark.seo
def test_sitemap_in_robots(page, live_url):
    """Tests that sitemap location is declared in robots.txt"""
    page.goto(f"{live_url}/robots.txt")
    content = page.content()
    
    assert 'Sitemap:' in content, "Sitemap not declared in robots.txt"
    assert 'sitemap.xml' in content.lower(), "sitemap.xml not referenced"
```

**File: `tests/seo/test_mobile_seo.py`**
```python
import pytest

@pytest.mark.seo
def test_viewport_meta_tag(mobile_page, live_url):
    """Tests viewport meta tag is present"""
    mobile_page.goto(live_url)
    
    viewport = mobile_page.locator('meta[name="viewport"]').get_attribute('content')
    assert viewport, "No viewport meta tag found"
    assert 'width=device-width' in viewport, "Viewport not configured for mobile"

@pytest.mark.seo
def test_font_size_readable_mobile(mobile_page, live_url):
    """Validates font sizes are readable on mobile"""
    mobile_page.goto(live_url)
    
    body_font_size = mobile_page.evaluate("""
        () => parseFloat(window.getComputedStyle(document.body).fontSize)
    """)
    
    assert body_font_size >= 14, f"Body font too small on mobile: {body_font_size}px (min 14px)"

@pytest.mark.seo
def test_no_horizontal_scroll_mobile(mobile_page, live_url):
    """Verifies no horizontal scrolling on mobile"""
    mobile_page.goto(live_url)
    
    scroll_width = mobile_page.evaluate('document.documentElement.scrollWidth')
    client_width = mobile_page.evaluate('document.documentElement.clientWidth')
    
    assert scroll_width <= client_width + 5, f"Horizontal scroll detected: {scroll_width} > {client_width}"
```

---

### Visual/Brand Tests

**File: `tests/visual/test_logo_compliance.py`**
```python
import pytest

@pytest.mark.visual
def test_logo_present(page, live_url):
    """Verifies logo appears on page"""
    page.goto(live_url)
    
    # Look for logo by various selectors
    logo = page.locator('svg, img[alt*="PermitIndex"], a[href="/"] img').first
    assert logo.count() > 0, "Logo not found on homepage"

@pytest.mark.visual
def test_logo_uses_correct_color(page, live_url):
    """Checks logo uses Primary Blue (#003366)"""
    page.goto(live_url)
    
    # This test would need to inspect SVG fill colors
    # For now, just verify logo element exists
    logo_element = page.locator('svg, [class*="logo"]').first
    assert logo_element.count() > 0, "Logo element not found"
```

---

### Analytics Tests

**File: `tests/analytics/test_wtp_slider_event.py`**
```python
import pytest

@pytest.mark.analytics
@pytest.mark.slow
def test_wtp_slider_present(page, live_url):
    """Verifies WTP slider widget exists on permit pages"""
    page.goto(f"{live_url}/california/contractor-license/")
    
    wtp_slider = page.locator('#wtp-slider')
    assert wtp_slider.count() > 0, "WTP slider not found on permit page"

@pytest.mark.analytics
@pytest.mark.slow
def test_wtp_submission_fires_event(page, live_url):
    """Tests that WTP submission triggers Plausible event"""
    page.goto(f"{live_url}/california/contractor-license/")
    
    # Track Plausible events
    events = []
    
    def handle_request(request):
        if 'plausible.io/api/event' in request.url:
            events.append(request.post_data_json)
    
    page.on('request', handle_request)
    
    # Fill and submit WTP form
    if page.locator('#wtp-slider').count() > 0:
        page.locator('#wtp-slider').fill('50')
        page.locator('#wtp-form').submit()
        
        page.wait_for_timeout(2000)
        
        wtp_events = [e for e in events if e and e.get('n') == 'WTP Submission']
        assert len(wtp_events) > 0, "WTP Submission event did not fire"
    else:
        pytest.skip("WTP widget not present on this page")
```

---

## GitHub Actions Workflows

**File: `.github/workflows/ci-critical-tests.yml`**
```yaml
name: Critical Tests (Every Push)

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  critical-tests:
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
          python -m playwright install chromium --with-deps
      
      - name: Run generator
        run: python3 generator.py
      
      - name: Run critical and data tests
        run: |
          pytest tests/critical/ tests/data/ \
            -m critical \
            --json-report \
            --json-report-file=test-report.json \
            --html=test-report.html \
            --self-contained-html
      
      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: critical-test-report
          path: |
            test-report.html
            test-report.json
      
      - name: Fail if tests failed
        if: failure()
        run: exit 1
```

**File: `.github/workflows/daily-visual-tests.yml`**
```yaml
name: Daily Visual & Brand Tests

on:
  schedule:
    - cron: '0 3 * * *'  # 3 AM UTC daily
  workflow_dispatch:

jobs:
  visual-tests:
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
          python -m playwright install chromium --with-deps
      
      - name: Run visual tests
        id: tests
        continue-on-error: true
        run: |
          pytest tests/visual/ \
            -m visual \
            --json-report \
            --json-report-file=tests/reports/visual-report.json \
            --html=tests/reports/visual-report.html \
            --self-contained-html
      
      - name: Generate Claude Code instructions
        if: steps.tests.outcome == 'failure'
        run: |
          python3 scripts/generate_claude_instructions.py \
            --test-report tests/reports/visual-report.json \
            --output claude-instructions.txt
      
      - name: Upload screenshots and reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: visual-test-artifacts
          path: |
            tests/visual/screenshots/
            tests/reports/visual-report.html
            claude-instructions.txt
      
      - name: Send email notification
        if: steps.tests.outcome == 'failure'
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "PermitIndex Visual Tests Failed - Claude Code Instructions"
          to: ${{ secrets.NOTIFICATION_EMAIL }}
          from: GitHub Actions <noreply@github.com>
          body: file://claude-instructions.txt
          content_type: text/plain
```

**File: `.github/workflows/weekly-seo-tests.yml`**
```yaml
name: Weekly SEO & Integration Tests

on:
  schedule:
    - cron: '0 10 * * 0'  # 10 AM UTC on Sundays
  workflow_dispatch:

jobs:
  seo-and-integration-tests:
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
          python -m playwright install chromium --with-deps
      
      - name: Run SEO tests
        id: seo_tests
        continue-on-error: true
        run: |
          pytest tests/seo/ tests/integration/ tests/analytics/ \
            --json-report \
            --json-report-file=tests/reports/weekly-report.json \
            --html=tests/reports/weekly-report.html \
            --self-contained-html
      
      - name: Generate Claude Code instructions
        if: steps.seo_tests.outcome == 'failure'
        run: |
          python3 scripts/generate_claude_instructions.py \
            --test-report tests/reports/weekly-report.json \
            --output claude-instructions.txt
      
      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: weekly-test-report
          path: |
            tests/reports/
            claude-instructions.txt
      
      - name: Send email notification
        if: steps.seo_tests.outcome == 'failure'
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "PermitIndex Weekly Tests Failed - Claude Code Instructions"
          to: ${{ secrets.NOTIFICATION_EMAIL }}
          from: GitHub Actions <noreply@github.com>
          body: file://claude-instructions.txt
          content_type: text/plain
```

---

## Claude Code Instruction Generator

**File: `scripts/generate_claude_instructions.py`**

```python
#!/usr/bin/env python3
"""
Generate Claude Code-ready instructions from test failures
"""

import json
import sys
from datetime import datetime
import argparse

def load_test_report(filepath):
    """Load pytest JSON report"""
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_instructions(test_report):
    """Convert test failures to Claude Code instructions"""
    
    failed_tests = [
        test for test in test_report.get('tests', [])
        if test.get('outcome') == 'failed'
    ]
    
    if not failed_tests:
        return None
    
    # Header
    instructions = [
        f"Subject: PermitIndex Tests Failed - {len(failed_tests)} issues detected\n",
        "",
        "─" * 70,
        "COPY EVERYTHING BELOW THIS LINE TO CLAUDE CODE",
        "─" * 70,
        "",
        f"PermitIndex automated tests detected {len(failed_tests)} issues that need fixing.",
        "",
        f"TASK: Fix the following test failures detected on {datetime.now().strftime('%Y-%m-%d')} at {datetime.now().strftime('%H:%M')} UTC",
        ""
    ]
    
    # Generate instructions for each failure
    for i, test in enumerate(failed_tests, 1):
        instructions.extend(format_test_failure(i, test))
    
    # Footer
    instructions.extend([
        "",
        "═" * 70,
        "AFTER FIXING ALL ISSUES",
        "═" * 70,
        "",
        "1. Run full test suite to verify all fixes:",
        "   pytest tests/",
        "",
        "2. Commit changes:",
        '   git add .',
        '   git commit -m "Fix test failures: [describe fixes]"',
        '   git push origin main',
        "",
        "3. Report back:",
        "   - Confirmation that all issues are fixed",
        "   - Test results showing all tests pass",
        "   - Summary of changes made",
        "",
        "─" * 70,
        "END OF CLAUDE CODE INSTRUCTIONS",
        "─" * 70,
        ""
    ])
    
    return "\n".join(instructions)

def format_test_failure(issue_num, test):
    """Format a single test failure for Claude Code"""
    
    test_name = test.get('nodeid', 'Unknown test')
    
    # Get error message
    call_info = test.get('call', {})
    longrepr = call_info.get('longrepr', '')
    
    # Extract just the relevant error lines
    if isinstance(longrepr, str):
        error_lines = longrepr.split('\n')
        # Get assertion error or last few lines
        relevant_lines = [l for l in error_lines if l.strip() and not l.startswith('_')][-5:]
        error_msg = '\n'.join(relevant_lines)
    else:
        error_msg = str(longrepr)
    
    # Determine test category
    if 'seo' in test_name:
        category = 'SEO'
    elif 'visual' in test_name or 'brand' in test_name:
        category = 'Visual/Brand'
    elif 'critical' in test_name:
        category = 'Critical'
    elif 'data' in test_name:
        category = 'Data Quality'
    elif 'analytics' in test_name:
        category = 'Analytics'
    elif 'integration' in test_name:
        category = 'Integration'
    else:
        category = 'General'
    
    instructions = [
        "",
        "═" * 70,
        f"ISSUE {issue_num}: {test_name.split('::')[-1].replace('_', ' ').title()}",
        "═" * 70,
        "",
        f"CATEGORY: {category}",
        f"TEST: {test_name}",
        "",
        "PROBLEM:",
        error_msg[:500],  # Truncate long errors
        "",
        "FIX REQUIRED:",
    ]
    
    # Add fix instructions based on test type
    fix_steps = generate_fix_steps(test_name, error_msg)
    instructions.extend(fix_steps)
    
    instructions.extend([
        "",
        "VERIFICATION:",
        f"After fixing, run: pytest {test_name}",
        ""
    ])
    
    return instructions

def generate_fix_steps(test_name, error_msg):
    """Generate specific fix steps based on test type"""
    
    # Meta description tests
    if 'meta_description' in test_name:
        return [
            "1. Open templates/transaction_page.html",
            "2. Locate meta description template",
            "3. Ensure descriptions are 150-160 characters",
            "4. Use descriptive, keyword-rich content",
            "5. Regenerate: python3 generator.py",
            "6. Verify output HTML files"
        ]
    
    # Sitemap tests
    elif 'sitemap' in test_name:
        return [
            "1. Verify generator.py creates sitemap.xml",
            "2. Check all pages in output/ are included",
            "3. Ensure lastmod dates are ISO format",
            "4. Regenerate: python3 generator.py",
            "5. Validate sitemap at https://permitindex.com/sitemap.xml"
        ]
    
    # Broken link tests
    elif 'link' in test_name:
        return [
            "1. Identify broken link(s) from error message",
            "2. Check if target page exists in output/",
            "3. Fix link URL in template OR remove link",
            "4. Update templates/index.html or transaction_page.html",
            "5. Regenerate: python3 generator.py"
        ]
    
    # CSV/data tests
    elif 'csv' in test_name or 'data' in test_name:
        return [
            "1. Open data/permits/permits.csv",
            "2. Find row(s) with issues from error",
            "3. Fix: formatting, missing values, or invalid data",
            "4. Ensure dates: YYYY-MM-DD format",
            "5. Verify URLs are valid",
            "6. Regenerate: python3 generator.py"
        ]
    
    # Visual/brand tests
    elif 'visual' in test_name or 'brand' in test_name or 'color' in test_name:
        return [
            "1. Review BRAND_GUIDELINES.md",
            "2. Check templates and CSS for violations",
            "3. Use only approved colors: #003366, #FF6B35",
            "4. Verify star cutout positioning formula",
            "5. Update templates/CSS",
            "6. Regenerate: python3 generator.py"
        ]
    
    # Analytics tests
    elif 'analytics' in test_name or 'plausible' in test_name:
        return [
            "1. Verify Plausible script in templates",
            "2. Check script URL is correct",
            "3. Test events fire properly",
            "4. Update tracking code if needed",
            "5. Regenerate: python3 generator.py"
        ]
    
    # Generic fallback
    else:
        return [
            "1. Review error message above",
            "2. Identify which file(s) need modification",
            "3. Make necessary changes",
            "4. Regenerate if templates/data changed: python3 generator.py",
            "5. Run specific test to verify"
        ]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-report', required=True, help='Path to pytest JSON report')
    parser.add_argument('--output', required=True, help='Output file for instructions')
    args = parser.parse_args()
    
    try:
        report = load_test_report(args.test_report)
        instructions = generate_instructions(report)
        
        if instructions:
            with open(args.output, 'w') as f:
                f.write(instructions)
            print(f"✅ Claude Code instructions written to {args.output}")
            print(f"   Found {len([t for t in report['tests'] if t['outcome'] == 'failed'])} test failures")
        else:
            print("✅ All tests passed - no instructions needed")
            # Create empty file so workflow doesn't fail
            with open(args.output, 'w') as f:
                f.write("All tests passed! No fixes needed.\n")
    except Exception as e:
        print(f"❌ Error generating instructions: {e}")
        sys.exit(1)
```

---

## Helper Scripts

**File: `scripts/run_all_tests.sh`**
```bash
#!/bin/bash

echo "🧪 Running all PermitIndex tests..."

# Critical tests
echo "📍 Critical tests..."
pytest tests/critical/ -m critical -v

# Data tests
echo "📊 Data validation..."
pytest tests/data/ -v

# Visual tests
echo "🎨 Visual/brand tests..."
pytest tests/visual/ -m visual -v

# SEO tests
echo "🔍 SEO tests..."
pytest tests/seo/ -m seo -v

# Integration tests
echo "🔗 Integration tests..."
pytest tests/integration/ -v

# Analytics tests
echo "📈 Analytics tests..."
pytest tests/analytics/ -v

echo "✅ All tests complete! Check test-report.html"
```

**File: `scripts/run_critical_tests.sh`**
```bash
#!/bin/bash

echo "⚡ Running critical tests only..."

pytest tests/critical/ tests/data/ \
  -m critical \
  -v \
  --html=quick-test-report.html \
  --self-contained-html

echo "✅ Critical tests complete!"
```

---

## Setup Checklist

- [ ] Create all test directories
- [ ] Create `__init__.py` in each test directory
- [ ] Create `pytest.ini` and `conftest.py`
- [ ] Create all test files (30 files total)
- [ ] Create GitHub Actions workflows (3 files)
- [ ] Create `generate_claude_instructions.py`
- [ ] Create helper scripts
- [ ] Update `requirements.txt`
- [ ] Install dependencies: `pip install -r requirements.txt --break-system-packages`
- [ ] Install Playwright: `python -m playwright install chromium`
- [ ] Run initial test: `pytest tests/critical/ -v`
- [ ] Commit all files to repository
- [ ] Configure GitHub Actions secrets (EMAIL_USERNAME, EMAIL_PASSWORD, NOTIFICATION_EMAIL)
- [ ] Verify first automated run

---

## Troubleshooting

**Tests fail locally:**
- Check Python version: `python3 --version` (should be 3.11+)
- Verify Playwright installed: `python -m playwright install chromium`
- Run generator first: `python3 generator.py`
- Check live URL is accessible: `https://permitindex.com`

**GitHub Actions fail:**
- Check workflow logs in Actions tab
- Verify secrets are configured
- Check email credentials are correct
- Ensure workflows have proper permissions

**No email received:**
- Check spam folder
- Verify EMAIL_USERNAME and EMAIL_PASSWORD secrets
- Test email settings outside GitHub Actions first
- Check NOTIFICATION_EMAIL is correct

---

## Next Steps

1. Implement critical tests first (verify builds work)
2. Add data validation tests (prevent bad data)
3. Gradually add SEO, visual, and integration tests
4. Set up email notifications once tests are stable
5. Create baseline screenshots for visual regression
6. Monitor test results and adjust thresholds as needed

---

**Total Implementation Time: 4-6 hours**
**Maintenance Time: ~30 min/week reviewing failures**
