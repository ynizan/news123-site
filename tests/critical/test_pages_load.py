import pytest
import os

@pytest.mark.critical
def test_homepage_loads(page, live_url):
    """Test homepage returns 200"""
    response = page.goto(live_url)

    # Handle 403 from Cloudflare bot protection on production
    if response.status == 403 and 'permitindex.com' in live_url:
        pytest.skip("Production site has bot protection enabled (403)")

    assert response.status == 200, f"Homepage returned {response.status}"

@pytest.mark.critical
def test_sample_permit_page_loads(page, live_url):
    """Test a sample permit page loads"""
    response = page.goto(f"{live_url}/california/los-angeles/apply-for-a-business-license/")

    # Handle 403 from Cloudflare bot protection on production
    if response.status == 403 and 'permitindex.com' in live_url:
        pytest.skip("Production site has bot protection enabled (403)")

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
    response = page.goto(live_url)

    # Handle 403 from Cloudflare bot protection on production
    if response.status == 403 and 'permitindex.com' in live_url:
        pytest.skip("Production site has bot protection enabled (403)")

    # Filter out known acceptable errors
    real_errors = [e for e in errors if 'favicon' not in e.lower()]

    assert len(real_errors) == 0, f"Console errors found: {real_errors}"
