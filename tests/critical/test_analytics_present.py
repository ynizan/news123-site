import pytest

@pytest.mark.critical
def test_plausible_script_exists(page, live_url):
    """Confirm Plausible script tag exists in head"""
    response = page.goto(live_url)

    # Handle 403 from Cloudflare bot protection on production
    if response.status == 403 and 'news123.info' in live_url:
        pytest.skip("Production site has bot protection enabled (403)")

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
    response = page.goto(live_url)

    # Handle 403 from Cloudflare bot protection on production
    if response.status == 403 and 'news123.info' in live_url:
        pytest.skip("Production site has bot protection enabled (403)")

    page.wait_for_timeout(2000)  # Wait for script to load

    assert len(responses) > 0, "Plausible script did not load"
    assert any(r.ok for r in responses), "Plausible script failed to load successfully"

@pytest.mark.critical
def test_plausible_initialized(page, live_url):
    """Test that plausible object is initialized"""
    response = page.goto(live_url)

    # Handle 403 from Cloudflare bot protection on production
    if response.status == 403 and 'news123.info' in live_url:
        pytest.skip("Production site has bot protection enabled (403)")

    page.wait_for_timeout(2000)

    has_plausible = page.evaluate('typeof window.plausible !== "undefined"')
    assert has_plausible, "window.plausible object not initialized"
