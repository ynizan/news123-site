# News123 Brand Implementation Guide

**For: Claude Code**  
**Purpose:** Implement brand guidelines consistently across the News123 site

---

## Overview

This document provides step-by-step instructions for implementing the News123 brand system, including:
1. CSS setup with brand variables
2. Logo implementation (SVG)
3. Star cutout system for all elements
4. Component patterns
5. Automated testing with Playwright

---

## Part 1: Initial Setup

### 1.1 CSS Variables

Add these variables to your main CSS file (or in a `<style>` tag in your Jinja2 base template):

```css
:root {
    /* Colors */
    --primary: #003366;
    --accent: #FF6B35;
    --text: #1a1a1a;
    --text-light: #666666;
    --bg: #ffffff;
    --bg-light: #f8f9fa;
    --border: #e0e0e0;
    --success: #10b981;
    
    /* Typography */
    --font-display: 'Arial Black', 'Helvetica Bold', sans-serif;
    --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    
    /* Spacing */
    --radius-large: 12px;
    --radius-medium: 8px;
    --radius-small: 6px;
    
    /* Shadows */
    --shadow-low: 0 2px 8px rgba(0,0,0,0.05);
    --shadow-medium: 0 4px 16px rgba(0,0,0,0.1);
    --shadow-high: 0 8px 24px rgba(0,0,0,0.15);
}
```

### 1.2 Base Typography

```css
body {
    font-family: var(--font-body);
    color: var(--text);
    line-height: 1.6;
    background: var(--bg-light);
}

h1, h2 {
    font-family: var(--font-display);
    font-weight: 900;
    letter-spacing: -1px;
    color: var(--primary);
}

h1 { font-size: 32px; }
h2 { font-size: 24px; }
h3 { font-size: 20px; font-weight: 700; }
h4 { font-size: 18px; font-weight: 700; }
```

---

## Part 2: Logo Implementation

### 2.1 Horizontal Logo (Primary)

**Location:** Header/Navigation

**Implementation:**
```html
<div class="logo">
    <svg viewBox="0 0 240 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="News123">
        <title>News123</title>
        <desc>News123 - Complete database of US government transactions</desc>
        <defs>
            <mask id="p-star-mask">
                <rect width="100%" height="100%" fill="white"/>
                <polygon points="20,2 21.5,6 25.5,6 22.2,8.5 23.5,12.5 20,9.8 16.5,12.5 17.8,8.5 14.5,6 18.5,6" fill="black"/>
            </mask>
        </defs>
        <g fill="var(--primary)" font-family="Arial Black, sans-serif" font-weight="900">
            <text x="0" y="32" font-size="36" letter-spacing="-1" mask="url(#p-star-mask)">P</text>
            <text x="25" y="32" font-size="36" letter-spacing="-1">ermitIndex</text>
        </g>
    </svg>
</div>
```

**CSS:**
```css
.logo svg {
    height: 32px;
    width: auto;
}

/* For dark backgrounds */
.dark-bg .logo svg g {
    fill: white;
}
```

### 2.2 Icon/Favicon

**Location:** favicon.ico, app icons

**Implementation:**
```html
<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <mask id="p-icon-mask">
            <rect width="100%" height="100%" fill="white"/>
            <polygon points="20,2 21.5,6 25.5,6 22.2,8.5 23.5,12.5 20,9.8 16.5,12.5 17.8,8.5 14.5,6 18.5,6" fill="black"/>
        </mask>
    </defs>
    <text x="0" y="32" font-size="36" font-family="Arial Black, sans-serif" font-weight="900" fill="var(--primary)" letter-spacing="-1" mask="url(#p-icon-mask)">P</text>
</svg>
```

**Generate PNG versions:**
```bash
# Use your browser or a tool to export at these sizes:
# - 16x16px (favicon.ico)
# - 32x32px (favicon-32x32.png)
# - 512x512px (apple-touch-icon.png)
```

---

## Part 3: Star Cutout System

### 3.1 Star Formula

**For any element with border-radius R:**
```
top: R × -0.66 (negative)
right: R × 1.5
width: R × 1.5
height: R × 1.5
```

**Common values:**
- 12px radius: `top: -8px; right: 18px; width: 18px; height: 18px;`
- 8px radius: `top: -5px; right: 12px; width: 12px; height: 12px;`

### 3.2 Base Star Mixin (for reference)

```css
/* Standard star for 12px border-radius */
.star-box {
    background: white;
    padding: 30px;
    border-radius: var(--radius-large);
    position: relative;
    box-shadow: var(--shadow-low);
}

.star-box::before {
    content: '';
    position: absolute;
    top: -8px;
    right: 18px;
    width: 18px;
    height: 18px;
    background: var(--bg-light);
    clip-path: polygon(
        50% 0%, 61% 35%, 98% 35%, 68% 57%, 
        79% 91%, 50% 70%, 21% 91%, 32% 57%, 
        2% 35%, 39% 35%
    );
}
```

### 3.3 Variations

**Colored boxes:**
```css
.star-box.primary {
    background: var(--primary);
    color: white;
}

.star-box.accent {
    background: var(--accent);
    color: white;
}
```

**Bordered boxes (star shows only bottom half):**
```css
.star-box.bordered {
    border: 2px solid var(--primary);
    background: white;
    overflow: hidden; /* Clips star */
}

.star-box.bordered::before {
    background: var(--primary); /* Border color */
    top: -9px; /* Slightly higher for trim */
}
```

---

## Part 4: Component Patterns

### 4.1 Buttons

```css
.star-button {
    display: inline-block;
    padding: 14px 32px;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: var(--radius-medium);
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    position: relative;
    transition: all 0.2s;
}

.star-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
}

.star-button::before {
    content: '';
    position: absolute;
    top: -5px;
    right: 12px;
    width: 12px;
    height: 12px;
    background: var(--bg-light);
    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}

/* Secondary style */
.star-button.secondary {
    background: var(--primary);
}

/* Outline style */
.star-button.outline {
    background: white;
    color: var(--primary);
    border: 2px solid var(--primary);
    overflow: hidden;
}

.star-button.outline::before {
    background: var(--primary);
    top: -6px;
}
```

### 4.2 Status Badges

```css
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: var(--radius-medium);
    font-size: 13px;
    font-weight: 600;
    position: relative;
}

.status-badge::before {
    content: '';
    position: absolute;
    top: -5px;
    right: 12px;
    width: 12px;
    height: 12px;
    background: var(--bg-light);
    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}

.status-badge.online {
    background: var(--success);
    color: white;
}

.status-badge.api {
    background: var(--primary);
    color: white;
}

.status-badge.inperson {
    background: var(--accent);
    color: white;
}
```

### 4.3 Info Cards (Statistics)

```css
.info-card {
    background: white;
    padding: 24px;
    border-radius: var(--radius-large);
    text-align: center;
    position: relative;
    border: 2px solid var(--border);
    overflow: hidden;
}

.info-card::before {
    content: '';
    position: absolute;
    top: -8px;
    right: 18px;
    width: 18px;
    height: 18px;
    background: var(--border);
    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}

.info-value {
    font-size: 32px;
    font-weight: 900;
    color: var(--primary);
    margin-bottom: 8px;
}

.info-label {
    font-size: 13px;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 1px;
}
```

---

## Part 5: Automated Testing with Playwright

### 5.1 Install Playwright

```bash
pip install playwright --break-system-packages
playwright install
```

### 5.2 Create Test Script

**File: `tests/brand_compliance_test.py`**

```python
"""
News123 Brand Compliance Tests
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
        logo = page.locator('svg[role="img"][aria-label="News123"]')
        assert logo.count() > 0, "❌ Logo SVG not found"
        
        # Check logo color (should be primary blue)
        logo_color = page.locator('svg[role="img"] g').get_attribute('fill')
        assert 'var(--primary)' in logo_color or '#003366' in logo_color, f"❌ Logo color incorrect: {logo_color}"
        print("   ✅ Logo present and correctly colored")
        
        # Test 2: Star cutouts present on cards
        print("\n2️⃣ Testing star cutouts...")
        star_boxes = page.locator('.star-box::before')
        # Note: ::before pseudo-elements can't be directly selected, so we check the class exists
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
            button_bg = page.locator('.star-button').first.evaluate("el => getComputedStyle(el).backgroundColor")
            # Should be accent orange or primary blue
            print(f"   ✅ Found {buttons} branded buttons")
        
        # Test 6: Accessibility - Logo has proper ARIA
        print("\n6️⃣ Testing accessibility...")
        logo_aria = logo.get_attribute('aria-label')
        assert logo_aria == 'News123', f"❌ Logo aria-label incorrect: {logo_aria}"
        
        logo_title = page.locator('svg[role="img"] title').inner_text()
        assert 'News123' in logo_title, "❌ Logo <title> missing or incorrect"
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
        page.goto('http://localhost:8000/california/food-truck-permit/')
        
        print("\n🧪 Testing Permit Page Brand Compliance...")
        
        # Test breadcrumbs exist
        breadcrumb = page.locator('[itemtype*="BreadcrumbList"]')
        assert breadcrumb.count() > 0, "❌ Breadcrumbs missing"
        print("   ✅ Breadcrumbs present")
        
        # Test star boxes on page
        star_boxes = page.locator('.star-box').count()
        assert star_boxes >= 2, f"❌ Expected multiple star-box cards, found {star_boxes}"
        print(f"   ✅ Found {star_boxes} branded content cards")
        
        # Test CTA button exists
        cta = page.locator('.star-button')
        assert cta.count() > 0, "❌ No CTA button found"
        print("   ✅ CTA button present")
        
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
        page.goto('http://localhost:8000/california/food-truck-permit/')
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
```

### 5.3 Run Tests

```bash
# Start local server first
cd output
python3 -m http.server 8000 &

# Run tests
python3 tests/brand_compliance_test.py

# Stop server
kill %1
```

### 5.4 Integrate with Git Hooks

**File: `.git/hooks/pre-commit`**

```bash
#!/bin/bash
# Pre-commit hook to test brand compliance

echo "Running brand compliance tests..."

# Generate site
python3 generator.py

# Start server in background
cd output
python3 -m http.server 8000 > /dev/null 2>&1 &
SERVER_PID=$!
cd ..

# Wait for server to start
sleep 2

# Run tests
python3 tests/brand_compliance_test.py
TEST_RESULT=$?

# Kill server
kill $SERVER_PID

if [ $TEST_RESULT -ne 0 ]; then
    echo "❌ Brand compliance tests failed. Commit aborted."
    exit 1
fi

echo "✅ All tests passed. Proceeding with commit."
exit 0
```

**Make executable:**
```bash
chmod +x .git/hooks/pre-commit
```

---

## Part 6: Testing Checklist

### Before Every Commit:

- [ ] Run `python3 generator.py` to generate pages
- [ ] Preview locally: `cd output && python3 -m http.server 8000`
- [ ] Visual check: Open http://localhost:8000 in browser
- [ ] Run automated tests: `python3 tests/brand_compliance_test.py`
- [ ] Check screenshots in `tests/screenshots/` folder
- [ ] Verify no console errors (open browser DevTools)

### Visual Checklist:

**Logo:**
- [ ] Logo renders correctly in header
- [ ] Star cutout visible on "P"
- [ ] Color is primary blue (#003366)
- [ ] No distortion or stretching

**Star Cutouts:**
- [ ] All `.star-box` elements have star in top-right
- [ ] Star position follows formula (not random)
- [ ] Star size proportional to border-radius
- [ ] Bordered boxes show only bottom half of star

**Colors:**
- [ ] Primary blue used for headers, links, primary elements
- [ ] Accent orange used only for CTAs and highlights
- [ ] No random colors outside palette
- [ ] Good contrast (passes WCAG AA)

**Typography:**
- [ ] Headings use Arial Black
- [ ] Body text readable and properly sized
- [ ] Letter-spacing correct on logo and headings (-1px)

**Buttons:**
- [ ] Orange CTA buttons with star cutouts
- [ ] Hover states work (subtle lift)
- [ ] No buttons without star cutouts

**Responsive:**
- [ ] Test at 375px (mobile)
- [ ] Test at 768px (tablet)
- [ ] Test at 1920px (desktop)
- [ ] Logo scales appropriately
- [ ] Cards stack properly on mobile

---

## Part 7: Common Issues & Solutions

### Issue: Star cutout not visible

**Causes:**
- Wrong background color (star uses `var(--bg-light)`)
- Z-index issue
- Border-radius missing

**Solution:**
```css
/* Ensure parent has position: relative */
.parent {
    position: relative;
}

/* Star uses page background color */
.parent::before {
    background: var(--bg-light); /* or #f8f9fa */
}
```

### Issue: Logo colors not updating

**Cause:** SVG fill attribute hardcoded instead of using CSS variable

**Solution:**
```html
<!-- Wrong -->
<g fill="#003366">

<!-- Correct -->
<g fill="var(--primary)">
```

### Issue: Star position inconsistent

**Cause:** Not using formula, hardcoded values

**Solution:**
Always use the formula:
```
For border-radius R:
top: R × -0.66
right: R × 1.5
width/height: R × 1.5
```

### Issue: Playwright tests fail on CI

**Cause:** Server not starting before tests run

**Solution:**
Add sleep or wait for server:
```bash
python3 -m http.server 8000 &
sleep 3  # Wait for server
python3 tests/brand_compliance_test.py
```

---

## Part 8: Deployment Checklist

### Before Pushing to Production:

1. **Generate all pages:**
   ```bash
   python3 generator.py
   ```

2. **Run full test suite:**
   ```bash
   python3 tests/brand_compliance_test.py
   ```

3. **Visual regression check:**
   - Compare `tests/screenshots/*.png` with baseline
   - Approve any intentional changes
   - Reject unintended differences

4. **Manual spot checks:**
   - Homepage: http://localhost:8000
   - Permit page: http://localhost:8000/california/food-truck-permit/
   - Mobile view (DevTools)

5. **Commit:**
   ```bash
   git add .
   git commit -m "Brand implementation: [describe changes]"
   git push
   ```

6. **Cloudflare deploys automatically** (monitors GitHub)

7. **Post-deploy verification:**
   - Check https://ainews123.com
   - Verify logo renders
   - Check star cutouts
   - Test on real mobile device

---

## Part 9: Ongoing Maintenance

### Weekly:
- Review any new components for brand compliance
- Update screenshots baseline if design intentionally changed

### Monthly:
- Audit full site for consistency
- Check for any rogue colors or fonts
- Verify all new pages follow patterns

### Quarterly:
- Review brand guidelines document
- Update if new patterns emerge
- Document any approved exceptions

---

## Resources

- **Brand Guidelines:** `/BRAND_GUIDELINES.md`
- **Logo Suite:** `/news123-logo-suite.html`
- **Brand System Demo:** `/news123-brand-final.html`
- **Test Screenshots:** `/tests/screenshots/`

---

## Contact

For implementation questions or brand clarifications, refer to the Brand Guidelines document or create a GitHub issue.

**Document Version:** 1.0  
**Last Updated:** November 2024