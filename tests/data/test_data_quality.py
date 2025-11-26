import pytest
import json
from urllib.parse import urlparse
from datetime import datetime

@pytest.mark.critical
def test_urls_valid_format():
    """Verifies all URLs are valid format"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    url_fields = ['payment_form_url', 'source_url']

    for field in url_fields:
        for idx, permit in enumerate(data):
            url = permit.get(field, '')
            if url and url.strip():  # Only validate non-empty URLs
                try:
                    parsed = urlparse(url)
                    assert parsed.scheme in ['http', 'https'], f"Permit {idx} {field}: Invalid scheme"
                    assert parsed.netloc, f"Permit {idx} {field}: No domain"
                except Exception as e:
                    pytest.fail(f"Permit {idx} {field}: Invalid URL '{url}' - {e}")

@pytest.mark.critical
def test_dates_iso_format():
    """Checks dates are in ISO format (YYYY-MM-DD)"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    date_fields = ['date_extracted']

    for field in date_fields:
        for idx, permit in enumerate(data):
            date_str = permit.get(field, '')
            if date_str and date_str.strip():  # Only validate non-empty dates
                try:
                    datetime.strptime(str(date_str), '%Y-%m-%d')
                except ValueError:
                    pytest.fail(f"Permit {idx} {field}: Invalid date format '{date_str}' (expected YYYY-MM-DD)")

@pytest.mark.critical
def test_cost_field_reasonable():
    """Validates cost field contains reasonable values"""
    with open('data/permits/permits.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for idx, permit in enumerate(data):
        cost = permit.get('cost', '')
        cost_str = str(cost).lower()

        # Should not be negative
        assert not cost_str.startswith('-'), f"Permit {idx}: Negative cost '{cost}'"

        # Should contain reasonable patterns
        valid_patterns = ['$', 'free', 'varies', '-', 'contact', 'no fee', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        assert any(p in cost_str for p in valid_patterns), f"Permit {idx}: Suspicious cost format '{cost}'"
