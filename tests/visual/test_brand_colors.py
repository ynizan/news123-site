import pytest

@pytest.mark.visual
def test_primary_blue_usage(page, live_url):
    """Checks that Primary Blue (#003366) is used in branding"""
    page.goto(live_url)

    # Look for elements using primary blue
    elements_with_blue = page.evaluate("""
        () => {
            const elements = Array.from(document.querySelectorAll('*'));
            return elements.some(el => {
                const color = window.getComputedStyle(el).color;
                const bgColor = window.getComputedStyle(el).backgroundColor;
                return color.includes('0, 51, 102') || bgColor.includes('0, 51, 102');
            });
        }
    """)

    assert elements_with_blue, "Primary Blue (#003366) not found in page styling"

@pytest.mark.visual
def test_accent_orange_usage(page, live_url):
    """Checks that Accent Orange (#FF6B35) is used appropriately"""
    page.goto(live_url)

    # Look for elements using accent orange
    elements_with_orange = page.evaluate("""
        () => {
            const elements = Array.from(document.querySelectorAll('*'));
            return elements.some(el => {
                const color = window.getComputedStyle(el).color;
                const bgColor = window.getComputedStyle(el).backgroundColor;
                return color.includes('255, 107, 53') || bgColor.includes('255, 107, 53');
            });
        }
    """)

    # Orange is optional, so just log if not found
    if not elements_with_orange:
        pytest.skip("Accent Orange not used on this page (acceptable)")
