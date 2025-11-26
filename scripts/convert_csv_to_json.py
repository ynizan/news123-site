#!/usr/bin/env python3
"""
Convert permits.csv to permits.json

This script converts CSV files in data/permits/ to JSON format.
It handles special cases like:
- JSON strings stored in CSV columns (community_feedback, user_tips, faqs)
- NaN/empty values conversion to appropriate types
- Preserving data types and structure
"""

import pandas as pd
import json
import os
import sys

def convert_csv_to_json(csv_path, json_path):
    """
    Convert a CSV file to JSON format

    Args:
        csv_path: Path to input CSV file
        json_path: Path to output JSON file
    """
    print(f"Reading CSV from: {csv_path}")

    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"  - Found {len(df)} permit records")
    print(f"  - Found {len(df.columns)} columns")

    # Array fields that need special handling
    array_fields = ['community_feedback', 'user_tips', 'faqs']

    # Convert to JSON array
    permits = []
    for idx, row in df.iterrows():
        permit = {}
        for col in df.columns:
            value = row[col]

            # Handle NaN/empty values
            if pd.isna(value):
                if col in array_fields:
                    permit[col] = []  # Empty array for array fields
                else:
                    permit[col] = ""  # Empty string for other fields
            else:
                # Parse JSON string fields back to arrays/objects
                if col in array_fields:
                    if value and str(value).strip():
                        try:
                            parsed = json.loads(value)
                            permit[col] = parsed if isinstance(parsed, list) else []
                        except json.JSONDecodeError as e:
                            print(f"  ⚠️  Warning: Row {idx+2}, column '{col}': Invalid JSON - {e}")
                            permit[col] = []
                    else:
                        permit[col] = []
                else:
                    permit[col] = str(value).strip() if value else ""

        permits.append(permit)

    # Write JSON with pretty formatting
    print(f"Writing JSON to: {json_path}")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(permits, f, indent=2, ensure_ascii=False)

    print(f"✅ Conversion complete!")
    print(f"  - Converted {len(permits)} permits")
    print(f"  - Output file: {json_path}")

    # Print file size comparison
    csv_size = os.path.getsize(csv_path)
    json_size = os.path.getsize(json_path)
    print(f"  - CSV size: {csv_size:,} bytes")
    print(f"  - JSON size: {json_size:,} bytes")
    print(f"  - Size difference: {json_size - csv_size:,} bytes ({(json_size/csv_size-1)*100:.1f}% change)")


def main():
    """Main conversion process"""
    print("\n" + "=" * 60)
    print("CSV to JSON Converter")
    print("=" * 60 + "\n")

    # Convert main permits file
    csv_path = 'data/permits/permits.csv'
    json_path = 'data/permits/permits.json'

    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found")
        return 1

    try:
        convert_csv_to_json(csv_path, json_path)

        # Validate the output
        print("\n" + "=" * 60)
        print("Validating output JSON...")
        print("=" * 60 + "\n")

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ JSON is valid!")
        print(f"  - Type: {type(data).__name__}")
        print(f"  - Records: {len(data)}")

        if len(data) > 0:
            print(f"  - Fields in first record: {len(data[0])}")
            print(f"  - Sample fields: {list(data[0].keys())[:5]}...")

        print("\n✅ Conversion successful!\n")
        return 0

    except Exception as e:
        print(f"\n❌ Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
