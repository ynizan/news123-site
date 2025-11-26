#!/usr/bin/env python3
"""
Test script to demonstrate multi-CSV validation
Creates test CSV files with various scenarios to verify validation works
"""

import os
import shutil
from pathlib import Path

def create_test_files():
    """Create test CSV files with various scenarios"""

    # Test 1: Valid file
    valid_csv = """agency_short,agency_full,request_type,cost,effort_hours,location_applicability,online_available,api_available
TEST Dept,Test State Department,Test Permit,100,2 hours,Statewide (Test State),Yes,No"""

    # Test 2: Duplicate permit-agency combination (should fail)
    duplicate_csv = """agency_short,agency_full,request_type,cost,effort_hours,location_applicability,online_available,api_available
TEST Dept,Test State Department,Test Permit,200,3 hours,Statewide (Test State),Yes,No"""

    # Test 3: Missing required column (should fail)
    missing_col_csv = """agency_short,agency_full,request_type,cost,effort_hours,online_available,api_available
MISSING Dept,Missing State Dept,Missing Column Test,300,4 hours,Yes,No"""

    # Test 4: Empty required field (should fail)
    empty_field_csv = """agency_short,agency_full,request_type,cost,effort_hours,location_applicability,online_available,api_available
,Empty Agency Dept,Empty Field Test,400,5 hours,Statewide (Empty State),Yes,No"""

    # Test 5: Valid file with extra columns (should pass with warning)
    extra_cols_csv = """agency_short,agency_full,request_type,cost,effort_hours,location_applicability,online_available,api_available,extra_field,another_extra
EXTRA Dept,Extra State Dept,Extra Columns Test,500,6 hours,Statewide (Extra State),Yes,No,extra value,another value"""

    test_dir = Path('data_test')
    test_dir.mkdir(exist_ok=True)

    (test_dir / 'test_valid.csv').write_text(valid_csv)
    (test_dir / 'test_duplicate.csv').write_text(duplicate_csv)
    (test_dir / 'test_missing_column.csv').write_text(missing_col_csv)
    (test_dir / 'test_empty_field.csv').write_text(empty_field_csv)
    (test_dir / 'test_extra_columns.csv').write_text(extra_cols_csv)

    print("✅ Test files created in data_test/\n")
    print("Test scenarios:")
    print("1. test_valid.csv - Should PASS")
    print("2. test_duplicate.csv - Should FAIL (duplicate permit-agency combo)")
    print("3. test_missing_column.csv - Should FAIL (missing location_applicability)")
    print("4. test_empty_field.csv - Should FAIL (empty agency_short)")
    print("5. test_extra_columns.csv - Should PASS with WARNING (extra columns)")
    print("\n" + "="*60)
    print("TO TEST:")
    print("="*60)
    print("# Backup current data")
    print("mv data data_backup\n")
    print("# Test with problematic files (should show errors)")
    print("mv data_test data")
    print("python3 generator.py\n")
    print("# Restore")
    print("mv data data_test")
    print("mv data_backup data")
    print("="*60)

if __name__ == "__main__":
    create_test_files()
