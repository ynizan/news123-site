import pytest

@pytest.mark.seo
def test_robots_txt_exists(page, live_url):
    """Confirms robots.txt exists"""
    response = page.goto(f"{live_url}/robots.txt")
    assert response.status == 200, f"robots.txt returned {response.status}"

@pytest.mark.seo
def test_sitemap_in_robots(page, live_url):
    """Tests that sitemap location is declared in robots.txt"""
    page.goto(f"{live_url}/robots.txt")
    content = page.content()

    assert 'Sitemap:' in content, "Sitemap not declared in robots.txt"
    assert 'sitemap.xml' in content.lower(), "sitemap.xml not referenced"
