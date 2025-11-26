# PermitIndex CSV Schema Documentation

This document defines the complete data schema for permits in the PermitIndex system.

## Schema Version: 3.0 (29 columns)

Last Updated: 2025-11-19

---

## File Organization

As of 2025-11-19, CSV files are organized into subdirectories:

- **`data/permits/`** - Permit CSV files (supports multiple files that will be combined)
- **`data/feedback/`** - User feedback CSV file(s)
- **`data/contributors/`** - Contributor profile CSV file(s)

**Note**: You can add multiple permit CSV files to `data/permits/` and they will all be loaded and combined into one dataset. This allows for modular organization by state, region, or category.

---

## Schema Overview

Permit CSV files in **`data/permits/`** must contain **29 columns** in the exact order specified below.

- **8 Required Columns**: Must have data for every permit
- **21 Optional Columns**: Enrich content quality when provided

### Quick Stats
- **Total Columns**: 29
- **Required**: 8 (marked with ⚠️)
- **Optional**: 21 (marked with ✅)
- **JSON Format**: 3 (community_feedback, user_tips, faqs)

---

## Complete Column Reference

### 1. Core Identification (3 columns)

#### `agency_short` ⚠️ REQUIRED
- **Type**: Text
- **Description**: Short agency name or abbreviation
- **Example**: `"NYC DCWP"`, `"LA Office of Finance"`
- **Validation**: Cannot be empty

#### `agency_full` ⚠️ REQUIRED
- **Type**: Text
- **Description**: Full official agency name
- **Example**: `"New York City Department of Consumer and Worker Protection"`
- **Validation**: Cannot be empty

#### `request_type` ⚠️ REQUIRED
- **Type**: Text
- **Description**: Type of permit or license
- **Example**: `"General Business License"`, `"Business Tax Registration Certificate"`
- **Validation**: Cannot be empty

#### `description` ✅ Optional
- **Type**: Text (Long)
- **Description**: Detailed description of what the permit covers and who it applies to
- **Example**: `"This applies to any individual or entity conducting business within Anchorage city limits, including home-based businesses, contractors, and retail operations."`
- **Best Practice**: Provide context about the permit's scope and applicability
- **Validation**: None (can be empty)
- **Used In**: Transaction pages, jurisdiction hub pages

#### `processing_time` ✅ Optional
- **Type**: Text
- **Description**: How long it takes to process the application
- **Example**: `"Typically 5 to 10 business days after application submission."`, `"2-4 weeks"`
- **Fallback**: If not provided, system falls back to `effort_hours` field
- **Validation**: None (can be empty)
- **Used In**: Transaction pages, jurisdiction hub pages

---

### 2. Process Details (3 columns)

#### `cost` ⚠️ REQUIRED
- **Type**: Text
- **Description**: Fee information (can describe ranges or variables)
- **Example**: `"Varies by license type. Fees can range from under $100 to several hundred dollars."`
- **Validation**: Cannot be empty

#### `how_to_description` ✅ Optional
- **Type**: Text (Long)
- **Description**: Step-by-step instructions for applying
- **Example**: `"Step 1: Use the Step-by-Step tool... Step 2: Gather all necessary documents..."`
- **Best Practice**: Use numbered steps for clarity
- **Validation**: None (can be empty)

#### `payment_form_url` ✅ Optional
- **Type**: URL
- **Description**: Direct link to application or payment form
- **Example**: `"https://a856-eevents.nyc.gov/dca/default_self.aspx"`
- **Validation**: Should be valid URL if provided

---

### 3. Eligibility & Scope (3 columns)

#### `eligibility` ✅ Optional
- **Type**: Text
- **Description**: Who can apply and any requirements
- **Example**: `"Applicants must typically be at least 18 years old and have a legally registered business."`
- **Validation**: None (can be empty)

#### `location_applicability` ⚠️ REQUIRED
- **Type**: Text
- **Description**: Geographic scope where permit is valid
- **Example**: `"New York City, New York"`, `"City of Los Angeles, California"`
- **Validation**: Cannot be empty

#### `document_requirements` ✅ Optional
- **Type**: Text (Comma-separated list)
- **Description**: Required documents for application
- **Example**: `"Business Certificate, Sales Tax ID, Federal EIN, Government-issued Photo ID"`
- **Best Practice**: Use comma separation for clarity
- **Validation**: None (can be empty)

---

### 4. Volume & Timing (3 columns)

#### `estimated_monthly_volume` ✅ Optional
- **Type**: Text (Range)
- **Description**: Approximate number of monthly applications
- **Example**: `"2000-5000"`, `"500-1500"`
- **Format**: Use hyphen for ranges
- **Validation**: None (can be empty)

#### `deadline_window` ✅ Optional
- **Type**: Text
- **Description**: Renewal periods, deadlines, or time windows
- **Example**: `"Licenses typically need to be renewed every 2 years."`
- **Validation**: None (can be empty)

#### `effort_hours` ⚠️ REQUIRED
- **Type**: Text (Range or estimate)
- **Description**: Estimated time to complete application
- **Example**: `"3-8 hours"`, `"Less than 1 hour"`, `"1-2 hours"`
- **Validation**: Cannot be empty

---

### 5. Availability Flags (3 columns)

#### `online_available` ⚠️ REQUIRED
- **Type**: Boolean Text
- **Description**: Whether application can be completed online
- **Values**: `"Yes"` or `"No"`
- **Validation**: Cannot be empty

#### `api_available` ⚠️ REQUIRED
- **Type**: Boolean Text
- **Description**: Whether agency provides API access
- **Values**: `"Yes"` or `"No"`
- **Validation**: Cannot be empty

#### `mcp_available` ✅ Optional
- **Type**: Boolean Text
- **Description**: Whether MCP (Model Context Protocol) integration exists
- **Values**: `"Yes"` or `"No"` (can be empty)
- **Validation**: None

---

### 6. Community Content (4 columns) - ENRICHES PAGES

These columns accept **JSON array format** when populated.

#### `common_mistakes` ✅ Optional
- **Type**: Text
- **Description**: Common errors applicants make
- **Example**: `"Not having all required documents can delay processing by weeks."`
- **Validation**: Plain text (not JSON)

#### `community_feedback` ✅ Optional
- **Type**: JSON Array
- **Description**: User feedback and reviews
- **Format**:
```json
["Feedback item 1", "Feedback item 2", "Feedback item 3"]
```
- **Validation**: Must be valid JSON array if not empty

#### `user_tips` ✅ Optional
- **Type**: JSON Array
- **Description**: Helpful tips from users who completed the process
- **Format**:
```json
["Tip 1: Apply early in the morning", "Tip 2: Have all docs ready", "Tip 3: Use the online portal"]
```
- **Validation**: Must be valid JSON array if not empty

#### `faqs` ✅ Optional
- **Type**: JSON Array of Objects
- **Description**: Frequently asked questions with answers
- **Format**:
```json
[
  {"question": "How long does processing take?", "answer": "Typically 2-4 weeks."},
  {"question": "Can I apply online?", "answer": "Yes, through the city portal."}
]
```
- **Validation**: Must be valid JSON array of objects, each with `question` and `answer` keys

---

### 7. Agency Contact (4 columns) - HELPS USERS

#### `agency_phone` ✅ Optional
- **Type**: Phone Number
- **Description**: Agency contact phone number
- **Example**: `"(212) 436-0000"`, `"800-555-1234"`
- **Validation**: None (any format accepted)

#### `agency_email` ✅ Optional
- **Type**: Email Address
- **Description**: Agency contact email
- **Example**: `"permits@nyc.gov"`
- **Validation**: Should be valid email if provided

#### `agency_address` ✅ Optional
- **Type**: Text (Address)
- **Description**: Physical office address
- **Example**: `"42 Broadway, New York, NY 10004"`
- **Validation**: None

#### `agency_hours` ✅ Optional
- **Type**: Text
- **Description**: Office hours for in-person visits
- **Example**: `"Monday-Friday 9:00 AM - 5:00 PM"`
- **Validation**: None

---

### 8. Metadata (3 columns)

#### `related_pages` ✅ Optional
- **Type**: Text (Comma-separated slugs)
- **Description**: Slugs of related permits (for cross-linking)
- **Example**: `"nyc-register-business-entity,get-federal-employer-identification-number-ein"`
- **Format**: Use comma separation, no spaces
- **Validation**: None

#### `date_extracted` ✅ Optional
- **Type**: Date (YYYY-MM-DD)
- **Description**: When this data was collected
- **Example**: `"2025-11-17"`
- **Format**: ISO date format preferred
- **Validation**: None

#### `source_url` ✅ Optional
- **Type**: URL
- **Description**: Original source where data was found
- **Example**: `"https://www.nyc.gov/site/dcwp/businesses/apply-for-a-license.page"`
- **Validation**: Should be valid URL if provided

---

### 9. Contributor System (1 column)

#### `verified_by` ✅ Optional
- **Type**: Text (Contributor ID)
- **Description**: ID of contributor who verified this permit
- **Example**: `"sarah-chen"` (matches contributor_id in contributors.csv)
- **Validation**: Should match a contributor_id if provided
- **Special**: Empty means permit is unclaimed (shows "Claim This Page" widget)

---

## Validation Rules

### Automated Validation (generator.py)

The generator.py script validates:

1. **Column Count**: Must have exactly 29 columns
2. **Column Order**: Must match schema exactly
3. **Required Fields**: 8 required columns cannot be empty
4. **JSON Format**: community_feedback, user_tips, faqs must be valid JSON arrays
5. **FAQ Structure**: faqs must have `question` and `answer` keys
6. **Duplicate Check**: No duplicate permit-agency combinations

### Automated Tests (tests/data/test_csv_schema.py)

Pytest validates:

1. ✅ File exists
2. ✅ Has exactly 29 columns in correct order
3. ✅ Valid UTF-8 encoding
4. ✅ Required columns not empty
5. ✅ JSON columns have valid format

### Running Validation

```bash
# Run generator validation
python3 generator.py

# Run automated tests
pytest tests/data/test_csv_schema.py -v

# Run critical tests only
pytest tests/data/test_csv_schema.py -m critical -v
```

---

## Common Mistakes to Avoid

1. **Wrong Column Count**: Schema requires exactly 29 columns
2. **Wrong Order**: Columns must be in exact order specified
3. **Empty Required Fields**: All 8 required columns must have data
4. **Invalid JSON**: JSON columns must be valid arrays (use online JSON validator)
5. **Missing FAQ Keys**: FAQs must have both `question` and `answer`
6. **Wrong Boolean Format**: Use "Yes" or "No" (not "true"/"false")

---

## Migration from Previous Schema

If you have permits.csv from an older schema:

### From 27 columns → 29 columns (Added 2 columns)

**Added columns** (both optional):
- `description` - Detailed description of what the permit covers
- `processing_time` - How long it takes to process the application

**Action required**: Add these 2 columns to your CSV header (can be empty initially). Note: Column order has changed - see schema above for new positions.

### From 19 columns → 27 columns (Added 8 columns)

**Added columns** (all optional):
- common_mistakes
- community_feedback
- user_tips
- faqs
- agency_phone
- agency_email
- agency_address
- agency_hours

**Action required**: Add these 8 columns to your CSV header (can be empty initially)

---

## Examples

### Minimal Valid Record (Required fields only)

```csv
agency_short,request_type,description,processing_time,cost,how_to_description,payment_form_url,estimated_monthly_volume,deadline_window,effort_hours,online_available,api_available,mcp_available,related_pages,date_extracted,source_url,agency_full,eligibility,location_applicability,document_requirements,common_mistakes,community_feedback,user_tips,faqs,agency_phone,agency_email,agency_address,agency_hours,verified_by
NYC DCWP,General Business License,,,,$50-$500,,,,,2-4 hours,Yes,No,,,2025-11-19,https://www.nyc.gov/dcwp,New York City Dept of Consumer and Worker Protection,,"New York City, New York",,,,,,,,,
```

### Rich Record (All fields populated)

See `data/permits/permits.csv` for real-world examples with all fields populated.

---

## Questions?

If you encounter schema validation errors:

1. Check column count: `head -1 data/permits/permits.csv | awk -F',' '{print NF}'`
2. Run validation: `python3 generator.py`
3. Run tests: `pytest tests/data/test_csv_schema.py -v`
4. Check this documentation for field formats
5. Validate JSON online: https://jsonlint.com/

---

**Schema Maintainer**: PermitIndex Development Team
**Last Schema Change**: 2025-11-19 (Added 2 columns: description, processing_time; column order changed)
**Previous Change**: 2025-11-17 (Added 8 community/contact columns)
**Next Review**: As needed for new features
