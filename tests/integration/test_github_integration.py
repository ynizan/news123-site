import pytest
import os

@pytest.mark.integration
def test_github_workflows_exist():
    """Verifies GitHub Actions workflows are configured"""
    workflows_dir = '.github/workflows'

    assert os.path.exists(workflows_dir), "Workflows directory missing"

    expected_workflows = [
        'process-user-feedback.yml',
        'approve-feedback.yml'
    ]

    for workflow in expected_workflows:
        workflow_path = os.path.join(workflows_dir, workflow)
        assert os.path.exists(workflow_path), f"Workflow missing: {workflow}"

@pytest.mark.integration
def test_feedback_csv_writable():
    """Checks that feedback CSV exists and is writable"""
    csv_path = 'data/feedback/user_feedback.csv'

    if not os.path.exists(csv_path):
        pytest.skip("Feedback CSV not yet created")

    assert os.access(csv_path, os.W_OK), "Feedback CSV not writable"
