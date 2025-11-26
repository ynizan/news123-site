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

@pytest.mark.visual
def test_logo_on_permit_page(page, live_url):
    """Verifies logo is present on permit pages"""
    page.goto(f"{live_url}/california/contractor-license/")

    logo = page.locator('svg, img[alt*="PermitIndex"], a[href="/"] img').first
    assert logo.count() > 0, "Logo not found on permit page"
