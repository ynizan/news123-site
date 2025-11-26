#!/bin/bash

echo "🔍 Premium Features Verification"
echo "================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        return 1
    fi
}

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $3"
        return 0
    else
        echo -e "${RED}✗${NC} $3"
        return 1
    fi
}

PASSED=0
FAILED=0

echo "📄 Checking Generated Pages:"
echo "----------------------------"
check_file "output/pricing/index.html" && ((PASSED++)) || ((FAILED++))
check_file "output/coming-soon/index.html" && ((PASSED++)) || ((FAILED++))
check_file "output/index.html" && ((PASSED++)) || ((FAILED++))

echo ""
echo "🎨 Checking Template Components:"
echo "--------------------------------"
check_file "templates/components/alert_widget_premium.html" && ((PASSED++)) || ((FAILED++))
check_file "templates/components/historic_data_widget.html" && ((PASSED++)) || ((FAILED++))
check_file "templates/components/csv_export_widget.html" && ((PASSED++)) || ((FAILED++))
check_file "templates/components/api_access_widget.html" && ((PASSED++)) || ((FAILED++))

echo ""
echo "💰 Checking Pricing Page Content:"
echo "---------------------------------"
check_content "output/pricing/index.html" "Free" "Free tier present" && ((PASSED++)) || ((FAILED++))
check_content "output/pricing/index.html" "\$39/mo" "Pro tier ($39/mo) present" && ((PASSED++)) || ((FAILED++))
check_content "output/pricing/index.html" "\$99/mo" "Business tier ($99/mo) present" && ((PASSED++)) || ((FAILED++))
check_content "output/pricing/index.html" "Enterprise" "Enterprise tier present" && ((PASSED++)) || ((FAILED++))
check_content "output/pricing/index.html" "MOST POPULAR" "MOST POPULAR badge present" && ((PASSED++)) || ((FAILED++))
check_content "output/pricing/index.html" "plausible.io" "Plausible analytics script" && ((PASSED++)) || ((FAILED++))

echo ""
echo "⏰ Checking Coming Soon Page:"
echo "-----------------------------"
check_content "output/coming-soon/index.html" "Join the Waitlist" "Waitlist form present" && ((PASSED++)) || ((FAILED++))
check_content "output/coming-soon/index.html" "sales@permitindex.com" "Sales email present" && ((PASSED++)) || ((FAILED++))
check_content "output/coming-soon/index.html" "plausible.io" "Plausible analytics script" && ((PASSED++)) || ((FAILED++))

echo ""
echo "🏠 Checking Homepage Widgets:"
echo "----------------------------"
check_content "output/index.html" "Export All Data to CSV" "CSV Export widget" && ((PASSED++)) || ((FAILED++))
check_content "output/index.html" "API Access for Developers" "API Access widget" && ((PASSED++)) || ((FAILED++))

echo ""
echo "📄 Checking Permit Page Widgets:"
echo "--------------------------------"
SAMPLE_PERMIT="output/california/san-jose/business-tax-certificate/index.html"
check_content "$SAMPLE_PERMIT" "Get Notified of Changes" "Alert widget on permit page" && ((PASSED++)) || ((FAILED++))
check_content "$SAMPLE_PERMIT" "Change History" "Historic data widget on permit page" && ((PASSED++)) || ((FAILED++))
check_content "$SAMPLE_PERMIT" "PRO FEATURE" "PRO FEATURE badge present" && ((PASSED++)) || ((FAILED++))

echo ""
echo "📚 Checking Documentation:"
echo "-------------------------"
check_file "ANALYTICS_EVENTS.md" && ((PASSED++)) || ((FAILED++))
check_file "PREMIUM_FEATURES_TESTING.md" && ((PASSED++)) || ((FAILED++))
check_file "PREMIUM_LAUNCH_PLAYBOOK.md" && ((PASSED++)) || ((FAILED++))

echo ""
echo "================================"
echo -e "Results: ${GREEN}${PASSED} passed${NC}, ${RED}${FAILED} failed${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Start local server: cd output && python3 -m http.server 8080"
    echo "2. Open test guide: http://localhost:8080/test_premium_features.html"
    echo "3. Or browse directly: http://localhost:8080/pricing/"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Review the output above.${NC}"
    exit 1
fi
