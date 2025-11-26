#!/usr/bin/env python3
"""
Generate favicon files using PIL directly
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"Error: Missing required library: {e}")
    print("Please install: pip install Pillow")
    exit(1)

def create_p_icon(size, output_path):
    """Create a simple 'P' icon with star cutout"""
    # Create image with navy blue background
    img = Image.new('RGB', (size, size), '#003366')
    draw = ImageDraw.Draw(img)

    # Calculate sizes proportional to image
    padding = size // 10
    letter_width = size // 2
    letter_top = padding
    letter_height = size - (padding * 2)

    # Draw 'P' letter in white
    # Vertical bar
    bar_width = size // 6
    draw.rectangle([
        padding,
        letter_top,
        padding + bar_width,
        letter_top + letter_height
    ], fill='#FFFFFF')

    # Top loop of P
    loop_size = int(letter_height * 0.4)
    draw.ellipse([
        padding,
        letter_top,
        padding + bar_width + loop_size,
        letter_top + loop_size
    ], fill='#FFFFFF')

    # Cut out inside of loop
    inner_padding = bar_width // 2
    draw.ellipse([
        padding + inner_padding,
        letter_top + inner_padding,
        padding + bar_width + loop_size - inner_padding,
        letter_top + loop_size - inner_padding
    ], fill='#003366')

    # Draw small star in top-right (simplified)
    star_size = max(4, size // 10)
    star_x = size - star_size * 2
    star_y = star_size

    # Simple star as diamond/square for small sizes
    if size >= 32:
        # Draw a small star shape
        star_points = [
            (star_x, star_y - star_size//2),  # top
            (star_x + star_size//4, star_y),  # right-mid
            (star_x + star_size//2, star_y + star_size//2),  # right-bottom
            (star_x, star_y + star_size//4),  # bottom-mid
            (star_x - star_size//2, star_y + star_size//2),  # left-bottom
            (star_x - star_size//4, star_y),  # left-mid
        ]
        draw.polygon(star_points, fill='#F8F9FA')

    # Save
    img.save(output_path, 'PNG')
    print(f"✓ Generated: {output_path.name} ({size}x{size})")
    return img

def main():
    base_dir = Path(__file__).parent
    favicon_dir = base_dir / 'static' / 'favicon'

    print("============================================================")
    print("🎨 FAVICON GENERATOR")
    print("============================================================")
    print(f"Output directory: {favicon_dir}")
    print()

    # Ensure output directory exists
    favicon_dir.mkdir(parents=True, exist_ok=True)

    # Define favicon sizes to generate
    sizes_to_generate = {
        'favicon-16x16.png': 16,
        'favicon-32x32.png': 32,
        'android-chrome-192x192.png': 192,
        'android-chrome-512x512.png': 512,
        'apple-touch-icon.png': 180,
    }

    # Generate PNG files
    print("Generating PNG files...")
    images = {}
    for filename, size in sizes_to_generate.items():
        output_path = favicon_dir / filename
        img = create_p_icon(size, output_path)
        images[size] = img

    print()

    # Generate .ico file (multi-size)
    print("Generating .ico file...")
    ico_path = favicon_dir / 'favicon.ico'
    ico_sizes = [16, 32, 48]
    ico_images = []

    for size in ico_sizes:
        img = create_p_icon(size, favicon_dir / f'temp_{size}.png')
        ico_images.append(img)

    # Save as .ico
    if ico_images:
        ico_images[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.size[0], img.size[1]) for img in ico_images]
        )
        print(f"✓ Generated: {ico_path.name} (multi-size)")

        # Clean up temporary files
        for size in ico_sizes:
            temp_file = favicon_dir / f'temp_{size}.png'
            if temp_file.exists():
                temp_file.unlink()

    print()
    print("============================================================")
    print(f"✅ Favicon generation completed!")
    print(f"Generated {len(sizes_to_generate) + 1} files")
    print("============================================================")
    return 0

if __name__ == '__main__':
    exit(main())
