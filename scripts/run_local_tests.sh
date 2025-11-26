#!/bin/bash

echo "🏠 Running local tests (no live site dependency)..."

# Run generator first
echo "🔄 Running generator..."
python3 generator.py

# Run tests that don't require live site
echo "📋 Running local tests..."
pytest tests/critical/test_site_builds.py \
       tests/data/ \
       tests/integration/test_github_integration.py \
       tests/integration/test_approval_workflow.py \
       -v

echo "✅ Local tests complete!"
