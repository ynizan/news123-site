#!/bin/bash

echo "⚡ Running critical tests only..."

pytest tests/critical/ tests/data/ \
  -m critical \
  -v \
  --html=quick-test-report.html \
  --self-contained-html

echo "✅ Critical tests complete!"
