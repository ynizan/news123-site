#!/bin/bash

echo "🧪 Running all PermitIndex tests..."

# Critical tests
echo "📍 Critical tests..."
pytest tests/critical/ -m critical -v

# Data tests
echo "📊 Data validation..."
pytest tests/data/ -v

# Visual tests
echo "🎨 Visual/brand tests..."
pytest tests/visual/ -m visual -v

# SEO tests
echo "🔍 SEO tests..."
pytest tests/seo/ -m seo -v

# Integration tests
echo "🔗 Integration tests..."
pytest tests/integration/ -v

# Analytics tests
echo "📈 Analytics tests..."
pytest tests/analytics/ -v

echo "✅ All tests complete! Check test-report.html"
