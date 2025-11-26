# News123 JSON Schema Documentation

This document defines the complete data schema for permits in the News123 system.

## Schema Version: 3.2 (31 fields)

Last Updated: 2025-11-19

---

## File Organization

As of 2025-11-19, JSON files are organized into subdirectories:

- **`data/permits/`** - Permit JSON files (supports multiple files that will be combined)
- **`data/feedback/`** - User feedback CSV file(s) *(still CSV for now)*
- **`data/contributors/`** - Contributor profile CSV file(s) *(still CSV for now)*

**Note**: You can add multiple permit JSON files to `data/permits/` and they will all be loaded and combined into one dataset. This allows for modular organization by state, region, or category.

Each JSON file should contain an array of permit objects:

```json
[
  {
    "agency_short": "NYC DCWP",
    "request_type": "General Business License",
    ...
  },
  {
    "agency_short": "LA Finance",
    "request_type": "Business Tax Registration",
    ...
  }
]
```

---

## Schema Overview

Permit JSON files in **`data/permits/`** must contain permit objects with **31 fields** as specified below.

- **10 Required Fields**: Must have data for every permit
- **21 Optional Fields**: Enrich content quality when provided

### Quick Stats
- **Total Fields**: 31
- **Required**: 10 (marked with ⚠️)
- **Optional**: 21 (marked with ✅)
- **Array Fields**: 4 (community_feedback, user_tips, faqs, related_pages)

---

## Complete Field Reference

### 1. Core Identification

#### `id` ⚠️ REQUIRED
- **Type**: String (UUID)
- **Description**: Unique identifier (GUID/UUID) for each permit entry
- **Example**: `"2e89cc1d-215d-4281-824b-003bffe05fc6"`
- **Format**: UUID v4 (standard GUID format)
- **Validation**: Must be a valid UUID format, cannot be empty or null
- **Best Practice**: Automatically generated when adding new permits to ensure uniqueness

#### `name` ⚠️ REQUIRED
- **Type**: String
- **Description**: Short 2-word name for the permit, generated from agency and request type
- **Example**: `"Chandler License"`, `"Business Permit"`, `"Finance Registration"`
- **Format**: Exactly 2 words, typically "[Location/Department] [Type]"
- **Validation**: Must be a non-empty string with exactly 2 words, cannot be empty or null
- **Best Practice**: Auto-generated from `agency_short` and `request_type` fields

#### `agency_short` ⚠️ REQUIRED
- **Type**: String
- **Description**: Short agency name or abbreviation
- **Example**: `"NYC DCWP"`, `"LA Office of Finance"`
- **Validation**: Cannot be empty or null

#### `agency_full` ⚠️ REQUIRED
- **Type**: String
- **Description**: Full official agency name
- **Example**: `"New York City Department of Consumer and Worker Protection"`
- **Validation**: Cannot be empty or null

#### `request_type` ⚠️ REQUIRED
- **Type**: String
- **Description**: Type of permit or license
- **Example**: `"General Business License"`, `"Business Tax Registration Certificate"`
- **Validation**: Cannot be empty or null

#### `description` ✅ Optional
- **Type**: String (Long)
- **Description**: Detailed description of what the permit covers and who it applies to
- **Example**: `"This applies to any individual or entity conducting business within Anchorage city limits, including home-based businesses, contractors, and retail operations."`
- **Best Practice**: Provide context about the permit's scope and applicability
- **Validation**: Can be empty string or null
- **Used In**: Transaction pages, jurisdiction hub pages

#### `processing_time` ✅ Optional
- **Type**: String
- **Description**: How long it takes to process the application
- **Example**: `"Typically 5 to 10 business days after application submission."`, `"2-4 weeks"`
- **Fallback**: If not provided, system falls back to `effort_hours` field
- **Validation**: Can be empty string or null
- **Used In**: Transaction pages, jurisdiction hub pages

---

### 2. Process Details

#### `cost` ⚠️ REQUIRED
- **Type**: String
- **Description**: Fee information (can describe ranges or variables)
- **Example**: `"Varies by license type. Fees can range from under $100 to several hundred dollars."`
- **Validation**: Cannot be empty or null

#### `how_to_description` ✅ Optional
- **Type**: String (Long)
- **Description**: Step-by-step instructions for applying
- **Example**: `"Step 1: Use the Step-by-Step tool... Step 2: Gather all necessary documents..."`
- **Best Practice**: Use numbered steps for clarity
- **Validation**: Can be empty string or null

#### `payment_form_url` ✅ Optional
- **Type**: String (URL)
- **Description**: Direct link to application or payment form
- **Example**: `"https://a856-eevents.nyc.gov/dca/default_self.aspx"`
- **Validation**: Should be valid URL if provided, can be empty string or null

---

### 3. Eligibility & Scope

#### `eligibility` ✅ Optional
- **Type**: String
- **Description**: Who can apply and any requirements
- **Example**: `"Applicants must typically be at least 18 years old and have a legally registered business."`
- **Validation**: Can be empty string or null

#### `location_applicability` ⚠️ REQUIRED
- **Type**: String
- **Description**: Geographic scope where permit is valid
- **Example**: `"New York City, New York"`, `"City of Los Angeles, California"`
- **Validation**: Cannot be empty or null

#### `document_requirements` ✅ Optional
- **Type**: String (Comma-separated list)
- **Description**: Required documents for application
- **Example**: `"Business Certificate, Sales Tax ID, Federal EIN, Government-issued Photo ID"`
- **Best Practice**: Use comma separation for clarity
- **Validation**: Can be empty string or null

---

### 4. Volume & Timing

#### `estimated_monthly_volume` ✅ Optional
- **Type**: String
- **Description**: Approximate number of monthly applications
- **Example**: `"2000-5000"`, `"500-1500"`
- **Format**: Use hyphen for ranges
- **Validation**: Can be empty string or null

#### `deadline_window` ✅ Optional
- **Type**: String
- **Description**: Renewal periods, deadlines, or time windows
- **Example**: `"Licenses typically need to be renewed every 2 years."`
- **Validation**: Can be empty string or null

#### `effort_hours` ⚠️ REQUIRED
- **Type**: String
- **Description**: Estimated time to complete application
- **Example**: `"3-8 hours"`, `"Less than 1 hour"`, `"1-2 hours"`
- **Validation**: Cannot be empty or null

---

### 5. Availability Flags

#### `online_available` ⚠️ REQUIRED
- **Type**: String
- **Description**: Whether application can be completed online
- **Values**: `"Yes"` or `"No"`
- **Validation**: Cannot be empty or null

#### `api_available` ⚠️ REQUIRED
- **Type**: String
- **Description**: Whether agency provides API access
- **Values**: `"Yes"` or `"No"`
- **Validation**: Cannot be empty or null

#### `mcp_available` ✅ Optional
- **Type**: String
- **Description**: Whether MCP (Model Context Protocol) integration exists
- **Values**: `"Yes"` or `"No"` (can be empty string or null)
- **Validation**: Can be empty string or null

---

### 6. Community Content - ENRICHES PAGES

#### `common_mistakes` ✅ Optional
- **Type**: String
- **Description**: Common errors applicants make
- **Example**: `"Not having all required documents can delay processing by weeks."`
- **Validation**: Can be empty string or null

#### `community_feedback` ✅ Optional
- **Type**: Array of Strings
- **Description**: User feedback and reviews
- **Format**:
```json
["Feedback item 1", "Feedback item 2", "Feedback item 3"]
```
- **Validation**: Must be array (can be empty array `[]`)

#### `user_tips` ✅ Optional
- **Type**: Array of Strings
- **Description**: Helpful tips from users who completed the process
- **Format**:
```json
["Tip 1: Apply early in the morning", "Tip 2: Have all docs ready", "Tip 3: Use the online portal"]
```
- **Validation**: Must be array (can be empty array `[]`)

#### `faqs` ✅ Optional
- **Type**: Array of Objects
- **Description**: Frequently asked questions with answers
- **Format**:
```json
[
  {"question": "How long does processing take?", "answer": "Typically 2-4 weeks."},
  {"question": "Can I apply online?", "answer": "Yes, through the city portal."}
]
```
- **Validation**: Must be array of objects, each with `question` and `answer` keys (can be empty array `[]`)

---

### 7. Agency Contact - HELPS USERS

#### `agency_phone` ✅ Optional
- **Type**: String
- **Description**: Agency contact phone number
- **Example**: `"(212) 436-0000"`, `"800-555-1234"`
- **Validation**: Can be empty string or null

#### `agency_email` ✅ Optional
- **Type**: String
- **Description**: Agency contact email
- **Example**: `"permits@nyc.gov"`
- **Validation**: Can be empty string or null

#### `agency_address` ✅ Optional
- **Type**: String
- **Description**: Physical office address
- **Example**: `"42 Broadway, New York, NY 10004"`
- **Validation**: Can be empty string or null

#### `agency_hours` ✅ Optional
- **Type**: String
- **Description**: Office hours for in-person visits
- **Example**: `"Monday-Friday 9:00 AM - 5:00 PM"`
- **Validation**: Can be empty string or null

---

### 8. Metadata

#### `related_pages` ✅ Optional
- **Type**: Array of Strings (UUIDs)
- **Description**: List of related permit IDs (references to other permit entries in the same document)
- **Format**:
```json
[
  "2e89cc1d-215d-4281-824b-003bffe05fc6",
  "85fef12f-ad0a-464d-ac6c-139fb8a28c67"
]
```
- **Validation**: Must be array (can be empty array `[]`). Each item must be a valid UUID string that references another permit's `id` field in the same document

#### `date_extracted` ✅ Optional
- **Type**: String (Date in YYYY-MM-DD format)
- **Description**: When this data was collected
- **Example**: `"2025-11-17"`
- **Format**: ISO date format preferred
- **Validation**: Can be empty string or null

#### `source_url` ✅ Optional
- **Type**: String (URL)
- **Description**: Original source where data was found
- **Example**: `"https://www.nyc.gov/site/dcwp/businesses/apply-for-a-license.page"`
- **Validation**: Can be empty string or null

---

### 9. Contributor System

#### `verified_by` ✅ Optional
- **Type**: String
- **Description**: ID of contributor who verified this permit
- **Example**: `"sarah-chen"` (matches contributor_id in contributors.csv)
- **Validation**: Should match a contributor_id if provided, can be empty string or null
- **Special**: Empty means permit is unclaimed (shows "Claim This Page" widget)

---

## Validation Rules

### Automated Validation (generator.py)

The generator.py script validates:

1. **Field Presence**: Must have all 31 fields (can be null/empty for optional fields)
2. **Required Fields**: 10 required fields cannot be null or empty string
3. **Array Format**: community_feedback, user_tips, faqs, related_pages must be arrays
4. **FAQ Structure**: faqs array items must have `question` and `answer` keys
5. **Related Pages Structure**: related_pages array items must be valid UUID strings referencing other permit IDs
6. **Duplicate Check**: No duplicate permit-agency combinations across all JSON files
7. **ID Format**: If provided, `id` field should be a valid UUID format

### Automated Tests (tests/data/test_json_schema.py)

Pytest validates:

1. ✅ File exists
2. ✅ Valid JSON format
3. ✅ Is a JSON array
4. ✅ Has all 31 fields in permit objects
5. ✅ Required fields not empty (including id and name)
6. ✅ Array fields have correct structure
7. ✅ ID field format (valid UUID)
8. ✅ Name field format (2 words, required)

### Running Validation

```bash
# Run generator validation
python3 generator.py

# Run automated tests
pytest tests/data/test_json_schema.py -v

# Run critical tests only
pytest tests/data/test_json_schema.py -m critical -v
```

---

## Common Mistakes to Avoid

1. **Invalid JSON**: Use a JSON validator to ensure proper syntax
2. **Missing Fields**: All 31 fields should be present (can be null for optional)
3. **Empty Required Fields**: All 10 required fields must have non-empty values
4. **Wrong Array Format**: community_feedback, user_tips, faqs, related_pages must be arrays
5. **Missing FAQ Keys**: FAQ objects must have both `question` and `answer`
6. **Wrong Boolean Format**: Use "Yes" or "No" strings (not boolean true/false)
7. **Wrong File Format**: File must be JSON array `[{...}, {...}]`, not single object
8. **Related Pages Format**: related_pages must be an array of UUID strings (permit IDs), not URLs or comma-separated strings
9. **Invalid ID Format**: `id` field must be a valid UUID format
10. **Invalid Name Format**: `name` field must be exactly 2 words (required field)

---

## Example JSON Files

### Minimal Valid Record (Required fields only)

```json
[
  {
    "id": "2e89cc1d-215d-4281-824b-003bffe05fc6",
    "name": "Business License",
    "agency_short": "NYC DCWP",
    "request_type": "General Business License",
    "description": "",
    "processing_time": "",
    "cost": "$50-$500",
    "how_to_description": "",
    "payment_form_url": "",
    "estimated_monthly_volume": "",
    "deadline_window": "",
    "effort_hours": "2-4 hours",
    "online_available": "Yes",
    "api_available": "No",
    "mcp_available": "",
    "related_pages": [],
    "date_extracted": "2025-11-19",
    "source_url": "https://www.nyc.gov/dcwp",
    "agency_full": "New York City Dept of Consumer and Worker Protection",
    "eligibility": "",
    "location_applicability": "New York City, New York",
    "document_requirements": "",
    "common_mistakes": "",
    "community_feedback": [],
    "user_tips": [],
    "faqs": [],
    "agency_phone": "",
    "agency_email": "",
    "agency_address": "",
    "agency_hours": "",
    "verified_by": ""
  }
]
```

### Rich Record (All fields populated)

```json
[
  {
    "id": "2e89cc1d-215d-4281-824b-003bffe05fc6",
    "name": "Business License",
    "agency_short": "NYC DCWP",
    "request_type": "General Business License",
    "description": "Required for any person or entity doing business in NYC. Covers retail stores, contractors, food vendors, and home-based businesses.",
    "processing_time": "Typically 5-10 business days after application submission",
    "cost": "$50-$500 depending on business size and type",
    "how_to_description": "1. Determine your business license type. 2. Complete the online application. 3. Submit required documents. 4. Pay applicable fees. 5. Receive your license by mail or email.",
    "payment_form_url": "https://a856-eevents.nyc.gov/dca/default_self.aspx",
    "estimated_monthly_volume": "2000-5000",
    "deadline_window": "Licenses must be renewed every 2 years by the expiration date",
    "effort_hours": "2-4 hours",
    "online_available": "Yes",
    "api_available": "No",
    "mcp_available": "No",
    "related_pages": [
      "2e89cc1d-215d-4281-824b-003bffe05fc6",
      "85fef12f-ad0a-464d-ac6c-139fb8a28c67"
    ],
    "date_extracted": "2025-11-19",
    "source_url": "https://www.nyc.gov/site/dcwp/businesses/apply-for-a-license.page",
    "agency_full": "New York City Department of Consumer and Worker Protection",
    "eligibility": "Any person or entity conducting business within NYC city limits",
    "location_applicability": "New York City, New York",
    "document_requirements": "Business Certificate, Sales Tax ID, Federal EIN, Government-issued Photo ID",
    "common_mistakes": "Not having all required documents can delay processing by weeks",
    "community_feedback": [
      "The online portal is very user-friendly",
      "Processing was faster than expected"
    ],
    "user_tips": [
      "Apply early in the day for faster response",
      "Have all documents ready before starting",
      "Use the online portal instead of in-person"
    ],
    "faqs": [
      {
        "question": "How long does processing take?",
        "answer": "Typically 5-10 business days after application submission"
      },
      {
        "question": "Can I apply online?",
        "answer": "Yes, through the NYC Business Portal"
      }
    ],
    "agency_phone": "(212) 436-0000",
    "agency_email": "permits@nyc.gov",
    "agency_address": "42 Broadway, New York, NY 10004",
    "agency_hours": "Monday-Friday 9:00 AM - 5:00 PM",
    "verified_by": "sarah-chen"
  }
]
```

### Multiple Permits in One File

```json
[
  {
    "agency_short": "NYC DCWP",
    "request_type": "General Business License",
    ...
  },
  {
    "agency_short": "NYC DCWP",
    "request_type": "Home Occupation Permit",
    ...
  },
  {
    "agency_short": "NYC DOH",
    "request_type": "Food Service Establishment Permit",
    ...
  }
]
```

---

## Migration from CSV to JSON

### Converting Existing CSV Files

Use Python to convert CSV to JSON:

```python
import pandas as pd
import json

# Read CSV
df = pd.read_csv('data/permits/permits.csv')

# Convert to JSON array
permits = []
for _, row in df.iterrows():
    permit = {}
    for col in df.columns:
        value = row[col]
        # Handle NaN/empty values
        if pd.isna(value):
            if col in ['community_feedback', 'user_tips', 'faqs']:
                permit[col] = []  # Empty array for array fields
            else:
                permit[col] = ""  # Empty string for other fields
        else:
            # Parse JSON string fields back to arrays/objects
            if col in ['community_feedback', 'user_tips', 'faqs', 'related_pages']:
                try:
                    permit[col] = json.loads(value) if value else []
                except:
                    permit[col] = []
            else:
                permit[col] = value
    permits.append(permit)

# Write JSON
with open('data/permits/permits.json', 'w', encoding='utf-8') as f:
    json.dump(permits, f, indent=2, ensure_ascii=False)
```

---

## Questions?

If you encounter schema validation errors:

1. Validate JSON syntax: https://jsonlint.com/
2. Run validation: `python3 generator.py`
3. Run tests: `pytest tests/data/test_json_schema.py -v`
4. Check this documentation for field formats

---

**Schema Maintainer**: News123 Development Team
**Last Schema Change**: 2025-11-19 (Added name field for short 2-word display names)
**Previous Change**: 2025-11-19 (Added 2 fields: description, processing_time)
**Next Review**: As needed for new features
