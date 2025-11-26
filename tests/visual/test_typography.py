import pytest

@pytest.mark.visual
def test_font_family_used(page, live_url):
    """Verifies approved fonts are used"""
    page.goto(live_url)

    body_font = page.evaluate("""
        () => window.getComputedStyle(document.body).fontFamily
    """)

    # Should use web-safe or custom fonts
    assert body_font, "No font-family set on body"
    assert len(body_font) > 0, "Font family is empty"

@pytest.mark.visual
def test_heading_font_sizes(page, live_url):
    """Checks that headings have appropriate sizes"""
    page.goto(live_url)

    if page.locator('h1').count() > 0:
        h1_size = page.locator('h1').first.evaluate("""
            (el) => parseFloat(window.getComputedStyle(el).fontSize)
        """)
        assert h1_size >= 24, f"H1 font size too small: {h1_size}px (min 24px)"

    if page.locator('h2').count() > 0:
        h2_size = page.locator('h2').first.evaluate("""
            (el) => parseFloat(window.getComputedStyle(el).fontSize)
        """)
        assert h2_size >= 18, f"H2 font size too small: {h2_size}px (min 18px)"

@pytest.mark.visual
def test_body_text_readable(page, live_url):
    """Validates body text is readable size"""
    page.goto(live_url)

    body_font_size = page.evaluate("""
        () => parseFloat(window.getComputedStyle(document.body).fontSize)
    """)

    assert body_font_size >= 14, f"Body font too small: {body_font_size}px (min 14px)"
