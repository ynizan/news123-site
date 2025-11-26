#!/usr/bin/env python3
"""
Script to capture screenshots of the generated HTML page
"""

from playwright.sync_api import sync_playwright
import os

def screenshot_page(html_file, output_screenshot):
    """Take a screenshot of the HTML file"""

    # Get absolute path to the HTML file
    abs_path = os.path.abspath(html_file)
    file_url = f"file://{abs_path}"

    print(f"📸 Loading: {file_url}")

    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Navigate to the file
        page.goto(file_url)

        # Wait for page to load
        page.wait_for_load_state('networkidle')

        # Take full page screenshot
        page.screenshot(path=output_screenshot, full_page=True)

        print(f"✓ Screenshot saved: {output_screenshot}")

        browser.close()

if __name__ == '__main__':
    # Screenshot the generated California Food Truck Permit page
    html_file = 'output/california/california-food-truck-permit.html'
    output_screenshot = 'output/california-food-truck-permit-screenshot.png'

    screenshot_page(html_file, output_screenshot)
    print(f"\n✅ Done! You can view the screenshot at: {output_screenshot}")
