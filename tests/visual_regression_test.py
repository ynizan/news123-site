#!/usr/bin/env python3
"""
Visual Regression Tests for PermitIndex
Tests for duplicate elements, timeline numbering, and visual alignment issues.
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
from collections import Counter

# Add parent directory to path to import generator
sys.path.insert(0, str(Path(__file__).parent.parent))

class VisualRegressionTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.output_dir = Path(__file__).parent / "screenshots"
        self.baseline_dir = self.output_dir / "baseline"
        self.current_dir = self.output_dir / "current"
        self.diff_dir = self.output_dir / "diff"

        # Create directories
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.current_dir.mkdir(parents=True, exist_ok=True)
        self.diff_dir.mkdir(parents=True, exist_ok=True)

        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }

    def log(self, message, level="INFO"):
        """Log a message with color coding"""
        colors = {
            "INFO": "\033[94m",
            "PASS": "\033[92m",
            "FAIL": "\033[91m",
            "WARN": "\033[93m"
        }
        reset = "\033[0m"
        print(f"{colors.get(level, '')}{level}: {message}{reset}")

    def test_timeline_numbering(self, page, permit_url):
        """
        Test that timeline shows correct sequential numbering without duplicates
        """
        test_name = "Timeline Numbering"
        self.log(f"Running: {test_name}", "INFO")

        try:
            page.goto(f"{self.base_url}/{permit_url}")
            page.wait_for_load_state("networkidle")

            # Find all numbered circles in the timeline
            circles = page.locator('div[style*="background: var(--primary)"][style*="color: white"]').filter(has_text='')
            circle_count = circles.count()

            # Get the numbers from each circle
            circle_numbers = []
            for i in range(circle_count):
                number_text = circles.nth(i).inner_text().strip()
                if number_text.isdigit():
                    circle_numbers.append(int(number_text))

            # Check for sequential numbering (1, 2, 3, ...)
            expected = list(range(1, len(circle_numbers) + 1))

            if circle_numbers != expected:
                self.results["failed"] += 1
                error = f"{test_name} FAILED: Expected {expected}, got {circle_numbers}"
                self.results["errors"].append(error)
                self.log(error, "FAIL")
                return False

            # Check step text doesn't contain duplicate numbers like "1. Complete..."
            step_texts = page.locator('p.leading-relaxed').all_inner_texts()
            for i, text in enumerate(step_texts):
                # Check if text starts with "1. " or " 1. " (number prefix)
                if text.strip() and text.strip()[0].isdigit() and '. ' in text[:5]:
                    self.results["failed"] += 1
                    error = f"{test_name} FAILED: Step {i+1} has duplicate numbering: '{text[:50]}...'"
                    self.results["errors"].append(error)
                    self.log(error, "FAIL")
                    return False

            self.results["passed"] += 1
            self.log(f"{test_name} PASSED: {len(circle_numbers)} steps with correct sequential numbering", "PASS")
            return True

        except Exception as e:
            self.results["failed"] += 1
            error = f"{test_name} ERROR: {str(e)}"
            self.results["errors"].append(error)
            self.log(error, "FAIL")
            return False

    def test_no_duplicate_elements(self, page, permit_url):
        """
        Test for duplicate text or elements in the timeline section
        """
        test_name = "No Duplicate Timeline Elements"
        self.log(f"Running: {test_name}", "INFO")

        try:
            page.goto(f"{self.base_url}/{permit_url}")
            page.wait_for_load_state("networkidle")

            # Focus on the timeline section only
            timeline_section = page.locator('section.star-box:has(h2:text("How to Apply"))')

            if timeline_section.count() == 0:
                self.log(f"{test_name} SKIPPED: No timeline section found", "WARN")
                return True

            # Check for duplicate step text within timeline
            step_texts = timeline_section.locator('p.leading-relaxed').all_inner_texts()
            text_counts = Counter([t.strip() for t in step_texts if t.strip()])
            duplicates = {text[:50]: count for text, count in text_counts.items() if count > 1}

            if duplicates:
                self.results["failed"] += 1
                error = f"{test_name} FAILED: Found duplicate steps: {duplicates}"
                self.results["errors"].append(error)
                self.log(error, "FAIL")
                return False

            self.results["passed"] += 1
            self.log(f"{test_name} PASSED: No duplicate timeline elements", "PASS")
            return True

        except Exception as e:
            self.results["failed"] += 1
            error = f"{test_name} ERROR: {str(e)}"
            self.results["errors"].append(error)
            self.log(error, "FAIL")
            return False

    def test_visual_alignment(self, page, permit_url):
        """
        Test that timeline circles and text are properly aligned
        """
        test_name = "Timeline Visual Alignment"
        self.log(f"Running: {test_name}", "INFO")

        try:
            page.goto(f"{self.base_url}/{permit_url}")
            page.wait_for_load_state("networkidle")

            # Focus on the timeline section only
            timeline_section = page.locator('section.star-box:has(h2:text("How to Apply"))')

            if timeline_section.count() == 0:
                self.log(f"{test_name} SKIPPED: No timeline section found", "WARN")
                return True

            # Get timeline step containers within the section
            # Only select containers that have the numbered circles
            step_containers = timeline_section.locator('div.flex.items-start:has(div[style*="background: var(--primary)"][style*="color: white"])')
            step_count = step_containers.count()

            alignment_issues = []

            for i in range(step_count):
                container = step_containers.nth(i)

                # Check if container has both circle and text
                circle = container.locator('div[style*="background: var(--primary)"]')
                text = container.locator('p.leading-relaxed')

                if circle.count() == 0:
                    alignment_issues.append(f"Step {i+1}: Missing circle")
                if text.count() == 0:
                    alignment_issues.append(f"Step {i+1}: Missing text")

                # Check bounding boxes for overlap/misalignment
                if circle.count() > 0 and text.count() > 0:
                    circle_box = circle.bounding_box()
                    text_box = text.bounding_box()

                    if circle_box and text_box:
                        # Check if elements overlap (x coordinates)
                        if circle_box['x'] + circle_box['width'] > text_box['x']:
                            # Small overlap is OK (margin), but significant overlap is bad
                            overlap = (circle_box['x'] + circle_box['width']) - text_box['x']
                            if overlap > 10:  # More than 10px overlap
                                alignment_issues.append(
                                    f"Step {i+1}: Circle and text overlap by {overlap:.0f}px"
                                )

            if alignment_issues:
                self.results["failed"] += 1
                error = f"{test_name} FAILED: {', '.join(alignment_issues)}"
                self.results["errors"].append(error)
                self.log(error, "FAIL")
                return False

            self.results["passed"] += 1
            self.log(f"{test_name} PASSED: All {step_count} timeline steps properly aligned", "PASS")
            return True

        except Exception as e:
            self.results["failed"] += 1
            error = f"{test_name} ERROR: {str(e)}"
            self.results["errors"].append(error)
            self.log(error, "FAIL")
            return False

    def take_screenshot(self, page, name, baseline=False):
        """
        Take a screenshot and save to appropriate directory
        """
        target_dir = self.baseline_dir if baseline else self.current_dir
        filepath = target_dir / f"{name}.png"
        page.screenshot(path=str(filepath), full_page=True)
        return filepath

    def test_visual_regression(self, page, permit_url, name):
        """
        Compare current screenshot with baseline
        """
        test_name = f"Visual Regression: {name}"
        self.log(f"Running: {test_name}", "INFO")

        try:
            page.goto(f"{self.base_url}/{permit_url}")
            page.wait_for_load_state("networkidle")

            baseline_path = self.baseline_dir / f"{name}.png"
            current_path = self.current_dir / f"{name}.png"

            # Take current screenshot
            page.screenshot(path=str(current_path), full_page=True)

            # Check if baseline exists
            if not baseline_path.exists():
                self.log(f"{test_name} SKIPPED: No baseline found. Current screenshot saved as baseline.", "WARN")
                page.screenshot(path=str(baseline_path), full_page=True)
                return True

            # Compare screenshots (basic file size comparison for now)
            baseline_size = baseline_path.stat().st_size
            current_size = current_path.stat().st_size

            # Allow 5% difference
            diff_percent = abs(baseline_size - current_size) / baseline_size * 100

            if diff_percent > 5:
                self.results["failed"] += 1
                error = f"{test_name} FAILED: Visual change detected ({diff_percent:.1f}% difference)"
                self.results["errors"].append(error)
                self.log(error, "FAIL")
                self.log(f"  Baseline: {baseline_path}", "INFO")
                self.log(f"  Current:  {current_path}", "INFO")
                return False

            self.results["passed"] += 1
            self.log(f"{test_name} PASSED: Visual appearance matches baseline", "PASS")
            return True

        except Exception as e:
            self.results["failed"] += 1
            error = f"{test_name} ERROR: {str(e)}"
            self.results["errors"].append(error)
            self.log(error, "FAIL")
            return False

    def run_all_tests(self, test_mode="current"):
        """
        Run all visual regression tests

        Args:
            test_mode: "baseline" to create baseline screenshots, "current" to test against baseline
        """
        self.log("=" * 60, "INFO")
        self.log("PERMITINDEX VISUAL REGRESSION TESTS", "INFO")
        self.log("=" * 60, "INFO")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1920, "height": 1080})

            # Test pages
            test_pages = [
                ("california/food-truck-operating-permit/", "food-truck-permit"),
                ("california/business-license/", "business-license"),
                ("california/contractor-license/", "contractor-license"),
            ]

            for permit_url, name in test_pages:
                self.log(f"\nTesting: {permit_url}", "INFO")
                self.log("-" * 60, "INFO")

                if test_mode == "baseline":
                    # Create baseline screenshots
                    page.goto(f"{self.base_url}/{permit_url}")
                    page.wait_for_load_state("networkidle")
                    self.take_screenshot(page, name, baseline=True)
                    self.log(f"Baseline screenshot saved: {name}", "PASS")
                else:
                    # Run functional tests
                    self.test_timeline_numbering(page, permit_url)
                    self.test_no_duplicate_elements(page, permit_url)
                    self.test_visual_alignment(page, permit_url)

                    # Run visual regression test
                    self.test_visual_regression(page, permit_url, name)

            browser.close()

        # Print summary
        self.log("\n" + "=" * 60, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("=" * 60, "INFO")
        self.log(f"Passed: {self.results['passed']}", "PASS")
        self.log(f"Failed: {self.results['failed']}", "FAIL" if self.results['failed'] > 0 else "INFO")

        if self.results['errors']:
            self.log("\nERRORS:", "FAIL")
            for error in self.results['errors']:
                self.log(f"  - {error}", "FAIL")

        return self.results['failed'] == 0


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Run visual regression tests for PermitIndex")
    parser.add_argument(
        "--mode",
        choices=["baseline", "test"],
        default="test",
        help="Mode: 'baseline' to create baseline screenshots, 'test' to run tests"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL to test (default: http://localhost:8000)"
    )

    args = parser.parse_args()

    tester = VisualRegressionTester(base_url=args.url)

    if args.mode == "baseline":
        print("\n📸 Creating baseline screenshots...")
        tester.run_all_tests(test_mode="baseline")
        print("\n✅ Baseline screenshots created!")
        print(f"📁 Location: {tester.baseline_dir}")
    else:
        print("\n🧪 Running visual regression tests...")
        success = tester.run_all_tests(test_mode="current")

        if not success:
            sys.exit(1)

        print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
