#!/bin/bash
set -e

echo "════════════════════════════════════════════════════════════════"
echo "🧪 PRE-COMMIT TESTING - Run before git commit"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# Test 1: CSV Schema Validation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test 1: CSV Schema Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 -m pytest tests/data/test_csv_schema.py -v --tb=short; then
    echo -e "${GREEN}✅ CSV schema validation passed${NC}"
else
    echo -e "${RED}❌ CSV schema validation failed${NC}"
    FAILED=1
fi
echo ""

# Test 2: Data Quality
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Test 2: Data Quality Checks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 -m pytest tests/data/test_required_fields.py tests/data/test_data_quality.py -v --tb=short; then
    echo -e "${GREEN}✅ Data quality checks passed${NC}"
else
    echo -e "${RED}❌ Data quality checks failed${NC}"
    FAILED=1
fi
echo ""

# Test 3: Site Generator
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Test 3: Site Generator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if SKIP_PAGEFIND=1 python3 generator.py; then
    echo -e "${GREEN}✅ Site generator ran successfully${NC}"
else
    echo -e "${RED}❌ Site generator failed${NC}"
    FAILED=1
fi
echo ""

# Test 4: Build Output Validation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Test 4: Build Output Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 -m pytest tests/critical/test_site_builds.py -v --tb=short; then
    echo -e "${GREEN}✅ Build output validation passed${NC}"
else
    echo -e "${RED}❌ Build output validation failed${NC}"
    FAILED=1
fi
echo ""

# Test 5: Thin Content SEO Protection
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Test 5: Thin Content SEO Protection (CRITICAL)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 -m pytest tests/critical/test_thin_content.py -v --tb=short; then
    echo -e "${GREEN}✅ Thin content SEO protection passed${NC}"
else
    echo -e "${RED}❌ Thin content SEO protection failed${NC}"
    echo -e "${YELLOW}⚠️  This is CRITICAL - thin content may be exposed to indexing${NC}"
    FAILED=1
fi
echo ""

# Test 6: GitHub Workflows Validation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚙️  Test 6: GitHub Workflows"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 -m pytest tests/integration/test_github_integration.py tests/integration/test_approval_workflow.py -v --tb=short; then
    echo -e "${GREEN}✅ Workflow validation passed${NC}"
else
    echo -e "${RED}❌ Workflow validation failed${NC}"
    FAILED=1
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL PRE-COMMIT TESTS PASSED${NC}"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "✓ Safe to commit and push"
    echo ""
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo -e "${YELLOW}⚠️  DO NOT COMMIT until tests pass${NC}"
    echo ""
    echo "Fix the failing tests above, then run:"
    echo "  ./scripts/pre_commit_tests.sh"
    echo ""
    exit 1
fi
