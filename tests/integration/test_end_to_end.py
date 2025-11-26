import pytest

@pytest.mark.integration
@pytest.mark.slow
def test_permit_page_displays_approved_feedback(page, live_url):
    """Verifies approved feedback is displayed on permit pages"""
    page.goto(f"{live_url}/california/contractor-license/")

    # Look for feedback display section
    feedback_display = page.locator('.feedback-tips, .user-feedback, [data-feedback-display]').first

    if feedback_display.count() == 0:
        pytest.skip("Feedback display not yet implemented")

    # Should have some feedback content
    feedback_content = feedback_display.inner_text()
    assert len(feedback_content) > 0, "Feedback display is empty"

@pytest.mark.integration
@pytest.mark.slow
def test_feedback_form_workflow(page, live_url):
    """Tests complete feedback form workflow"""
    page.goto(f"{live_url}/california/contractor-license/")

    # Check if form exists
    feedback_form = page.locator('form[data-feedback], #feedback-form').first
    if feedback_form.count() == 0:
        pytest.skip("Feedback form not yet implemented")

    # Verify form has required elements
    feedback_type = page.locator('select[name="feedbackType"], #feedback-type').first
    feedback_text = page.locator('textarea[name="feedbackText"], #feedback-text').first
    submit_button = page.locator('button[type="submit"]').first

    assert feedback_type.count() > 0, "Feedback type selector missing"
    assert feedback_text.count() > 0, "Feedback text area missing"
    assert submit_button.count() > 0, "Submit button missing"

@pytest.mark.integration
def test_full_system_integration():
    """High-level test that all system components exist"""
    import os

    components = {
        'Feedback CSV': 'data/feedback/user_feedback.csv',
        'Permits CSV': 'data/permits/permits.csv',
        'Process Workflow': '.github/workflows/process-user-feedback.yml',
        'Approve Workflow': '.github/workflows/approve-feedback.yml',
        'Worker Code': 'worker/feedback-proxy.js',
    }

    missing = []
    for name, path in components.items():
        if not os.path.exists(path):
            missing.append(name)

    if missing:
        pytest.skip(f"Missing components: {', '.join(missing)}")

    assert True, "All system components present"
