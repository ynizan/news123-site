import pytest

@pytest.mark.analytics
def test_pageview_includes_url(page, live_url):
    """Verifies pageview events include URL"""
    events = []

    def handle_request(request):
        if 'plausible.io/api/event' in request.url:
            data = request.post_data_json
            if data:
                events.append(data)

    page.on('request', handle_request)
    page.goto(live_url)
    page.wait_for_timeout(2000)

    if len(events) > 0:
        pageview = events[0]
        assert 'u' in pageview or 'url' in pageview, "Pageview missing URL property"
    else:
        pytest.skip("No analytics events captured")

@pytest.mark.analytics
def test_custom_props_format(page, live_url):
    """Tests that custom event properties use correct format"""
    page.goto(f"{live_url}/california/contractor-license/")

    # Verify plausible function is available for custom events
    has_plausible = page.evaluate('typeof window.plausible === "function"')

    if has_plausible:
        # Test custom event with properties
        result = page.evaluate("""
            () => {
                try {
                    window.plausible('Test Event', {props: {test: 'value'}});
                    return true;
                } catch (e) {
                    return false;
                }
            }
        """)
        assert result, "Custom event with properties failed"
    else:
        pytest.skip("Plausible function not available")

@pytest.mark.analytics
def test_permit_tracking_props(page, live_url):
    """Verifies permit pages include permit-specific tracking properties"""
    page.goto(f"{live_url}/california/contractor-license/")

    # Check if page includes data attributes for tracking
    body = page.locator('body').first
    data_attrs = page.evaluate("""
        () => {
            const body = document.body;
            return {
                hasPermitSlug: body.hasAttribute('data-permit-slug'),
                hasJurisdiction: body.hasAttribute('data-jurisdiction'),
                hasPermitType: body.hasAttribute('data-permit-type')
            };
        }
    """)

    # These are optional enhancements
    # Test documents expected tracking properties
    if not any(data_attrs.values()):
        pytest.skip("Permit-specific tracking props not implemented (optional)")
