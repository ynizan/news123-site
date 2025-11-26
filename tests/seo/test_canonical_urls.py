import pytest

@pytest.mark.seo
def test_homepage_has_canonical(page, live_url):
    """Verifies homepage has canonical URL"""
    page.goto(live_url)

    canonical = page.locator('link[rel="canonical"]').get_attribute('href')
    assert canonical, "No canonical URL found on homepage"
    assert canonical.startswith('http'), "Canonical URL should be absolute"

@pytest.mark.seo
def test_permit_page_has_canonical(page, live_url):
    """Verifies permit pages have canonical URL"""
    page.goto(f"{live_url}/california/contractor-license/")

    canonical = page.locator('link[rel="canonical"]').get_attribute('href')
    assert canonical, "No canonical URL found on permit page"
    assert canonical.startswith('http'), "Canonical URL should be absolute"
