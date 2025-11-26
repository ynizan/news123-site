#!/usr/bin/env python3
"""
Generate PNG logo variations for PermitIndex
Creates 4 versions: Primary (Navy), Accent (Orange), White, and Black
"""

from playwright.sync_api import sync_playwright
import os

# Logo variations with different colors
LOGO_VARIATIONS = {
    'primary': {
        'color': '#003366',
        'name': 'logo-primary.png',
        'bg': 'transparent'
    },
    'accent': {
        'color': '#FF6B35',
        'name': 'logo-accent.png',
        'bg': 'transparent'
    },
    'white': {
        'color': '#FFFFFF',
        'name': 'logo-white.png',
        'bg': '#003366'  # Dark background to show white logo
    },
    'black': {
        'color': '#000000',
        'name': 'logo-black.png',
        'bg': 'transparent'
    }
}

def create_logo_html(color, bg_color='transparent'):
    """Create HTML with the logo SVG"""

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
        <g fill="{color}" font-family="Arial Black, Helvetica Bold, sans-serif" font-weight="900">
            <text x="0" y="32" font-size="36" letter-spacing="-1" mask="url(#p-star-mask)">P</text>
            <text x="25" y="32" font-size="36" letter-spacing="-1">ermitIndex</text>
        </g>
    </svg>
</body>
</html>
"""

def generate_logo_pngs():
    """Generate PNG files for all logo variations"""

    output_dir = 'output/logos'
    os.makedirs(output_dir, exist_ok=True)

    print("🎨 Generating PermitIndex logo variations...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 600, 'height': 200})

        for variant_name, config in LOGO_VARIATIONS.items():
            print(f"Creating {variant_name} logo ({config['color']})...")

            # Create HTML with the logo
            html_content = create_logo_html(config['color'], config['bg'])

            # Load the HTML
            page.set_content(html_content)

            # Wait for fonts to load
            page.wait_for_timeout(500)

            # Take screenshot
            output_path = os.path.join(output_dir, config['name'])

            # Screenshot with transparent background (except for white version)
            if config['bg'] == 'transparent':
                page.screenshot(
                    path=output_path,
                    omit_background=True
                )
            else:
                page.screenshot(path=output_path)

            print(f"✓ Saved: {output_path}")

        browser.close()

    print("\n✅ All logo variations generated successfully!")
    print(f"📁 Output directory: {output_dir}/")
    print("\nGenerated files:")
    for config in LOGO_VARIATIONS.values():
        print(f"  - {config['name']}")

if __name__ == '__main__':
    generate_logo_pngs()
