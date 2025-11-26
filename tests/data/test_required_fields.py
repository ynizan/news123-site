import pytest
import json

@pytest.mark.critical
def test_no_empty_required_fields():
    """Confirms no empty values in required fields"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    required_fields = ['agency_short', 'request_type', 'cost', 'effort_hours']

    for idx, permit in enumerate(data):
        for field in required_fields:
            value = permit.get(field)
            assert value is not None, f"Permit {idx}: Field '{field}' is None"
            assert value != '', f"Permit {idx}: Field '{field}' is empty string"

@pytest.mark.critical
def test_unique_composite_key():
    """Validates that composite key (agency_short + request_type) is unique"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    composite_keys = set()
    duplicates = []

    for idx, permit in enumerate(data):
        key = f"{permit.get('agency_short', '')}|||{permit.get('request_type', '')}"
        if key in composite_keys:
            duplicates.append((idx, key))
        composite_keys.add(key)

    assert len(duplicates) == 0, f"Found {len(duplicates)} duplicate composite keys: {[k for _, k in duplicates]}"

@pytest.mark.critical
def test_boolean_fields_valid():
    """Checks boolean fields contain only 'Yes' or 'No'"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    boolean_fields = ['online_available', 'api_available', 'mcp_available']

    for idx, permit in enumerate(data):
        for field in boolean_fields:
            value = permit.get(field, '')
            valid_values = ['Yes', 'No', '']  # Allow empty for optional fields like mcp_available
            assert value in valid_values, f"Permit {idx}: Field '{field}' has invalid value '{value}' (expected 'Yes', 'No', or empty)"
