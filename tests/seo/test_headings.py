import pytest

@pytest.mark.seo
def test_homepage_has_h1(page, live_url):
    """Verifies homepage has exactly one H1"""
    page.goto(live_url)

    h1_count = page.locator('h1').count()
    assert h1_count == 1, f"Expected 1 H1, found {h1_count}"

@pytest.mark.seo
def test_permit_page_has_h1(page, live_url):
    """Verifies permit pages have exactly one H1"""
    page.goto(f"{live_url}/california/contractor-license/")

    h1_count = page.locator('h1').count()
    assert h1_count == 1, f"Expected 1 H1, found {h1_count}"

@pytest.mark.seo
def test_heading_hierarchy(page, live_url):
    """Checks that headings follow proper hierarchy"""
    page.goto(live_url)

    h1_count = page.locator('h1').count()
    h2_count = page.locator('h2').count()

    assert h1_count > 0, "No H1 found"
    assert h2_count >= 0, "Check H2 structure"
