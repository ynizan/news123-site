#!/usr/bin/env python3
"""
Generate Claude Code-ready instructions from test failures
"""

import json
import sys
from datetime import datetime
import argparse

def load_test_report(filepath):
    """Load pytest JSON report"""
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_instructions(test_report):
    """Convert test failures to Claude Code instructions"""

    failed_tests = [
        test for test in test_report.get('tests', [])
        if test.get('outcome') == 'failed'
    ]

    if not failed_tests:
        return None

    # Header
    instructions = [
        f"Subject: News123 Tests Failed - {len(failed_tests)} issues detected\n",
        "",
        "─" * 70,
        "COPY EVERYTHING BELOW THIS LINE TO CLAUDE CODE",
        "─" * 70,
        "",
        f"News123 automated tests detected {len(failed_tests)} issues that need fixing.",
        "",
        f"TASK: Fix the following test failures detected on {datetime.now().strftime('%Y-%m-%d')} at {datetime.now().strftime('%H:%M')} UTC",
        ""
    ]

    # Generate instructions for each failure
    for i, test in enumerate(failed_tests, 1):
        instructions.extend(format_test_failure(i, test))

    # Footer
    instructions.extend([
        "",
        "═" * 70,
        "AFTER FIXING ALL ISSUES",
        "═" * 70,
        "",
        "1. Run full test suite to verify all fixes:",
        "   pytest tests/",
        "",
        "2. Commit changes:",
        '   git add .',
        '   git commit -m "Fix test failures: [describe fixes]"',
        '   git push origin main',
        "",
        "3. Report back:",
        "   - Confirmation that all issues are fixed",
        "   - Test results showing all tests pass",
        "   - Summary of changes made",
        "",
        "─" * 70,
        "END OF CLAUDE CODE INSTRUCTIONS",
        "─" * 70,
        ""
    ])

    return "\n".join(instructions)

def format_test_failure(issue_num, test):
    """Format a single test failure for Claude Code"""

    test_name = test.get('nodeid', 'Unknown test')

    # Get error message
    call_info = test.get('call', {})
    longrepr = call_info.get('longrepr', '')

    # Extract just the relevant error lines
    if isinstance(longrepr, str):
        error_lines = longrepr.split('\n')
        # Get assertion error or last few lines
        relevant_lines = [l for l in error_lines if l.strip() and not l.startswith('_')][-5:]
        error_msg = '\n'.join(relevant_lines)
    else:
        error_msg = str(longrepr)

    # Determine test category
    if 'seo' in test_name:
        category = 'SEO'
    elif 'visual' in test_name or 'brand' in test_name:
        category = 'Visual/Brand'
    elif 'critical' in test_name:
        category = 'Critical'
    elif 'data' in test_name:
        category = 'Data Quality'
    elif 'analytics' in test_name:
        category = 'Analytics'
    elif 'integration' in test_name:
        category = 'Integration'
    else:
        category = 'General'

    instructions = [
        "",
        "═" * 70,
        f"ISSUE {issue_num}: {test_name.split('::')[-1].replace('_', ' ').title()}",
        "═" * 70,
        "",
        f"CATEGORY: {category}",
        f"TEST: {test_name}",
        "",
        "PROBLEM:",
        error_msg[:500],  # Truncate long errors
        "",
        "FIX REQUIRED:",
    ]

    # Add fix instructions based on test type
    fix_steps = generate_fix_steps(test_name, error_msg)
    instructions.extend(fix_steps)

    instructions.extend([
        "",
        "VERIFICATION:",
        f"After fixing, run: pytest {test_name}",
        ""
    ])

    return instructions

def generate_fix_steps(test_name, error_msg):
    """Generate specific fix steps based on test type"""

    # Meta description tests
    if 'meta_description' in test_name:
        return [
            "1. Open templates/transaction_page.html",
            "2. Locate meta description template",
            "3. Ensure descriptions are 150-160 characters",
            "4. Use descriptive, keyword-rich content",
            "5. Regenerate: python3 generator.py",
            "6. Verify output HTML files"
        ]

    # Sitemap tests
    elif 'sitemap' in test_name:
        return [
            "1. Verify generator.py creates sitemap.xml",
            "2. Check all pages in output/ are included",
            "3. Ensure lastmod dates are ISO format",
            "4. Regenerate: python3 generator.py",
            "5. Validate sitemap at https://news123.info/sitemap.xml"
        ]

    # Broken link tests
    elif 'link' in test_name:
        return [
            "1. Identify broken link(s) from error message",
            "2. Check if target page exists in output/",
            "3. Fix link URL in template OR remove link",
            "4. Update templates/index.html or transaction_page.html",
            "5. Regenerate: python3 generator.py"
        ]

    # CSV/data tests
    elif 'csv' in test_name or 'data' in test_name:
        return [
            "1. Open data/permits/permits.csv",
            "2. Find row(s) with issues from error",
            "3. Fix: formatting, missing values, or invalid data",
            "4. Ensure dates: YYYY-MM-DD format",
            "5. Verify URLs are valid",
            "6. Regenerate: python3 generator.py"
        ]

    # Visual/brand tests
    elif 'visual' in test_name or 'brand' in test_name or 'color' in test_name:
        return [
            "1. Review BRAND_GUIDELINES.md",
            "2. Check templates and CSS for violations",
            "3. Use only approved colors: #003366, #FF6B35",
            "4. Verify star cutout positioning formula",
            "5. Update templates/CSS",
            "6. Regenerate: python3 generator.py"
        ]

    # Analytics tests
    elif 'analytics' in test_name or 'plausible' in test_name:
        return [
            "1. Verify Plausible script in templates",
            "2. Check script URL is correct",
            "3. Test events fire properly",
            "4. Update tracking code if needed",
            "5. Regenerate: python3 generator.py"
        ]

    # Generic fallback
    else:
        return [
            "1. Review error message above",
            "2. Identify which file(s) need modification",
            "3. Make necessary changes",
            "4. Regenerate if templates/data changed: python3 generator.py",
            "5. Run specific test to verify"
        ]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-report', required=True, help='Path to pytest JSON report')
    parser.add_argument('--output', required=True, help='Output file for instructions')
    args = parser.parse_args()

    try:
        report = load_test_report(args.test_report)
        instructions = generate_instructions(report)

        if instructions:
            with open(args.output, 'w') as f:
                f.write(instructions)
            print(f"✅ Claude Code instructions written to {args.output}")
            print(f"   Found {len([t for t in report['tests'] if t['outcome'] == 'failed'])} test failures")
        else:
            print("✅ All tests passed - no instructions needed")
            # Create empty file so workflow doesn't fail
            with open(args.output, 'w') as f:
                f.write("All tests passed! No fixes needed.\n")
    except Exception as e:
        print(f"❌ Error generating instructions: {e}")
        sys.exit(1)
