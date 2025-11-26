import pytest

@pytest.mark.seo
def test_images_have_alt_text(page, live_url):
    """Verifies all images have alt attributes"""
    page.goto(live_url)

    images = page.locator('img').all()

    if len(images) > 0:
        for i, img in enumerate(images):
            alt = img.get_attribute('alt')
            # Alt can be empty string for decorative images, but must exist
            assert alt is not None, f"Image {i} missing alt attribute"

@pytest.mark.seo
def test_og_image_exists(page, live_url):
    """Checks that Open Graph image is specified"""
    page.goto(live_url)

    og_image = page.locator('meta[property="og:image"]').get_attribute('content')
    assert og_image, "No Open Graph image specified"
    assert og_image.startswith('http'), "OG image should be absolute URL"
