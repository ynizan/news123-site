# Premium Features Testing Checklist

## Generator Tests

- [ ] Run `python3 generator.py` successfully
- [ ] Check `output/pricing/index.html` exists
- [ ] Check `output/coming-soon/index.html` exists
- [ ] All permit pages have alert and historic data widgets
- [ ] Homepage has CSV export and API access widgets

## Page Load Tests

- [ ] `/pricing/` loads without errors
- [ ] `/coming-soon/` loads without errors
- [ ] Sample permit page loads with widgets visible
- [ ] Homepage loads with widgets visible

## Link Tests

- [ ] All "Upgrade to Pro" buttons → `/coming-soon/`
- [ ] All "Get API Access" buttons → `/coming-soon/` or mailto
- [ ] "Talk to Us" button → `mailto:sales@ainews123.com`
- [ ] Pricing page CTAs → `/coming-soon/`
- [ ] All links preserve URL parameters (`?feature=X`)

## Analytics Tests (Check Plausible Dashboard)

- [ ] Pricing Page View event fires
- [ ] Coming Soon Page View event fires with referrer
- [ ] Alert CTA Click fires with permit name
- [ ] Historic Data CTA Click fires
- [ ] CSV Export CTA Click fires with scope
- [ ] API Access CTA Click fires (both business and enterprise)
- [ ] Pricing CTA Click fires for each tier
- [ ] Waitlist Signup fires on form submit

## Waitlist Form Tests

- [ ] Form submits successfully
- [ ] GitHub Issue created with correct title format
- [ ] Issue has labels: `waitlist` and `plan-X`
- [ ] Issue body contains all form data
- [ ] Success message displays
- [ ] Plausible event fires

## Mobile Tests

- [ ] All widgets responsive on mobile (375px width)
- [ ] Buttons accessible and clickable
- [ ] Forms usable on mobile
- [ ] No horizontal scrolling
- [ ] Text readable (font size >= 14px)

## Visual Tests

- [ ] Brand colors correct (#003366, #FF6B35)
- [ ] "PRO FEATURE" badges visible
- [ ] Icons render properly
- [ ] Spacing/padding consistent
- [ ] No layout breaks or overlaps

## URL Parameter Tests

- [ ] `/coming-soon/?feature=alerts` displays correctly
- [ ] `/coming-soon/?permit=California+Contractor` preserves permit name
- [ ] Email parameter pre-fills form if present
- [ ] Multiple parameters work together

## Cross-Browser Tests

- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)
