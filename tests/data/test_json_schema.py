import pytest
import json
import os
import re

@pytest.mark.critical
def test_permits_json_exists():
    """Test that permits.json exists"""
    assert os.path.exists('data/permits/permits.json'), "permits.json not found in data/permits/"

@pytest.mark.critical
def test_permits_json_valid_format():
    """Validate permits.json is valid JSON and is an array"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert isinstance(data, list), f"JSON must be an array, got {type(data).__name__}"
    assert len(data) > 0, "JSON array is empty"

@pytest.mark.critical
def test_permits_json_has_correct_fields():
    """Validate permits.json has complete 31-field schema"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Complete expected schema (31 fields) - as of 2025-11-19
    expected_fields = [
        # Core identification
        'id', 'name', 'agency_short', 'request_type',
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

    # Check first permit object
    first_permit = data[0]
    actual_fields = list(first_permit.keys())

    assert len(actual_fields) == 31, f"Expected 31 fields, found {len(actual_fields)}"

    # Check all expected fields are present
    missing_fields = set(expected_fields) - set(actual_fields)
    assert not missing_fields, f"Missing fields: {missing_fields}"

    # Check for extra fields
    extra_fields = set(actual_fields) - set(expected_fields)
    assert not extra_fields, f"Unexpected extra fields: {extra_fields}"

@pytest.mark.critical
def test_required_fields_not_empty():
    """Validate that required fields have data"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Skip if JSON is empty
    if len(data) == 0:
        pytest.skip("JSON is empty (no permits)")

    required_fields = [
        'id', 'name', 'agency_short', 'agency_full', 'request_type',
        'cost', 'location_applicability', 'effort_hours',
        'online_available', 'api_available'
    ]

    for idx, permit in enumerate(data):
        for field in required_fields:
            value = permit.get(field)
            assert value is not None, f"Permit {idx}: Required field '{field}' is None"
            assert value != '', f"Permit {idx}: Required field '{field}' is empty string"

def test_array_fields_valid_format():
    """Validate array fields are actual arrays when populated"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Skip if JSON is empty
    if len(data) == 0:
        pytest.skip("JSON is empty (no permits)")

    array_fields = ['community_feedback', 'user_tips', 'faqs']

    for idx, permit in enumerate(data):
        for field in array_fields:
            value = permit.get(field)

            # Field should exist (can be empty array)
            assert field in permit, f"Permit {idx}: Missing field '{field}'"

            # If not empty string or None, must be array
            if value and value != '':
                assert isinstance(value, list), f"Permit {idx}: Field '{field}' must be array, got {type(value).__name__}"

                # Special validation for FAQs structure
                if field == 'faqs':
                    for faq_idx, faq in enumerate(value):
                        assert isinstance(faq, dict), f"Permit {idx}, FAQ {faq_idx}: Must be object"
                        assert 'question' in faq, f"Permit {idx}, FAQ {faq_idx}: Missing 'question' field"
                        assert 'answer' in faq, f"Permit {idx}, FAQ {faq_idx}: Missing 'answer' field"

@pytest.mark.critical
def test_id_field_format():
    """Validate that id field is present and has valid UUID format (required field)"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Skip if JSON is empty
    if len(data) == 0:
        pytest.skip("JSON is empty (no permits)")

    # UUID v4 pattern
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    for idx, permit in enumerate(data):
        # ID field must exist (required)
        assert 'id' in permit, f"Permit {idx}: Missing required 'id' field"
        
        id_value = permit.get('id')
        # ID is required, must not be empty or null
        assert id_value is not None, f"Permit {idx}: 'id' field cannot be None"
        assert id_value != '', f"Permit {idx}: 'id' field cannot be empty string"
        assert isinstance(id_value, str), f"Permit {idx}: 'id' must be a string"
        assert uuid_pattern.match(id_value), f"Permit {idx}: 'id' must be a valid UUID format, got '{id_value}'"

def test_related_pages_format():
    """Validate that related_pages field contains valid UUIDs (permit IDs)"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Skip if JSON is empty
    if len(data) == 0:
        pytest.skip("JSON is empty (no permits)")

    # UUID v4 pattern
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    # Create a set of all permit IDs for reference validation
    all_permit_ids = {permit['id'] for permit in data}

    for idx, permit in enumerate(data):
        # related_pages field must exist
        assert 'related_pages' in permit, f"Permit {idx}: Missing 'related_pages' field"

        related_pages = permit.get('related_pages')

        # Must be an array
        assert isinstance(related_pages, list), f"Permit {idx}: 'related_pages' must be an array, got {type(related_pages).__name__}"

        # If not empty, validate each item is a valid UUID
        if len(related_pages) > 0:
            for page_idx, page_id in enumerate(related_pages):
                assert isinstance(page_id, str), f"Permit {idx}, related_pages[{page_idx}]: Must be a string, got {type(page_id).__name__}"
                assert page_id != '', f"Permit {idx}, related_pages[{page_idx}]: Cannot be empty string"
                assert uuid_pattern.match(page_id), f"Permit {idx}, related_pages[{page_idx}]: Must be a valid UUID format, got '{page_id}'"

                # Optional: Validate that the ID references an actual permit (not self)
                if page_id in all_permit_ids:
                    assert page_id != permit['id'], f"Permit {idx}, related_pages[{page_idx}]: Cannot reference itself"
                # Note: We don't fail if ID doesn't exist, as permits might be in separate files

@pytest.mark.critical
def test_name_field_format():
    """Validate that name field is present and has 2-word format (required field)"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Skip if JSON is empty
    if len(data) == 0:
        pytest.skip("JSON is empty (no permits)")

    for idx, permit in enumerate(data):
        # name field must exist (required)
        assert 'name' in permit, f"Permit {idx}: Missing required 'name' field"
        
        name_value = permit.get('name')
        
        # name is required, must not be empty or null
        assert name_value is not None, f"Permit {idx}: 'name' field cannot be None"
        assert name_value != '', f"Permit {idx}: 'name' field cannot be empty string"
        assert isinstance(name_value, str), f"Permit {idx}: 'name' must be a string"
        words = name_value.split()
        assert len(words) == 2, f"Permit {idx}: 'name' must be exactly 2 words, got '{name_value}' ({len(words)} words)"
