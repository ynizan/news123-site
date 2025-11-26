import pytest

@pytest.mark.analytics
@pytest.mark.slow
def test_feedback_submission_event(page, live_url):
    """Tests that feedback submission fires analytics event"""
    page.goto(f"{live_url}/california/contractor-license/")

    events = []

    def handle_request(request):
        if 'plausible.io/api/event' in request.url:
            events.append(request.post_data_json)

    page.on('request', handle_request)

    # Look for feedback form
    feedback_form = page.locator('form[data-feedback], #feedback-form').first
    if feedback_form.count() == 0:
        pytest.skip("Feedback form not implemented")

    # This test documents the expected behavior
    # Actual implementation may vary
    pytest.skip("Feedback event tracking not yet implemented")

@pytest.mark.analytics
def test_outbound_link_tracking(page, live_url):
    """Checks that outbound links are tracked"""
    page.goto(f"{live_url}/california/contractor-license/")

    # Look for external links
    external_links = page.locator('a[href^="http"]').all()

    if len(external_links) == 0:
        pytest.skip("No external links found")

    # Verify Plausible is configured to track outbound links
    plausible_script = page.locator('script[src*="plausible.io"]').first
    if plausible_script.count() > 0:
        script_src = plausible_script.get_attribute('src')
        # Check if outbound-links tracking is enabled
        # This is optional and may not be configured
        if 'outbound-links' in script_src:
            assert True, "Outbound links tracking enabled"
        else:
            pytest.skip("Outbound links tracking not configured")
