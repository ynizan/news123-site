#!/usr/bin/env python3
"""
Generate official PNG logo variations for PermitIndex
Based on the official brand assets
Creates 6 versions total:
- Icon (Square P): primary, white, black
- Horizontal: primary, white, black
Outputs to ~/Downloads/permitindex-logos/
"""

from playwright.sync_api import sync_playwright
import os

# Output to user's Downloads folder, outside the project
OUTPUT_DIR = os.path.expanduser('~/Downloads/permitindex-logos')

# Logo variations
LOGO_CONFIGS = [
    # SQUARE ICON LOGOS
    {
        'name': 'permitindex-icon-primary.png',
        'type': 'icon',
        'color': '#003366',
        'bg': 'transparent',
        'desc': 'Square icon - Primary blue'
    },
    {
        'name': 'permitindex-icon-white.png',
        'type': 'icon',
        'color': '#FFFFFF',
        'bg': '#003366',
        'desc': 'Square icon - White on navy'
    },
    {
        'name': 'permitindex-icon-black.png',
        'type': 'icon',
        'color': '#000000',
        'bg': 'transparent',
        'desc': 'Square icon - Black'
    },
    # HORIZONTAL LOGOS
    {
        'name': 'permitindex-horizontal-primary.png',
        'type': 'horizontal',
        'color': '#003366',
        'bg': 'transparent',
        'desc': 'Horizontal logo - Primary blue'
    },
    {
        'name': 'permitindex-horizontal-white.png',
        'type': 'horizontal',
        'color': '#FFFFFF',
        'bg': '#003366',
        'desc': 'Horizontal logo - White on navy'
    },
    {
        'name': 'permitindex-horizontal-black.png',
        'type': 'horizontal',
        'color': '#000000',
        'bg': 'transparent',
        'desc': 'Horizontal logo - Black'
    },
]

def create_icon_html(color, bg_color):
    """Create HTML for square icon (just P with star cutout)"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 40px;
            background: {bg_color};
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        svg {{
            width: 400px;
            height: 400px;
        }}
    </style>
</head>
<body>
    <svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="PermitIndex Icon">
        <title>PermitIndex Icon</title>
        <defs>
            <mask id="p-icon-mask">
                <rect width="100%" height="100%" fill="white"/>
                <polygon points="20,2 21.5,6 25.5,6 22.2,8.5 23.5,12.5 20,9.8 16.5,12.5 17.8,8.5 14.5,6 18.5,6" fill="black"/>
            </mask>
        </defs>
        <text x="0" y="32" font-size="36" font-family="Arial Black, sans-serif" font-weight="900" fill="{color}" letter-spacing="-1" mask="url(#p-icon-mask)">P</text>
    </svg>
</body>
</html>
"""

def create_horizontal_html(color, bg_color):
    """Create HTML for horizontal logo"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 40px;
            background: {bg_color};
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        svg {{
            width: 480px;
            height: 80px;
        }}
    </style>
</head>
<body>
    <svg viewBox="0 0 240 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="PermitIndex">
        <title>PermitIndex</title>
        <desc>PermitIndex - Complete database of US government transactions</desc>
        <defs>
            <mask id="p-star-mask">
                <rect width="100%" height="100%" fill="white"/>
                <polygon points="20,2 21.5,6 25.5,6 22.2,8.5 23.5,12.5 20,9.8 16.5,12.5 17.8,8.5 14.5,6 18.5,6" fill="black"/>
            </mask>
        </defs>
        <g fill="{color}" font-family="Arial Black, sans-serif" font-weight="900">
            <text x="0" y="32" font-size="36" letter-spacing="-1" mask="url(#p-star-mask)">P</text>
            <text x="25" y="32" font-size="36" letter-spacing="-1">ermitIndex</text>
        </g>
    </svg>
</body>
</html>
"""

def generate_logos():
    """Generate all PNG logo variations"""

    # Clean and create output directory
    if os.path.exists(OUTPUT_DIR):
        import shutil
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("🎨 Generating official PermitIndex logo PNGs...\n")
    print(f"📁 Output location: {OUTPUT_DIR}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for config in LOGO_CONFIGS:
            print(f"Creating {config['desc']}...")

            # Choose appropriate viewport size
            if config['type'] == 'icon':
                page = browser.new_page(viewport={'width': 500, 'height': 500})
                html_content = create_icon_html(config['color'], config['bg'])
            else:  # horizontal
                page = browser.new_page(viewport={'width': 600, 'height': 200})
                html_content = create_horizontal_html(config['color'], config['bg'])

            # Load the HTML
            page.set_content(html_content)

            # Wait for fonts to load
            page.wait_for_timeout(500)

            # Take screenshot
            output_path = os.path.join(OUTPUT_DIR, config['name'])

            # Screenshot with transparent background (except for white versions)
            if config['bg'] == 'transparent':
                page.screenshot(path=output_path, omit_background=True)
            else:
                page.screenshot(path=output_path)

            print(f"✓ Saved: {config['name']}")
            page.close()

        browser.close()

    print("\n✅ All 6 official logo PNGs generated successfully!")
    print(f"\n📂 Files saved to: {OUTPUT_DIR}/\n")
    print("Generated files:")
    print("\nSquare Icons:")
    print("  - permitindex-icon-primary.png")
    print("  - permitindex-icon-white.png")
    print("  - permitindex-icon-black.png")
    print("\nHorizontal Logos:")
    print("  - permitindex-horizontal-primary.png")
    print("  - permitindex-horizontal-white.png")
    print("  - permitindex-horizontal-black.png")
    print(f"\n⚠️  These files are OUTSIDE the project directory and will NOT be committed to git")

if __name__ == '__main__':
    generate_logos()
