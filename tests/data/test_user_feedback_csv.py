import pytest
import pandas as pd
import os

def test_user_feedback_csv_schema():
    """Validates user_feedback.csv schema if it exists"""
    csv_path = 'data/feedback/user_feedback.csv'

    if not os.path.exists(csv_path):
        pytest.skip("user_feedback.csv does not exist yet")

    df = pd.read_csv(csv_path)

    expected_columns = [
        'permit_slug', 'feedback_type', 'feedback_text',
        'helpful_count', 'created_at', 'approved', 'github_issue_number'
    ]

    assert list(df.columns) == expected_columns, f"Column mismatch: {list(df.columns)}"

def test_feedback_type_values():
    """Checks feedback_type values are valid"""
    csv_path = 'data/feedback/user_feedback.csv'

    if not os.path.exists(csv_path):
        pytest.skip("user_feedback.csv does not exist yet")

    df = pd.read_csv(csv_path)

    valid_types = ['tip', 'common_mistake', 'time_estimate', 'cost_note']
    invalid = df[~df['feedback_type'].isin(valid_types)]

    assert len(invalid) == 0, f"Invalid feedback_type values: {invalid['feedback_type'].unique()}"

def test_approved_field():
    """Verifies approved field contains only 'yes' or 'no'"""
    csv_path = 'data/feedback/user_feedback.csv'

    if not os.path.exists(csv_path):
        pytest.skip("user_feedback.csv does not exist yet")

    df = pd.read_csv(csv_path)

    valid_values = ['yes', 'no']
    invalid = df[~df['approved'].isin(valid_values)]

    assert len(invalid) == 0, f"Invalid approved values: {invalid['approved'].unique()}"
