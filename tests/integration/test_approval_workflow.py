import pytest
import yaml
import os

@pytest.mark.integration
def test_approve_workflow_configured():
    """Validates approve-feedback workflow is properly configured"""
    workflow_path = '.github/workflows/approve-feedback.yml'

    assert os.path.exists(workflow_path), "Approve workflow missing"

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    # YAML parses 'on' as boolean True, so check for either 'on' or True
    triggers = workflow.get('on') or workflow.get(True)
    assert triggers is not None, "Workflow missing 'on' triggers"
    assert 'issues' in triggers, "Workflow missing issues trigger"
    assert 'labeled' in triggers['issues']['types'], "Workflow missing labeled trigger"

@pytest.mark.integration
def test_process_workflow_configured():
    """Validates process-user-feedback workflow is properly configured"""
    workflow_path = '.github/workflows/process-user-feedback.yml'

    assert os.path.exists(workflow_path), "Process workflow missing"

    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    # YAML parses 'on' as boolean True, so check for either 'on' or True
    triggers = workflow.get('on') or workflow.get(True)
    assert triggers is not None, "Workflow missing 'on' triggers"
    assert 'issues' in triggers, "Workflow missing issues trigger"
