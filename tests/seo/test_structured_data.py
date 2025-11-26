import pytest
import json

@pytest.mark.seo
def test_permit_page_has_json_ld(page, live_url):
    """Validates JSON-LD structured data exists"""
    page.goto(f"{live_url}/california/contractor-license/")

    json_ld_scripts = page.locator('script[type="application/ld+json"]').all()
    assert len(json_ld_scripts) > 0, "No JSON-LD structured data found"

@pytest.mark.seo
def test_json_ld_valid(page, live_url):
    """Verifies JSON-LD is valid JSON"""
    page.goto(f"{live_url}/california/contractor-license/")

    json_ld_scripts = page.locator('script[type="application/ld+json"]').all()

    for script in json_ld_scripts:
        content = script.inner_text()
        try:
            data = json.loads(content)
            assert '@context' in data, "Missing @context in JSON-LD"
            assert '@type' in data, "Missing @type in JSON-LD"
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON-LD: {e}")
