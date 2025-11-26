import pytest
import requests

@pytest.mark.integration
@pytest.mark.slow
def test_worker_endpoint_accessible():
    """Tests that Cloudflare Worker endpoint is accessible"""
    worker_url = "https://permitindex-feedback-proxy.yaniv-nizan.workers.dev"

    try:
        # OPTIONS request should return CORS headers
        response = requests.options(worker_url, timeout=10)
        assert response.status_code in [200, 204, 405], f"Worker returned {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Worker not accessible: {e}")

@pytest.mark.integration
@pytest.mark.slow
def test_worker_cors_headers():
    """Verifies Worker returns proper CORS headers"""
    worker_url = "https://permitindex-feedback-proxy.yaniv-nizan.workers.dev"

    try:
        response = requests.options(worker_url, timeout=10)
        assert 'access-control-allow-origin' in response.headers or 'Access-Control-Allow-Origin' in response.headers
    except requests.exceptions.RequestException:
        pytest.skip("Worker not accessible")
