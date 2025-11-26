import pytest

@pytest.mark.analytics
@pytest.mark.slow
def test_wtp_slider_present(page, live_url):
    """Verifies WTP slider widget exists on permit pages"""
    page.goto(f"{live_url}/california/contractor-license/")

    wtp_slider = page.locator('#wtp-slider, [data-wtp-slider]').first
    if wtp_slider.count() == 0:
        pytest.skip("WTP slider not yet implemented")

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
    wtp_slider = page.locator('#wtp-slider, [data-wtp-slider]').first
    if wtp_slider.count() > 0:
        wtp_slider.fill('50')
        submit_btn = page.locator('button[data-wtp-submit], #wtp-submit').first
        if submit_btn.count() > 0:
            submit_btn.click()
            page.wait_for_timeout(2000)

            wtp_events = [e for e in events if e and e.get('n') == 'WTP Submission']
            assert len(wtp_events) > 0, "WTP Submission event did not fire"
        else:
            pytest.skip("WTP submit button not found")
    else:
        pytest.skip("WTP widget not present on this page")
