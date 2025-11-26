# PermitIndex Developer Guide
**Version:** 1.0
**Last Updated:** November 2024

---

## Table of Contents

1. [Brand Color System](#brand-color-system)
2. [Quick Reference](#quick-reference)
3. [Usage Examples](#usage-examples)
4. [Component Patterns](#component-patterns)
5. [Accessibility Guidelines](#accessibility-guidelines)
6. [Common Mistakes](#common-mistakes)
7. [Testing](#testing)

---

## Brand Color System

### Overview

PermitIndex uses a strict brand color system defined in `/static/css/variables.css`. **All colors must use CSS variables** to ensure brand consistency.

### Color Philosophy

- **Primary Blue (#003366):** Trust, authority, professionalism
- **Accent Orange (#FF6B35):** Action, urgency (use sparingly!)
- **Neutrals:** High-contrast, accessibility-first

### File Locations

- `/static/css/variables.css` - CSS variable definitions
- `/docs/BRAND_GUIDELINES.md` - Complete brand guidelines
- `/AUDIT.md` - Current compliance status
- `/docs/IMPLEMENTATION_GUIDE.md` - Technical implementation

---

## Quick Reference

### Primary Colors

```css
/* Primary Blue - Headers, links, primary buttons */
color: var(--primary);              /* #003366 */
background: var(--primary);

/* Accent Orange - CTAs only! */
color: var(--accent);               /* #FF6B35 */
background: var(--accent);
```

### Text Colors

```css
/* Dark text - Body copy, headings */
color: var(--text);                 /* #1a1a1a */

/* Light text - Secondary info, labels */
color: var(--text-light);           /* #666666 */
```

### Backgrounds

```css
/* White - Cards, content boxes */
background: var(--bg);              /* #ffffff */

/* Light - Page background */
background: var(--bg-light);        /* #f8f9fa */
```

### Borders & Status

```css
/* Border - Dividers, separators */
border-color: var(--border);        /* #e0e0e0 */

/* Success - Online available badges */
background: var(--success);         /* #10b981 */

/* Warning - Caution indicators */
background: var(--warning);         /* #F59E0B */

/* Error - Critical alerts */
background: var(--error);           /* #EF4444 */
```

---

## Usage Examples

### Basic HTML Element Styling

#### ✅ CORRECT - Using CSS Variables

```html
<!-- Body tag -->
<body style="background: var(--bg-light); color: var(--text);">

<!-- Headers -->
<h1 style="color: var(--primary);">Page Title</h1>
<h2 style="color: var(--primary);">Section Title</h2>

<!-- Paragraphs -->
<p style="color: var(--text);">Main content text...</p>
<p style="color: var(--text-light);">Secondary information...</p>

<!-- Links -->
<a href="#" style="color: var(--primary);">Click here</a>

<!-- Buttons -->
<button style="background: var(--accent); color: white;">
  Apply Now
</button>

<button style="background: var(--primary); color: white;">
  Learn More
</button>

<!-- Cards -->
<div style="background: var(--bg); border: 1px solid var(--border);">
  Card content
</div>

<!-- Breadcrumbs -->
<nav style="background: var(--bg-light); border-bottom: 1px solid var(--border);">
  <a href="/" style="color: var(--primary);">Home</a>
  <span style="color: var(--text-light);">/</span>
  <span style="color: var(--text);">Current Page</span>
</nav>
```

#### ❌ INCORRECT - Hardcoded Colors

```html
<!-- DON'T use Tailwind color classes -->
<body class="bg-gray-50 text-gray-900">
<h1 class="text-blue-600">Title</h1>
<p class="text-gray-700">Text</p>
<a href="#" class="text-blue-600 hover:text-blue-700">Link</a>

<!-- DON'T use hex codes directly -->
<div style="background: #f8f9fa; color: #1a1a1a;">
<button style="background: #FF6B35;">Button</button>
```

### Using RGB Variants for Transparency

```html
<!-- Semi-transparent overlay -->
<div style="background: rgba(var(--primary-rgb), 0.9);">
  Overlay content
</div>

<!-- Transparent text -->
<p style="color: rgba(var(--text-rgb), 0.7);">
  Faded text
</p>

<!-- Transparent border -->
<div style="border: 1px solid rgba(var(--border-rgb), 0.5);">
  Content
</div>
```

---

## Component Patterns

### Buttons

```html
<!-- Primary CTA (Orange) -->
<button class="star-button" style="background: var(--accent); color: white;">
  Apply Now
</button>

<!-- Secondary (Blue) -->
<button class="star-button secondary" style="background: var(--primary); color: white;">
  Learn More
</button>

<!-- Outline -->
<button class="star-button outline" style="background: white; color: var(--primary); border: 2px solid var(--primary);">
  View Details
</button>
```

### Cards

```html
<!-- Standard card with star cutout -->
<div class="star-box" style="background: var(--bg); padding: 30px;">
  Card content
</div>

<!-- Bordered card -->
<div class="star-box bordered" style="background: var(--bg); border: 2px solid var(--border);">
  Card content
</div>

<!-- Colored card -->
<div class="star-box primary" style="background: var(--primary); color: white;">
  Colored card content
</div>
```

### Status Badges

```html
<!-- Online Available -->
<span class="status-badge online" style="background: var(--success); color: white;">
  ✅ Online
</span>

<!-- API Available -->
<span class="status-badge api" style="background: var(--primary); color: white;">
  🔌 API
</span>

<!-- In-Person Required -->
<span class="status-badge inperson" style="background: var(--accent); color: white;">
  👤 In-Person
</span>
```

### Info Cards (Statistics)

```html
<div class="info-card">
  <div class="info-value" style="color: var(--primary);">$500</div>
  <div class="info-label" style="color: var(--text-light);">COST</div>
</div>
```

### Navigation

```html
<!-- Header navigation -->
<nav>
  <a href="/" style="color: var(--text-light);"
     onmouseover="this.style.color='var(--primary)'"
     onmouseout="this.style.color='var(--text-light)'">
    Home
  </a>
</nav>

<!-- Breadcrumbs -->
<nav style="background: var(--bg-light); border-bottom: 1px solid var(--border);">
  <a href="/" style="color: var(--primary);">Home</a>
  <span style="color: var(--text-light);">/</span>
  <a href="/state/" style="color: var(--primary);">State</a>
  <span style="color: var(--text-light);">/</span>
  <span style="color: var(--text);">Current Page</span>
</nav>
```

---

## Accessibility Guidelines

### Color Contrast Requirements

All PermitIndex colors meet **WCAG 2.1 Level AA** requirements:

| **Combination** | **Contrast Ratio** | **Status** |
|-----------------|-------------------|------------|
| Primary (#003366) on White | 12.63:1 | ✅ AAA |
| Accent (#FF6B35) on White | 3.58:1 | ✅ AA |
| Text Dark (#1a1a1a) on White | 15.77:1 | ✅ AAA |
| Text Light (#666666) on White | 5.74:1 | ✅ AA |

### Best Practices

#### ✅ DO

```html
<!-- Use sufficient contrast -->
<div style="background: var(--bg); color: var(--text);">
  High contrast text
</div>

<!-- Use solid colors for text -->
<p style="color: var(--text);">Readable text</p>

<!-- Provide alternative cues beyond color -->
<span style="color: var(--success);">
  ✅ Available  <!-- Icon + color -->
</span>
```

#### ❌ DON'T

```html
<!-- Don't use low opacity on text -->
<p style="color: rgba(var(--text-rgb), 0.3);">
  Too faint! <!-- Fails contrast requirements -->
</p>

<!-- Don't use accent orange for large text blocks -->
<div style="background: var(--accent); color: white;">
  <p>Long paragraph... <!-- Too intense for reading -->
</p>
</div>

<!-- Don't rely on color alone -->
<span style="color: var(--error);">
  Error  <!-- Need icon or text indicator too -->
</span>
```

### Testing Contrast

```bash
# Use online tools to verify:
# https://webaim.org/resources/contrastchecker/

# Or browser DevTools:
# Chrome DevTools > Elements > Styles > Color picker shows contrast ratio
```

---

## Star Cutout Color Rules

### The Golden Rule: Stars Must Match Borders

**CRITICAL:** When using star cutouts with borders, the star background color MUST always match the border color.

### Why This Matters

- Mismatched colors look unprofessional
- Breaks visual consistency
- Creates confusing visual hierarchy
- Makes the site appear poorly maintained

### Correct Implementation

#### ✅ With Border - Star Matches Border

```html
<!-- Blue border = Blue star -->
<div class="alert-info">
    Content
</div>

<style>
.alert-info {
    background: rgba(0,51,102,0.05);
    border: 2px solid var(--primary);  /* Blue border */
    border-radius: 12px;
    position: relative;
    overflow: hidden;
}

.alert-info::before {
    content: '';
    position: absolute;
    top: -8px;
    right: 18px;
    width: 18px;
    height: 18px;
    background: var(--primary);  /* Blue star - MATCHES! */
    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}
</style>
```

#### ✅ Without Border - Star Matches Page Background

```html
<!-- No border = Page background star -->
<div class="star-box">
    Content
</div>

<style>
.star-box {
    background: white;
    border-radius: 12px;
    position: relative;
}

.star-box::before {
    background: var(--bg-light);  /* Page background #f8f9fa */
    /* Creates cutout effect revealing page behind */
}
</style>
```

### Alert Components with Color Harmony

```css
/* Warning Alert - Yellow/Orange */
.alert-warning {
    background: rgba(245,158,11,0.1);
    border: 2px solid var(--warning);  /* Orange */
    /* ... */
}
.alert-warning::before {
    background: var(--warning);  /* MUST match border */
}

/* Success Alert - Green */
.alert-success {
    background: rgba(16,185,129,0.1);
    border: 2px solid var(--success);  /* Green */
}
.alert-success::before {
    background: var(--success);  /* MUST match border */
}

/* Error Alert - Red */
.alert-error {
    background: rgba(239,68,68,0.1);
    border: 2px solid var(--error);  /* Red */
}
.alert-error::before {
    background: var(--error);  /* MUST match border */
}
```

### Common Color Pairings

| Border Color | Star Background | Use Case |
|---|---|---|
| `var(--primary)` #003366 | `var(--primary)` | Primary info boxes |
| `var(--accent)` #FF6B35 | `var(--accent)` | CTA/featured boxes |
| `var(--warning)` #F59E0B | `var(--warning)` | Warning/caution boxes |
| `var(--success)` #10b981 | `var(--success)` | Success/tip boxes |
| `var(--error)` #EF4444 | `var(--error)` | Error/danger boxes |
| `var(--border)` #E0E0E0 | `var(--border)` | Neutral bordered boxes |
| None (no border) | `var(--bg-light)` | Standard white cards |

### Incorrect Examples (DON'T DO THIS)

#### ❌ Mismatched Colors

```html
<!-- WRONG: Blue border with orange star -->
<div style="border: 2px solid var(--primary);">
    Content
</div>
<style>
div::before {
    background: var(--accent);  /* ❌ Doesn't match border! */
}
</style>

<!-- WRONG: Warning border with gray star -->
<div class="star-box bordered" style="border-color: var(--warning);">
    <!-- The default .star-box.bordered uses var(--border) for star -->
    <!-- This creates a mismatch! Need custom class instead -->
</div>
```

### How to Fix Existing Violations

1. **Identify the border color** - Check inline styles or CSS class
2. **Match the star background** - Use the SAME color variable
3. **Test visually** - Open `/test/star-color-test.html` for reference
4. **Use alert classes** - Prefer `.alert-warning`, `.alert-success`, etc.

### Testing

```bash
# Generate test page
python3 generator.py

# View in browser
open output/test/star-color-test.html
```

The test page shows correct and incorrect examples side-by-side.

---

## Common Mistakes

### Mistake #1: Using Tailwind Color Classes

```html
<!-- ❌ WRONG -->
<div class="bg-gray-50 text-gray-900">
<p class="text-blue-600">Text</p>

<!-- ✅ CORRECT -->
<div style="background: var(--bg-light); color: var(--text);">
<p style="color: var(--primary);">Text</p>
```

### Mistake #2: Hardcoding Hex Values

```html
<!-- ❌ WRONG -->
<div style="background: #003366;">

<!-- ✅ CORRECT -->
<div style="background: var(--primary);">
```

### Mistake #3: Creating One-Off Colors

```html
<!-- ❌ WRONG -->
<div style="background: #E6F0FF;"> <!-- Undefined color! -->

<!-- ✅ CORRECT -->
<!-- Either use existing variable OR add to variables.css first -->
<div style="background: var(--primary-light);"> <!-- After defining it -->
```

### Mistake #4: Overusing Accent Orange

```html
<!-- ❌ WRONG -->
<h1 style="color: var(--accent);">Title</h1>
<p style="color: var(--accent);">Paragraph</p>
<button style="background: var(--accent);">Button 1</button>
<button style="background: var(--accent);">Button 2</button>

<!-- ✅ CORRECT -->
<h1 style="color: var(--primary);">Title</h1>
<p style="color: var(--text);">Paragraph</p>
<button style="background: var(--accent);">Primary CTA</button> <!-- Only one! -->
<button style="background: var(--primary);">Secondary</button>
```

### Mistake #5: Inconsistent Variable Usage

```html
<!-- ❌ WRONG - Mixed approaches -->
<div class="bg-white text-gray-900">
  <h2 style="color: var(--primary);">Title</h2>
  <p class="text-gray-600">Content</p>
</div>

<!-- ✅ CORRECT - Consistent variables -->
<div style="background: var(--bg); color: var(--text);">
  <h2 style="color: var(--primary);">Title</h2>
  <p style="color: var(--text-light);">Content</p>
</div>
```

---

## Testing

### Visual Testing

1. **Generate test page:**
   ```bash
   python3 generator.py
   cd output/test
   open brand-colors-test.html
   ```

2. **Check all colors match brand guidelines**
3. **Verify responsive behavior**
4. **Test with browser DevTools color picker**

### Automated Testing

```bash
# Run brand compliance tests
cd ~/Downloads/permit-index-site
python3 tests/brand_compliance_test.py

# Expected output:
# ✅ Logo present and correctly colored
# ✅ Found N elements with star cutouts
# ✅ CSS variables correctly defined
# ✅ Typography correct
# ✅ Branded buttons present
# ✅ Accessibility attributes present
# ✅ Responsive scaling works
```

### Manual Checklist

Before committing template changes:

- [ ] No Tailwind color classes (`text-blue-*`, `bg-gray-*`, etc.)
- [ ] No hardcoded hex values
- [ ] All colors use CSS variables from `variables.css`
- [ ] Contrast ratios meet WCAG AA minimum
- [ ] Accent orange used sparingly (CTAs only)
- [ ] Page background uses `var(--bg-light)`
- [ ] Text uses `var(--text)` or `var(--text-light)`
- [ ] Borders use `var(--border)`
- [ ] Test page renders correctly locally

---

## Adding New Colors

If you need a color not in the current system:

1. **Check if existing colors work first**
   - Can you use `var(--primary)` with opacity?
   - Can you use an existing variable?

2. **If truly needed, update `variables.css`:**
   ```css
   /* Add to variables.css */
   :root {
     --new-color-name: #hexcode;
     --new-color-name-rgb: r, g, b;
   }
   ```

3. **Document in brand guidelines:**
   - Update `/docs/BRAND_GUIDELINES.md`
   - Specify usage rules
   - Test accessibility

4. **Get approval before deploying**

---

## Migration Guide

### Converting Existing Templates

**Step 1:** Find and replace Tailwind classes

```bash
# In your editor, find/replace:
text-gray-900       → var(--text)
text-gray-700       → var(--text)
text-gray-600       → var(--text-light)
text-gray-500       → var(--text-light)
text-blue-600       → var(--primary)
text-blue-700       → var(--primary)
bg-gray-50          → var(--bg-light)
bg-gray-100         → var(--bg-light)
bg-white            → var(--bg)
border-gray-200     → var(--border)
bg-blue-600         → var(--primary)
```

**Step 2:** Convert class attributes to style attributes

```html
<!-- Before -->
<div class="bg-gray-50 text-gray-900 border-gray-200">

<!-- After -->
<div style="background: var(--bg-light); color: var(--text); border-color: var(--border);">
```

**Step 3:** Test locally

```bash
python3 generator.py
cd output && python3 -m http.server 8000
# Visit http://localhost:8000
```

**Step 4:** Run automated tests

```bash
python3 tests/brand_compliance_test.py
```

---

## Resources

- **Brand Guidelines:** `/docs/BRAND_GUIDELINES.md`
- **Implementation Guide:** `/docs/IMPLEMENTATION_GUIDE.md`
- **CSS Variables:** `/static/css/variables.css`
- **Current Audit:** `/AUDIT.md`
- **Test Page:** `/output/test/brand-colors-test.html`

---

## Getting Help

### Questions about color usage?

1. Check `/docs/BRAND_GUIDELINES.md` first
2. Review examples in this document
3. Look at existing compliant components
4. Check `/AUDIT.md` for known issues

### Found a brand violation?

1. Document it in `/AUDIT.md`
2. Fix it using this guide
3. Test with automated tests
4. Commit with clear message

### Need a new color?

1. Confirm it's truly needed
2. Check accessibility requirements
3. Add to `/static/css/variables.css`
4. Update `/docs/BRAND_GUIDELINES.md`
5. Get team approval

---

## Changelog

**v1.0 - November 2024**
- Initial documentation created
- CSS variables system established
- Brand compliance audit completed
- Developer guide published

---

**Last Updated:** November 14, 2024
**Maintained By:** PermitIndex Team
**Questions?** See `/docs/BRAND_GUIDELINES.md` or create an issue
