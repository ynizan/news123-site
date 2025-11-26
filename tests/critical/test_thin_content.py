"""
CRITICAL TEST: Thin Content SEO Protection

This critical test ensures that thin content pages are properly protected from
Google penalties. It runs on every commit and merge to catch regressions.

Failures indicate:
- Thin content pages are being indexed (risk of penalty)
- Quality pages are being noindexed (loss of traffic)
- Sitemap priorities are misconfigured (wasted crawl budget)
"""

import pytest
import os
import json
import re
from pathlib import Path


@pytest.mark.critical
def test_thin_content_has_noindex_protection(output_dir):
    """CRITICAL: Verify thin content pages have noindex tag"""
    permits_file = 'data/permits/permits.json'

    if not os.path.exists(permits_file):
        pytest.skip("Permits data file not found")

    with open(permits_file) as f:
        permits = json.load(f)

    # Sample check: Look for business license pages
    business_license_pages = [
        p for p in permits
        if 'apply for a business license' in p.get('request_type', '').lower()
    ]

    if not business_license_pages:
        pytest.skip("No business license pages found")

    # Check first 5 business license pages (representative sample)
    pages_checked = 0
    pages_with_noindex = 0
    failures = []

    for permit in business_license_pages[:5]:
        request_type = permit.get('request_type', '')
        permit_slug = 'apply-for-a-business-license'

        found_files = list(Path(output_dir).rglob(f"*/{permit_slug}/index.html"))

        if not found_files:
            continue

        html_file = found_files[0]
        pages_checked += 1

        with open(html_file) as f:
            content = f.read()

        if 'noindex' in content:
            pages_with_noindex += 1
        else:
            failures.append(str(html_file.relative_to(output_dir)))

    if pages_checked == 0:
        pytest.skip("No business license pages found in output")

    # Require 100% of sampled pages to have noindex
    assert pages_with_noindex == pages_checked, (
        f"❌ CRITICAL: {pages_checked - pages_with_noindex}/{pages_checked} "
        f"thin content pages are missing noindex tag!\n"
        f"This exposes the site to thin content penalties.\n"
        f"Failed pages:\n" + "\n".join(failures)
    )


@pytest.mark.critical
def test_sitemap_has_proper_priorities(output_dir):
    """CRITICAL: Verify each page's sitemap priority matches its content quality"""
    permits_file = 'data/permits/permits.json'
    sitemap_file = os.path.join(output_dir, 'sitemap.xml')

    if not os.path.exists(permits_file):
        pytest.skip("Permits data file not found")

    if not os.path.exists(sitemap_file):
        pytest.fail("Sitemap not generated")

    # Load permits data
    with open(permits_file) as f:
        permits = json.load(f)

    # Parse sitemap
    with open(sitemap_file) as f:
        sitemap_content = f.read()

    # Extract all business license URLs with priorities
    url_pattern = re.compile(r'<loc>([^<]+apply-for-a-business-license[^<]*)</loc>.*?<priority>([\d.]+)</priority>', re.DOTALL)
    matches = url_pattern.findall(sitemap_content)

    if not matches:
        pytest.skip("No business license pages found in sitemap")

    # Check each page individually
    mismatches = []
    checked_count = 0

    for url, actual_priority in matches[:15]:  # Sample first 15 for speed
        actual_priority = float(actual_priority)

        # Find matching permit in data
        # URL format: https://ainews123.com/{state}/{city}/apply-for-a-business-license/
        # or: https://ainews123.com/{state}/apply-for-a-business-license/
        url_parts = url.rstrip('/').split('/')

        # Need at least: https, '', ainews123.com, state, permit
        if len(url_parts) < 5:
            continue

        # Extract components
        if len(url_parts) == 5:
            # State-level: https://ainews123.com/{state}/{permit}/
            state_slug = url_parts[3]
            city_slug = None
        else:
            # City-level: https://ainews123.com/{state}/{city}/{permit}/
            state_slug = url_parts[3]
            city_slug = url_parts[4]

        # Find permit by matching location
        matching_permit = None
        for permit in permits:
            if 'apply for a business license' not in permit.get('request_type', '').lower():
                continue

            location = permit.get('location_applicability', '')
            if not location:
                continue

            # Check if location matches the URL state/city
            location_lower = location.lower()

            # Simple matching: check if state and city names appear in location
            state_name = state_slug.replace('-', ' ')
            if city_slug:
                city_name = city_slug.replace('-', ' ')
                # For city-level permits, check both state and city match
                if state_name in location_lower and city_name in location_lower:
                    matching_permit = permit
                    break
            else:
                # For state-level permits, check state matches
                if state_name in location_lower:
                    matching_permit = permit
                    break

        if not matching_permit:
            continue

        checked_count += 1

        # Calculate expected priority using same logic as generator.py
        desc_len = len(str(matching_permit.get('description', '')))
        elig_len = len(str(matching_permit.get('eligibility', '')))
        how_to_len = len(str(matching_permit.get('how_to_description', '')))
        mistakes_len = len(str(matching_permit.get('common_mistakes', '')))

        feedback_count = len(matching_permit.get('community_feedback', []))
        tips_count = len(matching_permit.get('user_tips', []))
        faq_count = len(matching_permit.get('faqs', []))

        total_content = desc_len + elig_len + how_to_len + mistakes_len

        is_generic = True  # It's a business license page
        has_minimal_content = total_content < 800
        missing_mistakes = mistakes_len < 50
        no_community = (feedback_count == 0 and tips_count == 0 and faq_count < 3)

        should_noindex = (
            (is_generic and has_minimal_content) or
            (has_minimal_content and missing_mistakes and no_community) or
            (desc_len < 200)
        )

        expected_priority = 0.3 if should_noindex else 0.8

        # Check if priority matches expectation
        if abs(actual_priority - expected_priority) > 0.01:  # Allow small floating point differences
            content_type = "thin" if should_noindex else "quality"
            location_desc = f"{state_slug}/{city_slug}" if city_slug else state_slug
            mismatches.append(
                f"  • {location_desc}: {content_type} content ({total_content} chars) "
                f"but priority is {actual_priority} (expected {expected_priority})"
            )

    if checked_count == 0:
        pytest.skip("Could not match any sitemap URLs to permit data")

    assert len(mismatches) == 0, (
        f"❌ CRITICAL: {len(mismatches)}/{checked_count} pages have incorrect sitemap priorities!\n"
        f"Priorities must match content quality:\n"
        f"  - Thin content (< 800 chars) → priority 0.3\n"
        f"  - Quality content (≥ 800 chars) → priority 0.8\n\n"
        f"Mismatches:\n" + "\n".join(mismatches)
    )


@pytest.mark.critical
def test_noindex_uses_follow_directive(output_dir):
    """CRITICAL: Verify noindex pages preserve link equity with 'follow'"""
    # Find first noindex page
    for html_file in Path(output_dir).rglob("*/apply-for-a-business-license/index.html"):
        with open(html_file) as f:
            content = f.read()

        if 'noindex' in content:
            # Verify it uses "follow" directive
            assert 'noindex, follow' in content or 'noindex,follow' in content, (
                f"❌ CRITICAL: Noindex page doesn't use 'follow' directive!\n"
                f"File: {html_file.relative_to(output_dir)}\n"
                f"This breaks internal link equity flow."
            )
            # Only need to check one page
            return

    pytest.skip("No noindex pages found to test")


@pytest.mark.critical
def test_noindex_matches_sitemap_priority(output_dir):
    """CRITICAL: Verify noindex tags in HTML match sitemap priorities"""
    sitemap_file = os.path.join(output_dir, 'sitemap.xml')

    if not os.path.exists(sitemap_file):
        pytest.fail("Sitemap not found")

    # Parse sitemap to get URLs and priorities
    with open(sitemap_file) as f:
        sitemap_content = f.read()

    url_pattern = re.compile(r'<loc>([^<]+)</loc>.*?<priority>([\d.]+)</priority>', re.DOTALL)
    url_priorities = {}
    for url, priority in url_pattern.findall(sitemap_content):
        url_priorities[url] = float(priority)

    # Check sample of business license pages
    mismatches = []
    checked = 0

    for html_file in Path(output_dir).rglob("*/apply-for-a-business-license/index.html"):
        # Get URL from file path
        rel_path = html_file.relative_to(output_dir)
        url_path = '/' + str(rel_path.parent) + '/'
        full_url = f"https://ainews123.com{url_path}"

        if full_url not in url_priorities:
            continue

        priority = url_priorities[full_url]

        # Read HTML
        with open(html_file) as f:
            html_content = f.read()

        has_noindex = 'noindex' in html_content

        # Validate consistency
        if priority <= 0.5:
            # Thin content - should have noindex
            if not has_noindex:
                mismatches.append(
                    f"  • {url_path}: priority {priority} (thin) but NO noindex tag"
                )
        else:
            # Quality content - should NOT have noindex
            if has_noindex:
                mismatches.append(
                    f"  • {url_path}: priority {priority} (quality) but HAS noindex tag"
                )

        checked += 1
        if checked >= 15:  # Sample size
            break

    if checked == 0:
        pytest.skip("No business license pages found to check")

    assert len(mismatches) == 0, (
        f"❌ CRITICAL: {len(mismatches)}/{checked} pages have inconsistent noindex/priority!\n"
        f"Rules:\n"
        f"  - Priority ≤ 0.5 (thin) → MUST have noindex tag\n"
        f"  - Priority > 0.5 (quality) → MUST NOT have noindex tag\n\n"
        f"Mismatches:\n" + "\n".join(mismatches)
    )


@pytest.mark.critical
def test_robots_txt_exists_with_sitemap(output_dir):
    """CRITICAL: Verify robots.txt exists and references sitemap"""
    robots_file = os.path.join(output_dir, 'robots.txt')

    assert os.path.exists(robots_file), "❌ CRITICAL: robots.txt not found!"

    with open(robots_file) as f:
        robots_content = f.read()

    assert 'Sitemap:' in robots_content, (
        "❌ CRITICAL: robots.txt missing Sitemap reference!\n"
        "Search engines won't discover the sitemap."
    )

    assert 'https://ainews123.com/sitemap.xml' in robots_content, (
        "❌ CRITICAL: robots.txt has incorrect sitemap URL!"
    )
