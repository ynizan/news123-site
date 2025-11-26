import pytest
import time

@pytest.mark.seo
@pytest.mark.slow
def test_homepage_load_time(page, live_url):
    """Tests homepage loads within 3 seconds"""
    start = time.time()
    page.goto(live_url, wait_until='load')
    load_time = time.time() - start

    assert load_time < 3.0, f"Homepage took {load_time:.2f}s to load (max 3s)"

@pytest.mark.seo
@pytest.mark.slow
def test_permit_page_load_time(page, live_url):
    """Tests permit page loads within 3 seconds"""
    start = time.time()
    page.goto(f"{live_url}/california/contractor-license/", wait_until='load')
    load_time = time.time() - start

    assert load_time < 3.0, f"Permit page took {load_time:.2f}s to load (max 3s)"
