import pytest
from urllib.parse import urljoin, urlparse

@pytest.mark.critical
@pytest.mark.slow
def test_homepage_internal_links(page, live_url):
    """Crawl homepage and check all internal links return 200"""
    response = page.goto(live_url)

    # Handle 403 from Cloudflare bot protection on production
    if response.status == 403 and 'permitindex.com' in live_url:
        pytest.skip("Production site has bot protection enabled (403)")

    links = page.locator('a[href]').all()
    internal_links = []

    for link in links:
        href = link.get_attribute('href')
        if href and not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            full_url = urljoin(live_url, href)
            if urlparse(full_url).netloc == urlparse(live_url).netloc:
                internal_links.append(full_url)

    # Test unique internal links
    unique_links = list(set(internal_links))
    broken_links = []

    for link in unique_links[:20]:  # Test first 20 to keep it fast
        try:
            response = page.goto(link, timeout=10000)
            if response.status >= 400:
                broken_links.append((link, response.status))
        except Exception as e:
            broken_links.append((link, str(e)))

    assert len(broken_links) == 0, f"Broken internal links: {broken_links}"
