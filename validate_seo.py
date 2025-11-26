#!/usr/bin/env python3
"""
SEO Validation Script for News123
Tests deployed site at https://ainews123.com/
"""

import asyncio
import json
from playwright.async_api import async_playwright

BASE_URL = "https://ainews123.com"

async def validate_seo():
    """Run comprehensive SEO validation tests"""

    results = {
        'passed': [],
        'failed': [],
        'warnings': []
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print("=" * 80)
        print("🔍 NEWS123 SEO VALIDATION")
        print("=" * 80)
        print(f"Testing: {BASE_URL}\n")

        # Test 1: Homepage loads
        print("📄 Test 1: Homepage Accessibility")
        try:
            response = await page.goto(BASE_URL, wait_until="networkidle")
            if response.status == 200:
                results['passed'].append("✅ Homepage loads successfully (200 OK)")
                print("   ✅ Homepage loads successfully (200 OK)")
            else:
                results['failed'].append(f"❌ Homepage returned status {response.status}")
                print(f"   ❌ Homepage returned status {response.status}")
        except Exception as e:
            results['failed'].append(f"❌ Homepage failed to load: {str(e)}")
            print(f"   ❌ Homepage failed to load: {str(e)}")

        # Test 2: Hierarchical URL Structure
        print("\n📄 Test 2: URL Structure - Hierarchical Format")
        permit_url = f"{BASE_URL}/california/food-truck-operating-permit/"
        try:
            response = await page.goto(permit_url, wait_until="networkidle")
            if response.status == 200:
                results['passed'].append(f"✅ Hierarchical URL works: {permit_url}")
                print(f"   ✅ Hierarchical URL works: {permit_url}")
            else:
                results['failed'].append(f"❌ Permit page returned {response.status}")
                print(f"   ❌ Permit page returned {response.status}")
        except Exception as e:
            results['failed'].append(f"❌ Permit page failed: {str(e)}")
            print(f"   ❌ Permit page failed: {str(e)}")

        # Test 3: Canonical Tag
        print("\n📄 Test 3: Canonical Tag Validation")
        try:
            canonical = await page.query_selector('link[rel="canonical"]')
            if canonical:
                href = await canonical.get_attribute('href')
                expected = f"{BASE_URL}/california/food-truck-operating-permit/"
                if href == expected:
                    results['passed'].append(f"✅ Canonical tag correct: {href}")
                    print(f"   ✅ Canonical tag correct: {href}")
                else:
                    results['failed'].append(f"❌ Canonical mismatch. Got: {href}, Expected: {expected}")
                    print(f"   ❌ Canonical mismatch")
                    print(f"      Got: {href}")
                    print(f"      Expected: {expected}")
            else:
                results['failed'].append("❌ No canonical tag found")
                print("   ❌ No canonical tag found")
        except Exception as e:
            results['failed'].append(f"❌ Canonical check failed: {str(e)}")
            print(f"   ❌ Canonical check failed: {str(e)}")

        # Test 4: Meta Description
        print("\n📄 Test 4: Meta Description Quality")
        try:
            meta_desc = await page.query_selector('meta[name="description"]')
            if meta_desc:
                content = await meta_desc.get_attribute('content')
                if content and len(content) > 100 and len(content) < 160:
                    results['passed'].append(f"✅ Meta description optimal length: {len(content)} chars")
                    print(f"   ✅ Meta description optimal length: {len(content)} chars")
                    print(f"   📝 Content: {content[:80]}...")
                elif content:
                    results['warnings'].append(f"⚠️  Meta description suboptimal: {len(content)} chars")
                    print(f"   ⚠️  Meta description length: {len(content)} chars (ideal: 120-160)")
                else:
                    results['failed'].append("❌ Meta description empty")
                    print("   ❌ Meta description empty")
            else:
                results['failed'].append("❌ No meta description found")
                print("   ❌ No meta description found")
        except Exception as e:
            results['failed'].append(f"❌ Meta description check failed: {str(e)}")
            print(f"   ❌ Meta description check failed: {str(e)}")

        # Test 5: H1 Tag
        print("\n📄 Test 5: Heading Structure")
        try:
            h1_elements = await page.query_selector_all('h1')
            if len(h1_elements) == 1:
                h1_text = await h1_elements[0].inner_text()
                results['passed'].append(f"✅ Exactly one H1 found: '{h1_text}'")
                print(f"   ✅ Exactly one H1 found: '{h1_text}'")
            elif len(h1_elements) == 0:
                results['failed'].append("❌ No H1 tag found")
                print("   ❌ No H1 tag found")
            else:
                results['warnings'].append(f"⚠️  Multiple H1 tags found: {len(h1_elements)}")
                print(f"   ⚠️  Multiple H1 tags found: {len(h1_elements)}")
        except Exception as e:
            results['failed'].append(f"❌ H1 check failed: {str(e)}")
            print(f"   ❌ H1 check failed: {str(e)}")

        # Test 6: Above-the-Fold Summary
        print("\n📄 Test 6: Above-the-Fold Summary Section")
        try:
            summary = await page.query_selector('.bg-blue-50')
            if summary:
                text = await summary.inner_text()
                if len(text) > 50:
                    results['passed'].append(f"✅ Above-the-fold summary present: {len(text)} chars")
                    print(f"   ✅ Above-the-fold summary present: {len(text)} chars")
                else:
                    results['warnings'].append("⚠️  Summary too short")
                    print("   ⚠️  Summary too short")
            else:
                results['failed'].append("❌ No above-the-fold summary found")
                print("   ❌ No above-the-fold summary found")
        except Exception as e:
            results['warnings'].append(f"⚠️  Summary check failed: {str(e)}")
            print(f"   ⚠️  Summary check failed: {str(e)}")

        # Test 7: FAQ Section
        print("\n📄 Test 7: FAQ Section Presence")
        try:
            faq_heading = await page.query_selector('h2:has-text("Frequently Asked Questions")')
            if faq_heading:
                # Count FAQ items
                faq_items = await page.query_selector_all('h3')
                faq_count = len([item for item in faq_items])
                if faq_count >= 5:
                    results['passed'].append(f"✅ FAQ section with {faq_count} questions")
                    print(f"   ✅ FAQ section with {faq_count} questions")
                else:
                    results['warnings'].append(f"⚠️  Only {faq_count} FAQ items")
                    print(f"   ⚠️  Only {faq_count} FAQ items")
            else:
                results['failed'].append("❌ FAQ section not found")
                print("   ❌ FAQ section not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  FAQ check failed: {str(e)}")
            print(f"   ⚠️  FAQ check failed: {str(e)}")

        # Test 8: FAQPage Schema
        print("\n📄 Test 8: FAQPage Structured Data")
        try:
            scripts = await page.query_selector_all('script[type="application/ld+json"]')
            faq_schema_found = False
            for script in scripts:
                content = await script.inner_text()
                try:
                    data = json.loads(content)
                    if data.get('@type') == 'FAQPage':
                        faq_schema_found = True
                        questions = data.get('mainEntity', [])
                        results['passed'].append(f"✅ FAQPage schema with {len(questions)} questions")
                        print(f"   ✅ FAQPage schema with {len(questions)} questions")
                        break
                except:
                    continue

            if not faq_schema_found:
                results['failed'].append("❌ FAQPage schema not found")
                print("   ❌ FAQPage schema not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  Schema check failed: {str(e)}")
            print(f"   ⚠️  Schema check failed: {str(e)}")

        # Test 9: Community Feedback Section
        print("\n📄 Test 9: Community Feedback Section")
        try:
            feedback_heading = await page.query_selector('h2:has-text("What People Are Saying")')
            if feedback_heading:
                results['passed'].append("✅ Community feedback section present")
                print("   ✅ Community feedback section present")
            else:
                results['warnings'].append("⚠️  Community feedback section not found")
                print("   ⚠️  Community feedback section not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  Feedback check failed: {str(e)}")
            print(f"   ⚠️  Feedback check failed: {str(e)}")

        # Test 10: User Tips Section
        print("\n📄 Test 10: User Tips Section")
        try:
            tips_heading = await page.query_selector('h2:has-text("Tips from the Community")')
            if tips_heading:
                results['passed'].append("✅ User tips section present")
                print("   ✅ User tips section present")
            else:
                results['warnings'].append("⚠️  User tips section not found")
                print("   ⚠️  User tips section not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  Tips check failed: {str(e)}")
            print(f"   ⚠️  Tips check failed: {str(e)}")

        # Test 11: Common Mistakes Section
        print("\n📄 Test 11: Common Mistakes Section")
        try:
            mistakes_heading = await page.query_selector('h2:has-text("Common Mistakes")')
            if mistakes_heading:
                results['passed'].append("✅ Common mistakes section present")
                print("   ✅ Common mistakes section present")
            else:
                results['warnings'].append("⚠️  Common mistakes section not found")
                print("   ⚠️  Common mistakes section not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  Mistakes check failed: {str(e)}")
            print(f"   ⚠️  Mistakes check failed: {str(e)}")

        # Test 12: Agency Contact Information
        print("\n📄 Test 12: Agency Contact Information")
        try:
            contact_heading = await page.query_selector('h3:has-text("Contact Information")')
            if contact_heading:
                # Check for phone, email, address
                phone = await page.query_selector('a[href^="tel:"]')
                email = await page.query_selector('a[href^="mailto:"]')

                contact_items = []
                if phone:
                    contact_items.append("phone")
                if email:
                    contact_items.append("email")

                if contact_items:
                    results['passed'].append(f"✅ Contact info present: {', '.join(contact_items)}")
                    print(f"   ✅ Contact info present: {', '.join(contact_items)}")
                else:
                    results['warnings'].append("⚠️  Contact section exists but missing details")
                    print("   ⚠️  Contact section exists but missing details")
            else:
                results['warnings'].append("⚠️  Contact information section not found")
                print("   ⚠️  Contact information section not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  Contact check failed: {str(e)}")
            print(f"   ⚠️  Contact check failed: {str(e)}")

        # Test 13: Willingness to Pay Widget
        print("\n📄 Test 13: Willingness to Pay Widget")
        try:
            wtp_heading = await page.query_selector('h3:has-text("Value of Automation")')
            wtp_slider = await page.query_selector('#wtpSlider')
            if wtp_heading and wtp_slider:
                results['passed'].append("✅ WTP widget present with slider")
                print("   ✅ WTP widget present with slider")
            elif wtp_heading:
                results['warnings'].append("⚠️  WTP heading found but slider missing")
                print("   ⚠️  WTP heading found but slider missing")
            else:
                results['warnings'].append("⚠️  WTP widget not found")
                print("   ⚠️  WTP widget not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  WTP check failed: {str(e)}")
            print(f"   ⚠️  WTP check failed: {str(e)}")

        # Test 14: Jurisdiction Hub Page
        print("\n📄 Test 14: Jurisdiction Hub Page")
        hub_url = f"{BASE_URL}/california/"
        try:
            response = await page.goto(hub_url, wait_until="networkidle")
            if response.status == 200:
                # Check for statistics
                stats_present = await page.query_selector('text=/Total Permits/')
                if stats_present:
                    results['passed'].append(f"✅ Hub page exists with statistics: {hub_url}")
                    print(f"   ✅ Hub page exists with statistics: {hub_url}")
                else:
                    results['warnings'].append("⚠️  Hub page exists but missing statistics")
                    print("   ⚠️  Hub page exists but missing statistics")
            else:
                results['failed'].append(f"❌ Hub page returned {response.status}")
                print(f"   ❌ Hub page returned {response.status}")
        except Exception as e:
            results['failed'].append(f"❌ Hub page check failed: {str(e)}")
            print(f"   ❌ Hub page check failed: {str(e)}")

        # Test 15: Breadcrumbs
        print("\n📄 Test 15: Breadcrumb Navigation")
        await page.goto(permit_url, wait_until="networkidle")
        try:
            breadcrumbs = await page.query_selector('nav[aria-label="Breadcrumb"]')
            if breadcrumbs:
                # Check for working links
                links = await breadcrumbs.query_selector_all('a')
                if len(links) >= 2:
                    results['passed'].append(f"✅ Breadcrumbs present with {len(links)} links")
                    print(f"   ✅ Breadcrumbs present with {len(links)} links")
                else:
                    results['warnings'].append("⚠️  Breadcrumbs incomplete")
                    print("   ⚠️  Breadcrumbs incomplete")
            else:
                results['failed'].append("❌ Breadcrumbs not found")
                print("   ❌ Breadcrumbs not found")
        except Exception as e:
            results['warnings'].append(f"⚠️  Breadcrumb check failed: {str(e)}")
            print(f"   ⚠️  Breadcrumb check failed: {str(e)}")

        # Test 16: Word Count (Visible Text)
        print("\n📄 Test 16: Content Depth (Word Count)")
        try:
            # Get all text content
            body = await page.query_selector('body')
            text = await body.inner_text()
            words = text.split()
            word_count = len(words)

            if word_count >= 800:
                results['passed'].append(f"✅ Excellent content depth: {word_count} words")
                print(f"   ✅ Excellent content depth: {word_count} words")
            elif word_count >= 500:
                results['warnings'].append(f"⚠️  Moderate content: {word_count} words (target: 800+)")
                print(f"   ⚠️  Moderate content: {word_count} words (target: 800+)")
            else:
                results['failed'].append(f"❌ Thin content: {word_count} words")
                print(f"   ❌ Thin content: {word_count} words")
        except Exception as e:
            results['warnings'].append(f"⚠️  Word count check failed: {str(e)}")
            print(f"   ⚠️  Word count check failed: {str(e)}")

        # Test 17: Sitemap
        print("\n📄 Test 17: Sitemap Accessibility")
        sitemap_url = f"{BASE_URL}/sitemap.xml"
        try:
            response = await page.goto(sitemap_url, wait_until="networkidle")
            if response.status == 200:
                content = await page.content()
                if '<urlset' in content and permit_url in content:
                    results['passed'].append(f"✅ Sitemap accessible and contains permit URLs")
                    print(f"   ✅ Sitemap accessible and contains permit URLs")
                else:
                    results['warnings'].append("⚠️  Sitemap exists but may be incomplete")
                    print("   ⚠️  Sitemap exists but may be incomplete")
            else:
                results['failed'].append(f"❌ Sitemap returned {response.status}")
                print(f"   ❌ Sitemap returned {response.status}")
        except Exception as e:
            results['failed'].append(f"❌ Sitemap check failed: {str(e)}")
            print(f"   ❌ Sitemap check failed: {str(e)}")

        # Test 18: Mobile Responsiveness
        print("\n📄 Test 18: Mobile Responsiveness")
        await page.goto(permit_url, wait_until="networkidle")
        try:
            viewport_meta = await page.query_selector('meta[name="viewport"]')
            if viewport_meta:
                content = await viewport_meta.get_attribute('content')
                if 'width=device-width' in content:
                    results['passed'].append("✅ Mobile viewport meta tag present")
                    print("   ✅ Mobile viewport meta tag present")
                else:
                    results['warnings'].append("⚠️  Viewport meta tag missing width=device-width")
                    print("   ⚠️  Viewport meta tag missing width=device-width")
            else:
                results['failed'].append("❌ No viewport meta tag")
                print("   ❌ No viewport meta tag")
        except Exception as e:
            results['warnings'].append(f"⚠️  Mobile check failed: {str(e)}")
            print(f"   ⚠️  Mobile check failed: {str(e)}")

        await browser.close()

    # Print Summary
    print("\n" + "=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⚠️  Warnings: {len(results['warnings'])}")
    print()

    if results['failed']:
        print("❌ FAILED TESTS:")
        for fail in results['failed']:
            print(f"   {fail}")
        print()

    if results['warnings']:
        print("⚠️  WARNINGS:")
        for warning in results['warnings']:
            print(f"   {warning}")
        print()

    # Overall result
    if len(results['failed']) == 0:
        print("🎉 ALL CRITICAL TESTS PASSED!")
        if len(results['warnings']) == 0:
            print("✨ PERFECT SCORE - No warnings!")
        else:
            print(f"💡 {len(results['warnings'])} minor improvements suggested")
    else:
        print(f"⚠️  {len(results['failed'])} critical issues need attention")

    print("=" * 80)

    return len(results['failed']) == 0

if __name__ == '__main__':
    success = asyncio.run(validate_seo())
    exit(0 if success else 1)
