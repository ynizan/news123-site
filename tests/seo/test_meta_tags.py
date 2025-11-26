import pytest

@pytest.mark.seo
def test_homepage_has_title(page, live_url):
    """Verifies homepage has title tag"""
    page.goto(live_url)

    title = page.title()
    assert title, "No title tag found"
    assert 10 <= len(title) <= 60, f"Title length {len(title)} outside recommended 10-60 chars"

@pytest.mark.seo
def test_homepage_meta_description(page, live_url):
    """Checks meta description exists and is proper length"""
    page.goto(live_url)

    description = page.locator('meta[name="description"]').get_attribute('content')
    assert description, "No meta description found"
    assert 50 <= len(description) <= 160, f"Description length {len(description)} outside 50-160 chars"

@pytest.mark.seo
def test_open_graph_tags(page, live_url):
    """Validates Open Graph tags"""
    page.goto(live_url)

    og_title = page.locator('meta[property="og:title"]').get_attribute('content')
    og_description = page.locator('meta[property="og:description"]').get_attribute('content')
    og_image = page.locator('meta[property="og:image"]').get_attribute('content')
    og_url = page.locator('meta[property="og:url"]').get_attribute('content')

    assert og_title, "Missing og:title"
    assert og_description, "Missing og:description"
    assert og_image, "Missing og:image"
    assert og_url, "Missing og:url"

@pytest.mark.seo
def test_permit_page_unique_title(page, live_url):
    """Test permit pages have unique titles"""
    page.goto(f"{live_url}/california/contractor-license/")
    title1 = page.title()

    page.goto(f"{live_url}/california/food-truck-permit/")
    title2 = page.title()

    assert title1 != title2, "Permit pages have duplicate titles"
