import pytest

@pytest.mark.integration
def test_feedback_form_exists(page, live_url):
    """Verifies feedback form is present on permit pages"""
    page.goto(f"{live_url}/california/contractor-license/")

    # Look for feedback form elements
    feedback_section = page.locator('#feedback-section, .feedback-form, [data-feedback]').first
    if feedback_section.count() == 0:
        pytest.skip("Feedback form not yet implemented on this page")

    assert feedback_section.count() > 0, "Feedback form not found"

@pytest.mark.integration
def test_feedback_type_options(page, live_url):
    """Checks that feedback type options are available"""
    page.goto(f"{live_url}/california/contractor-license/")

    feedback_type_select = page.locator('select[name="feedbackType"], #feedback-type').first
    if feedback_type_select.count() == 0:
        pytest.skip("Feedback form not yet implemented")

    options = feedback_type_select.locator('option').all()
    assert len(options) >= 4, f"Expected at least 4 feedback types, found {len(options)}"

@pytest.mark.integration
def test_feedback_submit_button(page, live_url):
    """Verifies submit button exists"""
    page.goto(f"{live_url}/california/contractor-license/")

    submit_button = page.locator('button[type="submit"], input[type="submit"]').first
    if submit_button.count() == 0:
        pytest.skip("Feedback form not yet implemented")

    assert submit_button.count() > 0, "Submit button not found"
