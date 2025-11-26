#!/usr/bin/env python3
"""
Link Validation Script for PermitIndex
Can validate links in local build OR production site

Usage:
    python3 validate_links.py                    # Validate local build
    python3 validate_links.py --production       # Validate production site
    python3 validate_links.py --both             # Validate both
"""

import os
import re
import sys
import asyncio
from pathlib import Path
from urllib.parse import urljoin, urlparse
from collections import defaultdict

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Production validation disabled.")
    print("   Install with: pip3 install playwright && playwright install chromium")

# Configuration
OUTPUT_DIR = "output"
BASE_URL = "https://permitindex.com"


def extract_links_from_html(html_content, base_path=""):
    """Extract all internal links from HTML content"""
    links = set()

    # Find all href attributes
    href_pattern = r'href=["\']([^"\']+)["\']'
    matches = re.findall(href_pattern, html_content)

    for match in matches:
        # Skip external links, anchors, and special protocols
        if match.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:')):
            continue

        # Normalize the link
        if match.startswith('/'):
            links.add(match)
        else:
            # Relative link - resolve it
            if base_path:
                resolved = urljoin(base_path, match)
                parsed = urlparse(resolved)
                links.add(parsed.path)

    return links


def validate_local_links():
    """Validate all internal links in the local build"""
    print("=" * 80)
    print("🔍 LOCAL BUILD LINK VALIDATION")
    print("=" * 80)
    print(f"Checking links in: {OUTPUT_DIR}/\n")

    output_path = Path(OUTPUT_DIR)
    if not output_path.exists():
        print(f"❌ Output directory not found: {OUTPUT_DIR}")
        print("   Run generator.py first to build the site")
        return False

    # Collect all HTML files and their links
    html_files = list(output_path.glob("**/*.html"))
    print(f"📄 Found {len(html_files)} HTML files\n")

    all_links = defaultdict(set)  # file -> set of links
    broken_links = defaultdict(list)  # file -> list of broken links
    all_found_links = set()

    # Step 1: Extract all links from all files
    print("📊 Extracting links...")
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get relative path from output dir for reporting
        rel_path = html_file.relative_to(output_path)

        # Extract links
        links = extract_links_from_html(content, f"/{rel_path.parent}/")
        all_links[str(rel_path)] = links
        all_found_links.update(links)

    print(f"   Found {len(all_found_links)} unique internal links\n")

    # Step 2: Validate each link
    print("🔍 Validating links...")
    total_links_checked = 0

    for source_file, links in all_links.items():
        for link in links:
            total_links_checked += 1

            # Normalize link to file path
            if link == '/':
                file_path = output_path / "index.html"
            elif link.endswith('/'):
                file_path = output_path / link.strip('/') / "index.html"
            else:
                # Could be a file with extension or without
                file_path = output_path / link.strip('/')
                if not file_path.exists():
                    # Try with .html extension
                    file_path = output_path / (link.strip('/') + '.html')
                if not file_path.exists():
                    # Try as directory with index.html
                    file_path = output_path / link.strip('/') / 'index.html'

            # Check if file exists
            if not file_path.exists():
                broken_links[source_file].append(link)

    print(f"   Checked {total_links_checked} total link references\n")

    # Step 3: Report results
    print("=" * 80)
    print("📊 VALIDATION RESULTS")
    print("=" * 80)

    if not broken_links:
        print("✅ ALL LINKS VALID!")
        print(f"   Checked {total_links_checked} links across {len(html_files)} files")
        print("   No broken links found")
        return True
    else:
        print(f"❌ FOUND {sum(len(v) for v in broken_links.values())} BROKEN LINKS")
        print()

        for source_file, links in sorted(broken_links.items()):
            print(f"📄 {source_file}")
            for link in sorted(links):
                print(f"   ❌ {link}")
            print()

        return False


async def validate_production_links():
    """Validate links on production site using Playwright"""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Cannot validate production - Playwright not installed")
        return False

    print("=" * 80)
    print("🌐 PRODUCTION SITE LINK VALIDATION")
    print("=" * 80)
    print(f"Testing: {BASE_URL}\n")

    broken_links = defaultdict(list)  # page -> list of broken links
    visited_pages = set()
    pages_to_visit = ['/']
    link_to_status = {}  # link -> status code

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print("🔍 Crawling site and checking links...")

        while pages_to_visit and len(visited_pages) < 20:  # Limit to 20 pages for now
            current_path = pages_to_visit.pop(0)

            if current_path in visited_pages:
                continue

            visited_pages.add(current_path)
            url = urljoin(BASE_URL, current_path)

            try:
                print(f"   Checking: {current_path}")
                response = await page.goto(url, wait_until="networkidle", timeout=10000)

                if response.status != 200:
                    print(f"   ⚠️  Page returned {response.status}")
                    continue

                # Extract all links from this page
                links = await page.evaluate("""
                    () => {
                        const links = Array.from(document.querySelectorAll('a[href]'));
                        return links.map(a => a.href);
                    }
                """)

                # Check each link
                for link in links:
                    parsed = urlparse(link)

                    # Only check internal links
                    if parsed.netloc and parsed.netloc not in ['permitindex.com', 'www.permitindex.com']:
                        continue

                    link_path = parsed.path

                    # Skip if already checked
                    if link_path in link_to_status:
                        if link_to_status[link_path] != 200:
                            broken_links[current_path].append(link_path)
                        continue

                    # Check if link works
                    try:
                        check_response = await page.goto(urljoin(BASE_URL, link_path),
                                                        wait_until="domcontentloaded",
                                                        timeout=5000)
                        link_to_status[link_path] = check_response.status

                        if check_response.status != 200:
                            broken_links[current_path].append(link_path)
                        else:
                            # Add to pages to visit if it's an internal page
                            if link_path not in visited_pages and link_path not in pages_to_visit:
                                if not link_path.endswith(('.xml', '.txt', '.json')):
                                    pages_to_visit.append(link_path)
                    except Exception as e:
                        broken_links[current_path].append(link_path)
                        link_to_status[link_path] = 0

            except Exception as e:
                print(f"   ❌ Error loading {current_path}: {str(e)}")

        await browser.close()

    # Report results
    print()
    print("=" * 80)
    print("📊 PRODUCTION VALIDATION RESULTS")
    print("=" * 80)
    print(f"Visited {len(visited_pages)} pages")
    print(f"Checked {len(link_to_status)} unique links")
    print()

    if not broken_links:
        print("✅ ALL LINKS VALID!")
        print("   No broken links found on production site")
        return True
    else:
        total_broken = sum(len(v) for v in broken_links.values())
        print(f"❌ FOUND {total_broken} BROKEN LINKS")
        print()

        for page, links in sorted(broken_links.items()):
            print(f"📄 {page}")
            for link in sorted(set(links)):
                status = link_to_status.get(link, 'unknown')
                print(f"   ❌ {link} (status: {status})")
            print()

        return False


def main():
    """Main entry point"""
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    mode = args[0] if args else '--local'

    results = []

    if mode in ['--local', '--both']:
        print()
        local_ok = validate_local_links()
        results.append(('Local Build', local_ok))

    if mode in ['--production', '--both']:
        if PLAYWRIGHT_AVAILABLE:
            print("\n" if mode == '--both' else "")
            prod_ok = asyncio.run(validate_production_links())
            results.append(('Production Site', prod_ok))
        else:
            print("\n❌ Skipping production validation (Playwright not available)")
            results.append(('Production Site', None))

    # Final summary
    if results:
        print()
        print("=" * 80)
        print("📊 FINAL SUMMARY")
        print("=" * 80)
        for name, status in results:
            if status is True:
                print(f"✅ {name}: All links valid")
            elif status is False:
                print(f"❌ {name}: Broken links found")
            else:
                print(f"⚠️  {name}: Not checked")
        print("=" * 80)

        # Exit with error if any validation failed
        if any(status is False for name, status in results):
            sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
