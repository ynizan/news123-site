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
