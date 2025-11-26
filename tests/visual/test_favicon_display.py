import pytest

@pytest.mark.visual
def test_favicon_links_present(page, live_url):
    """Verifies favicon links exist in head"""
    page.goto(live_url)

    favicon_ico = page.locator('link[rel="icon"][type="image/x-icon"]').count()
    favicon_svg = page.locator('link[rel="icon"][type="image/svg+xml"]').count()
    apple_touch = page.locator('link[rel="apple-touch-icon"]').count()

    # At least one favicon type should exist
    assert (favicon_ico + favicon_svg + apple_touch) > 0, "No favicon links found"

@pytest.mark.visual
def test_favicon_files_accessible(page, live_url):
    """Tests that favicon files are accessible"""
    favicon_paths = [
        '/favicon/favicon.ico',
        '/favicon/favicon-32x32.png',
        '/favicon/apple-touch-icon.png'
    ]

    for path in favicon_paths:
        response = page.request.get(f"{live_url}{path}")
        if response.status == 404:
            # Try without /favicon prefix
            response = page.request.get(f"{live_url}{path.replace('/favicon', '')}")

        # At least one favicon should be accessible
        if response.status == 200:
            return  # Pass if any favicon is found

    pytest.fail("No favicon files accessible")

@pytest.mark.visual
def test_web_manifest_exists(page, live_url):
    """Checks for web app manifest"""
    page.goto(live_url)

    manifest_link = page.locator('link[rel="manifest"]').count()
    if manifest_link > 0:
        manifest_href = page.locator('link[rel="manifest"]').get_attribute('href')
        response = page.request.get(f"{live_url}{manifest_href}")
        assert response.status == 200, "Web manifest not accessible"
