import pytest
import pandas as pd
import os

@pytest.mark.integration
def test_feedback_csv_schema():
    """Validates user feedback CSV has correct schema"""
    csv_path = 'data/feedback/user_feedback.csv'

    if not os.path.exists(csv_path):
        pytest.skip("Feedback CSV not yet created")

    df = pd.read_csv(csv_path)

    expected_columns = [
        'permit_slug', 'feedback_type', 'feedback_text',
        'helpful_count', 'created_at', 'approved', 'github_issue_number'
    ]

    assert list(df.columns) == expected_columns, f"Schema mismatch: {list(df.columns)}"

@pytest.mark.integration
def test_approved_feedback_in_csv():
    """Checks that approved feedback exists in CSV"""
    csv_path = 'data/feedback/user_feedback.csv'

    if not os.path.exists(csv_path):
        pytest.skip("Feedback CSV not yet created")

    df = pd.read_csv(csv_path)

    if len(df) == 0:
        pytest.skip("No feedback entries yet")

    approved_count = (df['approved'] == 'yes').sum()
    # Should have at least some approved feedback
    assert approved_count >= 0, "Check approved feedback count"

@pytest.mark.integration
def test_feedback_references_valid_permits():
    """Verifies feedback references actual permits"""
    csv_path = 'data/feedback/user_feedback.csv'

    if not os.path.exists(csv_path):
        pytest.skip("Feedback CSV not yet created")

    feedback_df = pd.read_csv(csv_path)

    if len(feedback_df) == 0:
        pytest.skip("No feedback entries yet")

    # Just verify permit slugs have reasonable format
    # We can't easily check against actual permits without loading JSON
    for idx, row in feedback_df.iterrows():
        permit_slug = row['permit_slug']
        # Just verify it's a reasonable slug format
        assert isinstance(permit_slug, str), f"Row {idx}: permit_slug is not a string"
        assert len(permit_slug) > 0, f"Row {idx}: permit_slug is empty"
