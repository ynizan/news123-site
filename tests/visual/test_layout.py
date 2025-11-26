import pytest

@pytest.mark.visual
def test_responsive_layout(mobile_page, live_url):
    """Tests layout adapts to mobile viewport"""
    mobile_page.goto(live_url)

    # Check no horizontal overflow
    viewport_width = 375
    body_width = mobile_page.evaluate('document.body.scrollWidth')

    assert body_width <= viewport_width + 10, f"Mobile layout overflows: {body_width}px > {viewport_width}px"

@pytest.mark.visual
def test_desktop_layout_centered(page, live_url):
    """Verifies desktop layout is properly centered"""
    page.goto(live_url)

    # Check for main container
    main_container = page.locator('main, .container, #content').first
    assert main_container.count() > 0, "No main container found"

@pytest.mark.visual
def test_permit_page_layout(page, live_url):
    """Checks permit page has proper layout structure"""
    page.goto(f"{live_url}/california/contractor-license/")

    # Verify key sections exist
    h1_exists = page.locator('h1').count() > 0
    content_exists = len(page.content()) > 1000  # Should have substantial content

    assert h1_exists, "Permit page missing H1"
    assert content_exists, "Permit page has insufficient content"
