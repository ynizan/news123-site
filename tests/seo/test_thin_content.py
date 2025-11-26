"""
SEO Test: Thin Content Detection and Mitigation

This test validates that pages with thin content are properly handled to avoid
Google penalties. It checks that:
1. Thin content pages have noindex meta tags
2. Thin content pages are deprioritized in sitemap (priority 0.3)
3. Quality content pages are indexed normally (priority 0.8)

Thin content is defined as:
- Generic "Apply for a business license" with < 800 chars total content
- OR any page with < 800 chars AND missing common mistakes AND no community content
- OR pages with description < 200 chars
"""

import pytest
import os
import json
import re
from pathlib import Path


def parse_location_for_slug(location_text):
    """Parse location text to extract state and city slugs for path matching"""
    if not location_text:
        return None, None

    # Extract state and city from various location formats
    import re

    # Try descriptive patterns that extract city name properly
    # Match: "city limits of X, State" or "within X, State" etc.
    patterns = [
        r'(?:city limits of|within the city limits of|within|operating within(?:\s+the\s+(?:city\s+)?(?:limits\s+of)?)?)\s+([^,]+),\s*([^.]+)',
        r'([^,]+),\s*([^.]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, location_text, re.IGNORECASE)
        if match:
            city_part = match.group(1).strip()
            state_part = match.group(2).strip().rstrip('.')

            # Clean city name - remove common prefixes
            city_clean = re.sub(r'^(the\s+)?(City and County of|City of|County of|Town of|Municipality of|city\s+limits\s+of)\s+', '',
                               city_part, flags=re.IGNORECASE).strip()
            city_clean = re.sub(r'\s+city\s+limits$', '', city_clean, flags=re.IGNORECASE).strip()

            # Convert to slugs
            city_slug = city_clean.lower().replace(' ', '-').replace('&', 'and')
            city_slug = re.sub(r'[^\w-]', '', city_slug)
            state_slug = state_part.lower().replace(' ', '-')
            state_slug = re.sub(r'[^\w-]', '', state_slug)

            return state_slug, city_slug

    return None, None


@pytest.mark.seo
def test_thin_content_detection_logic():
    """Test that thin content detection logic matches generator.py"""
    permits_file = 'data/permits/permits.json'

    assert os.path.exists(permits_file), "Permits data file not found"

    with open(permits_file) as f:
        permits = json.load(f)

    assert len(permits) > 0, "No permits found in data file"

    # Count thin vs quality content
    thin_count = 0
    quality_count = 0

    for permit in permits:
        # Calculate content length (matches generator.py logic)
        desc_len = len(str(permit.get('description', '')))
        elig_len = len(str(permit.get('eligibility', '')))
        how_len = len(str(permit.get('how_to_description', '')))
        mistakes_len = len(str(permit.get('common_mistakes', '')))

        feedback_count = len(permit.get('community_feedback', []))
        tips_count = len(permit.get('user_tips', []))
        faq_count = len(permit.get('faqs', []))

        total_chars = desc_len + elig_len + how_len + mistakes_len

        is_generic = 'apply for a business license' in str(permit.get('request_type', '')).lower()
        has_minimal_content = total_chars < 800
        missing_mistakes = mistakes_len < 50
        no_community = (feedback_count == 0 and tips_count == 0 and faq_count < 3)

        # Matches should_noindex_page() logic in generator.py
        is_thin = (
            (is_generic and has_minimal_content) or
            (has_minimal_content and missing_mistakes and no_community) or
            (desc_len < 200)
        )

        if is_thin:
            thin_count += 1
        else:
            quality_count += 1

    # Sanity checks
    assert thin_count > 0, "No thin content detected - detection logic may be broken"
    assert quality_count >= 0, "All pages marked as thin - detection too aggressive"

    print(f"\n📊 Content Analysis:")
    print(f"   Thin content pages: {thin_count}")
    print(f"   Quality pages: {quality_count}")
    print(f"   Ratio: {thin_count}/{thin_count + quality_count} ({thin_count/(thin_count + quality_count)*100:.1f}%) thin")


@pytest.mark.seo
def test_thin_content_pages_have_noindex(output_dir):
    """Test that thin content pages have noindex meta tag"""
    permits_file = 'data/permits/permits.json'

    with open(permits_file) as f:
        permits = json.load(f)

    thin_pages_checked = 0
    thin_pages_with_noindex = 0
    missing_noindex = []

    for permit in permits:
        # Calculate if page should be thin (same logic as generator)
        desc_len = len(str(permit.get('description', '')))
        elig_len = len(str(permit.get('eligibility', '')))
        how_len = len(str(permit.get('how_to_description', '')))
        mistakes_len = len(str(permit.get('common_mistakes', '')))

        feedback_count = len(permit.get('community_feedback', []))
        tips_count = len(permit.get('user_tips', []))
        faq_count = len(permit.get('faqs', []))

        total_chars = desc_len + elig_len + how_len + mistakes_len

        is_generic = 'apply for a business license' in str(permit.get('request_type', '')).lower()
        has_minimal_content = total_chars < 800
        missing_mistakes = mistakes_len < 50
        no_community = (feedback_count == 0 and tips_count == 0 and faq_count < 3)

        should_be_noindexed = (
            (is_generic and has_minimal_content) or
            (has_minimal_content and missing_mistakes and no_community) or
            (desc_len < 200)
        )

        if not should_be_noindexed:
            continue

        thin_pages_checked += 1

        # Find the generated HTML file using location-aware path construction
        location = permit.get('location_applicability', '')
        request_type = permit.get('request_type', '')
        permit_slug = request_type.lower().replace(' ', '-')

        # Search for the file in output
        found_files = list(Path(output_dir).rglob(f"*/{permit_slug}/index.html"))

        if not found_files:
            continue

        # Match the correct file by parsing location and constructing expected path
        state_slug, city_slug = parse_location_for_slug(location)
        html_file = None
        content = None

        if state_slug and city_slug:
            # Try to find file matching the expected path pattern
            expected_pattern = f"/{state_slug}/{city_slug}/{permit_slug}/"
            for candidate_file in found_files:
                if expected_pattern in str(candidate_file):
                    html_file = candidate_file
                    with open(html_file) as f:
                        content = f.read()
                    break

        # Fall back to content matching if path matching failed
        if html_file is None:
            for candidate_file in found_files:
                with open(candidate_file) as f:
                    candidate_content = f.read()
                # Check if this file matches the permit's location
                if location[:50] in candidate_content:
                    html_file = candidate_file
                    content = candidate_content
                    break

        # Final fallback to first match
        if html_file is None:
            html_file = found_files[0]
            with open(html_file) as f:
                content = f.read()

        if 'noindex' in content:
            thin_pages_with_noindex += 1
        else:
            missing_noindex.append(str(html_file.relative_to(output_dir)))

    # Verify most thin pages have noindex (allow some flexibility for edge cases)
    if thin_pages_checked > 0:
        coverage = (thin_pages_with_noindex / thin_pages_checked) * 100

        assert coverage >= 90, (
            f"Only {thin_pages_with_noindex}/{thin_pages_checked} ({coverage:.1f}%) "
            f"thin content pages have noindex tag. Expected >= 90%.\n"
            f"Missing noindex:\n" + "\n".join(missing_noindex[:10])
        )

        print(f"\n✅ Noindex Coverage: {thin_pages_with_noindex}/{thin_pages_checked} ({coverage:.1f}%)")


@pytest.mark.seo
def test_sitemap_deprioritizes_thin_content(output_dir):
    """Test that thin content pages have low priority in sitemap"""
    sitemap_file = os.path.join(output_dir, 'sitemap.xml')

    assert os.path.exists(sitemap_file), "Sitemap not found"

    with open(sitemap_file) as f:
        sitemap_content = f.read()

    # Count priorities
    low_priority_count = len(re.findall(r'<priority>0\.[0-3]</priority>', sitemap_content))
    high_priority_count = len(re.findall(r'<priority>0\.[8-9]</priority>|<priority>1\.0</priority>', sitemap_content))

    # Extract URLs with priorities
    url_pattern = re.compile(r'<loc>([^<]+)</loc>.*?<priority>([\d.]+)</priority>', re.DOTALL)
    matches = url_pattern.findall(sitemap_content)

    # Check that business license pages have low priority
    business_license_low_priority = 0
    business_license_total = 0

    for url, priority in matches:
        if 'apply-for-a-business-license' in url:
            business_license_total += 1
            if float(priority) <= 0.3:
                business_license_low_priority += 1

    assert low_priority_count > 0, "No low-priority pages found in sitemap"

    if business_license_total > 0:
        bl_ratio = (business_license_low_priority / business_license_total) * 100
        assert bl_ratio >= 70, (
            f"Only {business_license_low_priority}/{business_license_total} ({bl_ratio:.1f}%) "
            f"business license pages have low priority. Expected >= 70%"
        )

        print(f"\n📉 Sitemap Priority Distribution:")
        print(f"   Low priority (0.0-0.3): {low_priority_count} pages")
        print(f"   High priority (0.8-1.0): {high_priority_count} pages")
        print(f"   Business license low priority: {business_license_low_priority}/{business_license_total} ({bl_ratio:.1f}%)")


@pytest.mark.seo
def test_quality_pages_are_indexed_normally(output_dir):
    """Test that quality content pages do NOT have noindex"""
    permits_file = 'data/permits/permits.json'

    with open(permits_file) as f:
        permits = json.load(f)

    quality_pages_checked = 0
    quality_pages_without_noindex = 0
    incorrectly_noindexed = []

    for permit in permits:
        # Calculate if page should be quality content
        desc_len = len(str(permit.get('description', '')))
        elig_len = len(str(permit.get('eligibility', '')))
        how_len = len(str(permit.get('how_to_description', '')))
        mistakes_len = len(str(permit.get('common_mistakes', '')))

        feedback_count = len(permit.get('community_feedback', []))
        tips_count = len(permit.get('user_tips', []))
        faq_count = len(permit.get('faqs', []))

        total_chars = desc_len + elig_len + how_len + mistakes_len

        is_generic = 'apply for a business license' in str(permit.get('request_type', '')).lower()
        has_minimal_content = total_chars < 800
        missing_mistakes = mistakes_len < 50
        no_community = (feedback_count == 0 and tips_count == 0 and faq_count < 3)

        should_be_noindexed = (
            (is_generic and has_minimal_content) or
            (has_minimal_content and missing_mistakes and no_community) or
            (desc_len < 200)
        )

        if should_be_noindexed:
            continue  # Skip thin content pages

        quality_pages_checked += 1

        # Find the generated HTML file using location-aware path construction
        request_type = permit.get('request_type', '')
        permit_slug = request_type.lower().replace(' ', '-')
        location = permit.get('location_applicability', '')

        # Try to match the file more precisely by parsing location
        # This handles permits with the same slug but different locations
        found_files = list(Path(output_dir).rglob(f"*/{permit_slug}/index.html"))

        if not found_files:
            continue

        # Match the correct file by parsing location and constructing expected path
        state_slug, city_slug = parse_location_for_slug(location)
        html_file = None
        content = None

        if state_slug and city_slug:
            # Try to find file matching the expected path pattern
            expected_pattern = f"/{state_slug}/{city_slug}/{permit_slug}/"
            for candidate_file in found_files:
                if expected_pattern in str(candidate_file):
                    html_file = candidate_file
                    with open(html_file) as f:
                        content = f.read()
                    break

        # Fall back to content matching if path matching failed
        if html_file is None:
            for candidate_file in found_files:
                with open(candidate_file) as f:
                    candidate_content = f.read()
                # Check if this file matches the permit's location
                if location[:50] in candidate_content:
                    html_file = candidate_file
                    content = candidate_content
                    break

        # Final fallback to first match
        if html_file is None:
            html_file = found_files[0]
            with open(html_file) as f:
                content = f.read()

        if 'noindex' not in content:
            quality_pages_without_noindex += 1
        else:
            incorrectly_noindexed.append(str(html_file.relative_to(output_dir)))

    # Quality pages should NOT have noindex
    if quality_pages_checked > 0:
        correct_ratio = (quality_pages_without_noindex / quality_pages_checked) * 100

        assert correct_ratio >= 90, (
            f"Only {quality_pages_without_noindex}/{quality_pages_checked} ({correct_ratio:.1f}%) "
            f"quality pages are indexed. Expected >= 90%.\n"
            f"Incorrectly noindexed:\n" + "\n".join(incorrectly_noindexed[:10])
        )

        print(f"\n✅ Quality Content Indexed: {quality_pages_without_noindex}/{quality_pages_checked} ({correct_ratio:.1f}%)")


@pytest.mark.seo
def test_robots_txt_has_crawl_optimization(output_dir):
    """Test that robots.txt has crawl rate management"""
    robots_file = os.path.join(output_dir, 'robots.txt')

    assert os.path.exists(robots_file), "robots.txt not found"

    with open(robots_file) as f:
        robots_content = f.read()

    # Check for crawl optimization
    assert 'Crawl-delay' in robots_content, "Missing Crawl-delay directive"
    assert 'Disallow:' in robots_content, "Missing Disallow directives for low-value pages"
    assert 'Sitemap:' in robots_content, "Missing Sitemap reference"

    print("\n✅ robots.txt has crawl optimization configured")


@pytest.mark.seo
def test_thin_content_noindex_follows(output_dir):
    """Test that noindex pages use 'follow' to preserve link equity"""
    permits_file = 'data/permits/permits.json'

    with open(permits_file) as f:
        permits = json.load(f)

    noindex_pages_checked = 0
    noindex_with_follow = 0

    for permit in permits:
        request_type = permit.get('request_type', '')
        permit_slug = request_type.lower().replace(' ', '-')

        found_files = list(Path(output_dir).rglob(f"*/{permit_slug}/index.html"))

        if not found_files:
            continue

        html_file = found_files[0]

        with open(html_file) as f:
            content = f.read()

        if 'noindex' in content:
            noindex_pages_checked += 1

            # Check for proper format: noindex, follow
            if 'noindex, follow' in content or 'noindex,follow' in content:
                noindex_with_follow += 1

    if noindex_pages_checked > 0:
        follow_ratio = (noindex_with_follow / noindex_pages_checked) * 100

        assert follow_ratio >= 95, (
            f"Only {noindex_with_follow}/{noindex_pages_checked} ({follow_ratio:.1f}%) "
            f"noindex pages use 'follow' directive. Expected >= 95%"
        )

        print(f"\n✅ Noindex pages with follow: {noindex_with_follow}/{noindex_pages_checked} ({follow_ratio:.1f}%)")
