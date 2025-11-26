import pytest
import pandas as pd
import os

@pytest.mark.critical
def test_permits_csv_exists():
    """Test that permits.csv exists"""
    assert os.path.exists('data/permits/permits.csv'), "permits.csv not found in data/permits/"

@pytest.mark.critical
def test_permits_csv_has_correct_columns():
    """Validate permits.csv has complete 29-column schema"""
    df = pd.read_csv('data/permits/permits.csv')

    # Complete expected schema (29 columns) - NEW ORDER as of 2025-11-19
    expected_columns = [
        # Core identification
        'agency_short', 'request_type',
        # New descriptive fields
        'description', 'processing_time',
        # Process details
        'cost', 'how_to_description', 'payment_form_url',
        # Volume & timing
        'estimated_monthly_volume', 'deadline_window', 'effort_hours',
        # Availability flags
        'online_available', 'api_available', 'mcp_available',
        # Metadata
        'related_pages', 'date_extracted', 'source_url',
        # Agency identification (moved)
        'agency_full',
        # Eligibility & scope
        'eligibility', 'location_applicability', 'document_requirements',
        # Community content (optional - enriches pages)
        'common_mistakes', 'community_feedback', 'user_tips', 'faqs',
        # Agency contact (optional - helps users)
        'agency_phone', 'agency_email', 'agency_address', 'agency_hours',
        # Contributor system
        'verified_by'
    ]

    actual_columns = list(df.columns)

    assert len(actual_columns) == 29, f"Expected 29 columns, found {len(actual_columns)}"
    assert actual_columns == expected_columns, f"Column mismatch. Expected: {expected_columns}, Got: {actual_columns}"

@pytest.mark.critical
def test_csv_valid_utf8():
    """Ensure CSV is valid UTF-8 encoded"""
    try:
        with open('data/permits/permits.csv', 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError as e:
        pytest.fail(f"CSV is not valid UTF-8: {e}")

@pytest.mark.critical
def test_required_columns_not_empty():
    """Validate that required columns have data"""
    df = pd.read_csv('data/permits/permits.csv')

    # Skip if CSV is empty (just headers)
    if len(df) == 0:
        pytest.skip("CSV is empty (no data rows)")

    required_columns = [
        'agency_short', 'agency_full', 'request_type',
        'cost', 'location_applicability', 'effort_hours',
        'online_available', 'api_available'
    ]

    for col in required_columns:
        empty_count = df[col].isna().sum() + (df[col] == '').sum()
        assert empty_count == 0, f"Required column '{col}' has {empty_count} empty values"

def test_json_columns_valid_format():
    """Validate JSON columns have valid JSON array format when populated"""
    import json

    df = pd.read_csv('data/permits/permits.csv')

    # Skip if CSV is empty
    if len(df) == 0:
        pytest.skip("CSV is empty (no data rows)")

    json_columns = ['community_feedback', 'user_tips', 'faqs']

    for col in json_columns:
        for idx, value in enumerate(df[col]):
            if pd.notna(value) and value != '':
                try:
                    parsed = json.loads(value)
                    assert isinstance(parsed, list), f"{col} row {idx+2}: Must be JSON array, got {type(parsed).__name__}"

                    # Special validation for FAQs structure
                    if col == 'faqs':
                        for faq in parsed:
                            assert isinstance(faq, dict), f"{col} row {idx+2}: FAQ items must be objects"
                            assert 'question' in faq, f"{col} row {idx+2}: FAQ missing 'question' field"
                            assert 'answer' in faq, f"{col} row {idx+2}: FAQ missing 'answer' field"

                except json.JSONDecodeError as e:
                    pytest.fail(f"{col} row {idx+2}: Invalid JSON - {str(e)}")
