import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.fixture(scope="session")
def browser():
    """Shared browser instance for all tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    """New page for each test - desktop viewport"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        ignore_https_errors=True
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def mobile_page(browser):
    """Mobile viewport for responsive tests"""
    context = browser.new_context(
        viewport={'width': 375, 'height': 812},
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        is_mobile=True,
        has_touch=True,
        ignore_https_errors=True
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def tablet_page(browser):
    """Tablet viewport for responsive tests"""
    context = browser.new_context(
        viewport={'width': 768, 'height': 1024},
        user_agent='Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        ignore_https_errors=True
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="session")
def live_url():
    """Base URL for live site"""
    return os.getenv('TEST_URL', 'https://ainews123.com')

@pytest.fixture(scope="session")
def output_dir():
    """Local output directory for testing generated files"""
    return os.path.abspath('output')
