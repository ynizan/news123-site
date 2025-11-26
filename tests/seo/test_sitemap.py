import pytest
import xml.etree.ElementTree as ET

@pytest.mark.seo
def test_sitemap_exists(page, live_url):
    """Confirms sitemap.xml exists"""
    response = page.goto(f"{live_url}/sitemap.xml")
    assert response.status == 200, f"Sitemap returned {response.status}"

@pytest.mark.seo
def test_sitemap_valid_xml(page, live_url):
    """Validates XML structure is well-formed"""
    page.goto(f"{live_url}/sitemap.xml")
    content = page.content()

    assert '<?xml' in content, "Missing XML declaration"
    assert '<urlset' in content, "Not a valid sitemap"

    try:
        ET.fromstring(content)
    except ET.ParseError as e:
        pytest.fail(f"Invalid XML: {e}")

@pytest.mark.seo
def test_homepage_in_sitemap(page, live_url):
    """Checks homepage is included in sitemap"""
    page.goto(f"{live_url}/sitemap.xml")
    content = page.content()

    assert f'<loc>{live_url}</loc>' in content or f'<loc>{live_url}/</loc>' in content, "Homepage not in sitemap"
