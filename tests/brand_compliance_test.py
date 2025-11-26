#!/usr/bin/env python3
"""
PermitIndex Brand Compliance Tests
Tests visual consistency of brand elements across the site
"""

from playwright.sync_api import sync_playwright, expect
import sys

def test_brand_compliance():
    """Test that all pages comply with brand guidelines"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Test homepage
        page.goto('http://localhost:8000')

        print("🧪 Testing Brand Compliance...")

        # Test 1: Logo exists and uses correct colors
        print("\n1️⃣ Testing logo...")
        logo = page.locator('svg[role="img"][aria-label="PermitIndex"]')
        assert logo.count() > 0, "❌ Logo SVG not found"

        # Check logo color (should be primary blue)
        logo_color = page.locator('svg[role="img"] g').get_attribute('fill')
        assert 'var(--primary)' in logo_color or '#003366' in logo_color, f"❌ Logo color incorrect: {logo_color}"
        print("   ✅ Logo present and correctly colored")

        # Test 2: Star cutouts present on cards
        print("\n2️⃣ Testing star cutouts...")
        star_boxes_count = page.locator('.star-box').count()
        assert star_boxes_count > 0, "❌ No star-box elements found"
        print(f"   ✅ Found {star_boxes_count} elements with star cutouts")

        # Test 3: Color variables defined
        print("\n3️⃣ Testing CSS variables...")
        primary_color = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--primary')")
        assert primary_color.strip() == '#003366', f"❌ Primary color incorrect: {primary_color}"

        accent_color = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--accent')")
        assert accent_color.strip() == '#FF6B35', f"❌ Accent color incorrect: {accent_color}"
        print("   ✅ CSS variables correctly defined")

        # Test 4: Typography
        print("\n4️⃣ Testing typography...")
        h1 = page.locator('h1').first
        if h1.count() > 0:
            h1_font = h1.evaluate("el => getComputedStyle(el).fontFamily")
            assert 'Arial Black' in h1_font or 'Helvetica Bold' in h1_font, f"❌ H1 font incorrect: {h1_font}"
            print("   ✅ Typography correct")

        # Test 5: Buttons have star cutouts
        print("\n5️⃣ Testing buttons...")
        buttons = page.locator('.star-button').count()
        if buttons > 0:
            print(f"   ✅ Found {buttons} branded buttons")
        else:
            print("   ⚠️  No star-button elements found")

        # Test 6: Accessibility - Logo has proper ARIA
        print("\n6️⃣ Testing accessibility...")
        logo_aria = logo.get_attribute('aria-label')
        assert logo_aria == 'PermitIndex', f"❌ Logo aria-label incorrect: {logo_aria}"

        logo_title = page.locator('svg[role="img"] title').text_content()
        assert 'PermitIndex' in logo_title, "❌ Logo <title> missing or incorrect"
        print("   ✅ Accessibility attributes present")

        # Test 7: Responsive - logo scales properly
        print("\n7️⃣ Testing responsive design...")
        page.set_viewport_size({"width": 375, "height": 667})  # Mobile
        logo_height = logo.bounding_box()['height']
        assert logo_height > 0 and logo_height < 100, f"❌ Logo height unexpected on mobile: {logo_height}"
        print("   ✅ Responsive scaling works")

        browser.close()

        print("\n✅ All brand compliance tests passed!")
        return True

def test_permit_page_brand():
    """Test brand consistency on permit detail pages"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to a permit page
        page.goto('http://localhost:8000/california/food-truck-operating-permit/')

        print("\n🧪 Testing Permit Page Brand Compliance...")

        # Test breadcrumbs exist
        breadcrumb = page.locator('nav[aria-label="Breadcrumb"]')
        assert breadcrumb.count() > 0, "❌ Breadcrumbs missing"
        print("   ✅ Breadcrumbs present")

        # Test star boxes on page
        star_boxes = page.locator('.star-box').count()
        assert star_boxes >= 2, f"❌ Expected multiple star-box cards, found {star_boxes}"
        print(f"   ✅ Found {star_boxes} branded content cards")

        # Test CTA button exists
        cta = page.locator('.star-button')
        # Note: CTA button may not exist on all pages, so just check if found
        if cta.count() > 0:
            print("   ✅ CTA button present")
        else:
            print("   ℹ️  No CTA button found (acceptable)")

        browser.close()

        print("\n✅ Permit page brand tests passed!")
        return True

def visual_regression_test():
    """Take screenshots for visual regression testing"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        print("\n📸 Taking visual regression screenshots...")

        # Screenshot homepage
        page.goto('http://localhost:8000')
        page.screenshot(path='tests/screenshots/homepage.png', full_page=True)
        print("   ✅ Homepage screenshot saved")

        # Screenshot permit page
        page.goto('http://localhost:8000/california/food-truck-operating-permit/')
        page.screenshot(path='tests/screenshots/permit-page.png', full_page=True)
        print("   ✅ Permit page screenshot saved")

        # Screenshot components
        page.goto('http://localhost:8000')

        # Logo
        page.locator('.logo').screenshot(path='tests/screenshots/logo.png')
        print("   ✅ Logo screenshot saved")

        # First star box
        if page.locator('.star-box').count() > 0:
            page.locator('.star-box').first.screenshot(path='tests/screenshots/star-box.png')
            print("   ✅ Star box screenshot saved")

        # Button
        if page.locator('.star-button').count() > 0:
            page.locator('.star-button').first.screenshot(path='tests/screenshots/button.png')
            print("   ✅ Button screenshot saved")

        browser.close()

        print("\n✅ Visual regression screenshots complete!")
        print("   Compare these with baseline images to detect unintended changes")

if __name__ == '__main__':
    try:
        # Run all tests
        test_brand_compliance()
        test_permit_page_brand()
        visual_regression_test()

        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED - Brand compliance verified!")
        print("="*60)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
