# PermitIndex Plausible Analytics Events

This document defines all Plausible analytics events tracked across the PermitIndex platform for premium features.

## Page Views

### Pricing Page View
- **Event Name:** `Pricing Page View`
- **Fired When:** User visits `/pricing/`
- **Props:** None
- **Purpose:** Track pricing page traffic

### Coming Soon Page View
- **Event Name:** `Coming Soon Page View`
- **Fired When:** User visits `/coming-soon/`
- **Props:**
  - `referrer`: Document referrer (which page sent them)
  - `feature`: URL parameter indicating which feature (alerts, csv-export, api, historic-data)
- **Purpose:** Track which features drive waitlist interest
- **Example:**
  ```javascript
  plausible('Coming Soon Page View', {
    props: {
      referrer: '/california/contractor-license/',
      feature: 'alerts'
    }
  })
  ```

## Premium Feature CTAs

### Alert CTA Click
- **Event Name:** `Alert CTA Click`
- **Fired When:** User clicks "Subscribe to Alerts" button on permit page
- **Props:**
  - `permit`: Permit slug (e.g., "contractor-license")
  - `has_email`: "yes" or "no" (whether email was entered)
  - `source`: "permit-page"
- **Purpose:** Track interest in email alert feature
- **Example:**
  ```javascript
  plausible('Alert CTA Click', {
    props: {
      permit: 'contractor-license',
      has_email: 'yes',
      source: 'permit-page'
    }
  })
  ```

### Historic Data CTA Click
- **Event Name:** `Historic Data CTA Click`
- **Fired When:** User clicks "Upgrade to Pro" on historic data widget
- **Props:**
  - `permit`: Permit slug
  - `source`: "permit-page"
- **Purpose:** Track interest in historic data feature
- **Example:**
  ```javascript
  plausible('Historic Data CTA Click', {
    props: {
      permit: 'contractor-license',
      source: 'permit-page'
    }
  })
  ```

### CSV Export CTA Click
- **Event Name:** `CSV Export CTA Click`
- **Fired When:** User clicks "Get CSV Access" button
- **Props:**
  - `scope`: Data scope (e.g., "all 50 states", "California", "Contractor Licenses")
  - `permit_count`: Number of permits in scope
  - `source`: Page source ("homepage", "state-page", "category-page")
- **Purpose:** Track interest in CSV export feature
- **Example:**
  ```javascript
  plausible('CSV Export CTA Click', {
    props: {
      scope: 'all 50 states',
      permit_count: 500,
      source: 'homepage'
    }
  })
  ```

### API Access CTA Click
- **Event Name:** `API Access CTA Click`
- **Fired When:** User clicks API access button (Business or Enterprise)
- **Props:**
  - `type`: "business" or "enterprise"
  - `source`: "homepage" (or other pages where widget appears)
- **Purpose:** Track interest in API access
- **Example:**
  ```javascript
  // Business tier
  plausible('API Access CTA Click', {
    props: {
      type: 'business',
      source: 'homepage'
    }
  })

  // Enterprise tier
  plausible('API Access CTA Click', {
    props: {
      type: 'enterprise',
      source: 'homepage'
    }
  })
  ```

## Pricing Page Actions

### Pricing CTA Click
- **Event Name:** `Pricing CTA Click`
- **Fired When:** User clicks any plan CTA on pricing page
- **Props:**
  - `plan`: "Free", "Pro", "Business", or "Enterprise"
- **Purpose:** Track which plans drive most interest
- **Example:**
  ```javascript
  plausible('Pricing CTA Click', {
    props: {
      plan: 'Pro'
    }
  })
  ```

## Waitlist Actions

### Waitlist Signup
- **Event Name:** `Waitlist Signup`
- **Fired When:** User successfully submits waitlist form
- **Props:**
  - `plan`: Selected plan (Pro, Business, Enterprise)
  - `source`: "coming-soon-page"
  - `has_company`: "yes" or "no" (whether company was provided)
- **Purpose:** Track waitlist conversions
- **Example:**
  ```javascript
  plausible('Waitlist Signup', {
    props: {
      plan: 'Pro',
      source: 'coming-soon-page',
      has_company: 'yes'
    }
  })
  ```

### Sales Email Click
- **Event Name:** `Sales Email Click`
- **Fired When:** User clicks "Email Us" mailto link
- **Props:**
  - `plan`: Relevant plan (usually "enterprise")
  - `source`: "coming-soon-page" or other page
- **Purpose:** Track direct sales inquiries
- **Example:**
  ```javascript
  plausible('Sales Email Click', {
    props: {
      plan: 'enterprise',
      source: 'coming-soon-page'
    }
  })
  ```

## Usage & Analysis

### Viewing Events in Plausible

1. **Dashboard:** Visit [https://plausible.io/permitindex.com](https://plausible.io/permitindex.com)
2. **Custom Events:** Click "Goals" in the left sidebar
3. **Filter by Properties:** Click any event to see breakdown by custom properties

### Key Metrics to Track

#### Feature Interest (Before Launch)
- **Most Clicked Features:** Compare event counts for Alert CTA Click, CSV Export CTA Click, API Access CTA Click
- **Conversion Funnel:**
  1. Coming Soon Page View
  2. → CTA Click (alerts/csv/api)
  3. → → Waitlist Signup
- **Source Attribution:** Which permits/pages drive most signups

#### Plan Distribution
- **Waitlist Signup props:** Filter by `plan` property
- **Target:** 60% Pro, 30% Business, 10% Enterprise
- **Action:** If too many Enterprise, may indicate pricing too high

#### Geographic Interest
- **CSV Export props:** Filter by `scope` property
- **Shows:** Which states/categories have most demand
- **Action:** Prioritize data quality for high-demand areas

### Example Queries

**"Which feature drives most signups?"**
- View: Waitlist Signup event
- Group by: `props.plan`
- Compare: Alert vs CSV vs API sources

**"What's our pricing page conversion rate?"**
- Funnel: Pricing Page View → Pricing CTA Click → Coming Soon Page View → Waitlist Signup
- Target: 20-30% pricing-to-waitlist conversion

**"Which permits generate most Pro interest?"**
- View: Alert CTA Click (Pro feature)
- Group by: `props.permit`
- Top 10 = Focus areas for launch

**"Business vs Enterprise API interest?"**
- View: API Access CTA Click
- Group by: `props.type`
- Ratio: Business should be 3-5x Enterprise

## Integration Notes

### Adding Plausible to New Pages

All new pages must include the Plausible script in `<head>`:

```html
<!-- Privacy-friendly analytics by Plausible -->
<script async src="https://plausible.io/js/pa-ag6g5Gg1btKfcdZ4oA-vo.js"></script>
<script>
  window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
  plausible.init()
</script>
```

### Firing Custom Events

```javascript
// Basic event (no properties)
plausible('Event Name')

// Event with properties
plausible('Event Name', {
  props: {
    property1: 'value1',
    property2: 'value2'
  }
})

// Always check if plausible is defined
if (typeof plausible !== 'undefined') {
  plausible('Event Name', { props: { ... } })
}
```

### Testing Events Locally

1. Open browser console
2. Visit a page with Plausible installed
3. Type: `plausible('Test Event', { props: { test: 'value' } })`
4. Check Plausible dashboard (may take 30s to appear)

## Privacy & Compliance

- **No PII:** Never track email addresses, names, or personal information in event properties
- **No Cookies:** Plausible is cookieless and GDPR-compliant
- **Opt-out:** Users can block Plausible script via browser settings
- **Data Retention:** 24 months (Plausible default)

## Support & Troubleshooting

**Events not appearing?**
- Check browser console for errors
- Verify Plausible script loads (Network tab)
- Ensure `plausible` function exists: `typeof plausible` should return "function"
- Check Goals are configured in Plausible dashboard

**Property values truncated?**
- Plausible limits property values to 500 characters
- Keep slugs and values short (<100 chars ideal)

**Need new events?**
- Add event name to this document
- Define props clearly
- Test in production
- Add to Plausible Goals (automatic after first fire)
