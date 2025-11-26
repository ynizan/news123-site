import pytest
import os
from pathlib import Path

@pytest.mark.visual
@pytest.mark.slow
def test_homepage_screenshot(page, live_url):
    """Takes screenshot of homepage for visual regression"""
    page.goto(live_url)
    page.wait_for_load_state('networkidle')

    screenshot_dir = Path('tests/visual/screenshots')
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = screenshot_dir / 'homepage.png'
    page.screenshot(path=str(screenshot_path), full_page=False)

    assert screenshot_path.exists(), "Screenshot not created"
    assert screenshot_path.stat().st_size > 1000, "Screenshot file too small"

@pytest.mark.visual
@pytest.mark.slow
def test_permit_page_screenshot(page, live_url):
    """Takes screenshot of permit page for visual regression"""
    page.goto(f"{live_url}/california/contractor-license/")
    page.wait_for_load_state('networkidle')

    screenshot_dir = Path('tests/visual/screenshots')
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = screenshot_dir / 'permit_page.png'
    page.screenshot(path=str(screenshot_path), full_page=False)

    assert screenshot_path.exists(), "Screenshot not created"
    assert screenshot_path.stat().st_size > 1000, "Screenshot file too small"

@pytest.mark.visual
@pytest.mark.slow
def test_mobile_homepage_screenshot(mobile_page, live_url):
    """Takes mobile screenshot for responsive testing"""
    mobile_page.goto(live_url)
    mobile_page.wait_for_load_state('networkidle')

    screenshot_dir = Path('tests/visual/screenshots')
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = screenshot_dir / 'homepage_mobile.png'
    mobile_page.screenshot(path=str(screenshot_path), full_page=False)

    assert screenshot_path.exists(), "Screenshot not created"
    assert screenshot_path.stat().st_size > 1000, "Screenshot file too small"
