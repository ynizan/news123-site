#!/usr/bin/env python3
"""
Simple script to view the generated HTML page in a browser
"""

from playwright.sync_api import sync_playwright
import os

def view_page(html_file):
    """Open the HTML file in a browser"""

    # Get absolute path to the HTML file
    abs_path = os.path.abspath(html_file)
    file_url = f"file://{abs_path}"

    print(f"Opening: {file_url}")

    with sync_playwright() as p:
        # Launch browser in headed mode (visible)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the file
        page.goto(file_url)

        # Keep browser open
        print("\nBrowser is open. Press Enter to close...")
        input()

        browser.close()

if __name__ == '__main__':
    # View the generated California Food Truck Permit page
    html_file = 'output/california/california-food-truck-permit.html'
    view_page(html_file)
