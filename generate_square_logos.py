#!/usr/bin/env python3
"""
Generate square PNG logo variations for PermitIndex (just the P)
Creates 4 versions: Primary (Navy), Accent (Orange), White, and Black
Outputs to ~/Downloads/news123-logos/
"""

from playwright.sync_api import sync_playwright
import os

# Output to user's Downloads folder, outside the project
OUTPUT_DIR = os.path.expanduser('~/Downloads/news123-logos')

# Logo variations with different colors
LOGO_VARIATIONS = {
    'primary': {
        'color': '#003366',
        'name': 'logo-square-primary.png',
        'bg': 'transparent'
    },
    'accent': {
        'color': '#FF6B35',
        'name': 'logo-square-accent.png',
        'bg': 'transparent'
    },
    'white': {
        'color': '#FFFFFF',
        'name': 'logo-square-white.png',
        'bg': '#003366'  # Dark background to show white logo
    },
    'black': {
        'color': '#000000',
        'name': 'logo-square-black.png',
        'bg': 'transparent'
    }
}

def create_square_logo_html(color, bg_color='transparent'):
    """Create HTML with the square P logo SVG"""

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
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="PermitIndex">
        <title>PermitIndex</title>
        <desc>PermitIndex - Complete database of US government transactions</desc>
        <defs>
            <mask id="p-star-mask-square">
                <rect width="100%" height="100%" fill="white"/>
                <!-- Star cutout positioned in top-right of P -->
                <polygon points="50,15 52,20 57,20 53,23 55,28 50,25 45,28 47,23 43,20 48,20" fill="black"/>
            </mask>
        </defs>
        <g fill="{color}" font-family="Arial Black, Helvetica Bold, sans-serif" font-weight="900">
            <text x="10" y="80" font-size="90" letter-spacing="-2" mask="url(#p-star-mask-square)">P</text>
        </g>
    </svg>
</body>
</html>
"""

def generate_square_logo_pngs():
    """Generate square PNG files for all logo variations"""

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"🎨 Generating PermitIndex square logo variations...\n")
    print(f"📁 Output location: {OUTPUT_DIR}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 500, 'height': 500})

        for variant_name, config in LOGO_VARIATIONS.items():
            print(f"Creating {variant_name} square logo ({config['color']})...")

            # Create HTML with the logo
            html_content = create_square_logo_html(config['color'], config['bg'])

            # Load the HTML
            page.set_content(html_content)

            # Wait for fonts to load
            page.wait_for_timeout(500)

            # Take screenshot
            output_path = os.path.join(OUTPUT_DIR, config['name'])

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

    print("\n✅ All square logo variations generated successfully!")
    print(f"\n📂 Files saved to: {OUTPUT_DIR}/")
    print("\nGenerated files:")
    for config in LOGO_VARIATIONS.values():
        print(f"  - {config['name']}")
    print(f"\n⚠️  These files are OUTSIDE the project directory and will NOT be committed to git")

if __name__ == '__main__':
    generate_square_logo_pngs()
