#!/usr/bin/env python3
"""
Generate favicon files from SVG source
Requires: pip install Pillow cairosvg
"""

import os
from pathlib import Path

# Try importing required libraries
try:
    from PIL import Image
    import cairosvg
    import io
except ImportError as e:
    print(f"Error: Missing required library: {e}")
    print("Please install: pip install Pillow cairosvg")
    exit(1)

def svg_to_png(svg_path, png_path, size):
    """Convert SVG to PNG at specified size"""
    try:
        # Read SVG content
        with open(svg_path, 'r') as f:
            svg_content = f.read()

        # Convert SVG to PNG using cairosvg
        png_data = cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            output_width=size,
            output_height=size
        )

        # Save PNG
        with open(png_path, 'wb') as f:
            f.write(png_data)

        print(f"✓ Generated: {png_path.name} ({size}x{size})")
        return True
    except Exception as e:
        print(f"✗ Failed to generate {png_path.name}: {e}")
        return False

def create_ico(png_paths, ico_path):
    """Create multi-size .ico file from PNG images"""
    try:
        images = []
        for png_path in png_paths:
            if png_path.exists():
                img = Image.open(png_path)
                images.append(img)

        if images:
            images[0].save(
                ico_path,
                format='ICO',
                sizes=[(img.size[0], img.size[1]) for img in images]
            )
            print(f"✓ Generated: {ico_path.name} (multi-size)")
            return True
    except Exception as e:
        print(f"✗ Failed to generate {ico_path.name}: {e}")
        return False

def main():
    # Paths
    base_dir = Path(__file__).parent
    favicon_dir = base_dir / 'static' / 'favicon'
    svg_source = favicon_dir / 'logo-icon.svg'

    print("============================================================")
    print("🎨 FAVICON GENERATOR")
    print("============================================================")
    print(f"Source SVG: {svg_source}")
    print(f"Output directory: {favicon_dir}")
    print()

    # Check if SVG exists
    if not svg_source.exists():
        print(f"Error: SVG source not found at {svg_source}")
        return 1

    # Ensure output directory exists
    favicon_dir.mkdir(parents=True, exist_ok=True)

    # Define favicon sizes to generate
    sizes = {
        'favicon-16x16.png': 16,
        'favicon-32x32.png': 32,
        'android-chrome-192x192.png': 192,
        'android-chrome-512x512.png': 512,
        'apple-touch-icon.png': 180,
    }

    # Generate PNG files
    print("Generating PNG files...")
    png_files = []
    for filename, size in sizes.items():
        png_path = favicon_dir / filename
        if svg_to_png(svg_source, png_path, size):
            png_files.append(png_path)

    print()

    # Generate .ico file (multi-size)
    print("Generating .ico file...")
    ico_sizes = [16, 32, 48]
    ico_pngs = []
    for size in ico_sizes:
        png_path = favicon_dir / f'temp_{size}.png'
        if svg_to_png(svg_source, png_path, size):
            ico_pngs.append(png_path)

    if ico_pngs:
        ico_path = favicon_dir / 'favicon.ico'
        create_ico(ico_pngs, ico_path)

        # Clean up temporary files
        for png_path in ico_pngs:
            png_path.unlink()

    print()
    print("============================================================")
    print(f"✅ Favicon generation completed!")
    print(f"Generated {len(png_files) + 1} files")
    print("============================================================")
    return 0

if __name__ == '__main__':
    exit(main())
