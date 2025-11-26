import pytest

@pytest.mark.analytics
def test_plausible_pageview_tracking(page, live_url):
    """Verifies Plausible tracks pageviews"""
    events = []

    def handle_request(request):
        if 'plausible.io/api/event' in request.url:
            events.append(request.post_data_json)

    page.on('request', handle_request)
    page.goto(live_url)
    page.wait_for_timeout(2000)

    # Plausible should fire at least one event (pageview)
    pageview_events = [e for e in events if e and e.get('n') == 'pageview']
    assert len(pageview_events) > 0, "Plausible pageview event did not fire"

@pytest.mark.analytics
def test_plausible_domain_tracking(page, live_url):
    """Checks that Plausible tracks correct domain"""
    page.goto(live_url)
    page.wait_for_timeout(2000)

    # Verify data-domain attribute is set correctly
    plausible_script = page.locator('script[src*="plausible.io"]').first
    if plausible_script.count() > 0:
        data_domain = plausible_script.get_attribute('data-domain')
        assert data_domain, "Plausible data-domain not set"
        assert 'permitindex' in data_domain.lower(), f"Unexpected domain: {data_domain}"
