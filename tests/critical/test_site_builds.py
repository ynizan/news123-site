import pytest
import subprocess
import os

@pytest.mark.critical
def test_generator_runs_without_errors():
    """Test that generator.py completes successfully"""
    # Set environment variable to skip Pagefind indexing (which can hang in tests)
    env = os.environ.copy()
    env['SKIP_PAGEFIND'] = '1'

    result = subprocess.run(
        ['python3', 'generator.py'],
        capture_output=True,
        text=True,
        timeout=60,
        env=env
    )
    assert result.returncode == 0, f"Generator failed: {result.stderr}"

@pytest.mark.critical
def test_output_directory_created(output_dir):
    """Test that output directory exists and has files"""
    assert os.path.exists(output_dir), "Output directory missing"
    assert os.path.exists(os.path.join(output_dir, 'index.html')), "Homepage not generated"

    html_files = [f for f in os.listdir(output_dir) if f.endswith('.html') and f != 'index.html']
    assert len(html_files) >= 1, "No permit pages generated"

@pytest.mark.critical
def test_required_files_exist(output_dir):
    """Test that all required files are generated"""
    required_files = ['sitemap.xml', 'robots.txt']

    for filename in required_files:
        filepath = os.path.join(output_dir, filename)
        assert os.path.exists(filepath), f"Required file missing: {filename}"
