# News123 Brand Guidelines

**Version 1.0 | November 2024**

---

## Table of Contents

1. [Brand Overview](#brand-overview)
2. [Logo System](#logo-system)
3. [Color Palette](#color-palette)
4. [Typography](#typography)
5. [Visual Elements](#visual-elements)
6. [Design Patterns](#design-patterns)
7. [Usage Examples](#usage-examples)
8. [Don'ts](#donts)

---

## Brand Overview

### Brand Essence

**News123** is the comprehensive database of US government transactions, permits, and applications. We provide infrastructure that makes government interactions simple, transparent, and accessible.

### Positioning
- **What we are:** Developer infrastructure for government transactions ("Stripe for government")
- **Not:** A consumer-facing permit service or government agency
- **Tone:** Professional, authoritative, data-focused, transparent

### Target Audience
1. Startups building government-facing applications
2. Tech companies whose customers struggle with bureaucracy
3. Enterprise IT developing government automation software

---

## Logo System

### Primary Logo: Horizontal Wordmark

**Logo Features:**
- Wordmark: "News123" (one word, no space)
- Star cutout from top-right corner of "P"
- Font: Arial Black (or similar heavy sans-serif)
- Letter spacing: -1px for tight, modern look

**File Format:**
- Web: Inline SVG (best SEO)
- Social/Print: Download from logo suite

**Logo Variations:**

#### 1. Horizontal Logo (Primary)
- **Use for:** Website headers, email signatures, presentations, documentation
- **Minimum size:** 120px width
- **Formats:** SVG (web), PNG (social media)

#### 2. Icon/Favicon
- **Use for:** Browser tabs, app icons, social media avatars
- **Minimum size:** 16px width
- **Formats:** SVG, PNG (16x16, 32x32, 64x64, 512x512)

### Logo Colors

**Primary Logo Colors:**
- Light backgrounds: Primary Blue (#003366)
- Dark backgrounds: White (#FFFFFF)

**When NOT to use:**
- Never use accent orange (#FF6B35) for logo
- Never use gradients
- Never add effects (shadows, glows, etc.)

### Clear Space

Maintain clear space around logo equal to the height of the "P":
```
[    P    ] ← Clear space = height of P on all sides
```

### Logo Don'ts
❌ Don't stretch or distort
❌ Don't rotate
❌ Don't change colors outside defined palette
❌ Don't add effects or borders
❌ Don't place on busy backgrounds
❌ Don't recreate or modify the star cutout

---

## Color Palette

### Primary Palette: Gov Blue + Safety Orange

Our chosen palette conveys authority (government blue) combined with urgency and action (safety orange).

#### Primary Blue
- **Hex:** #003366
- **RGB:** 0, 51, 102
- **Usage:** Logo, headers, primary buttons, links, borders, primary content boxes
- **Represents:** Trust, authority, government, professionalism

#### Accent Orange
- **Hex:** #FF6B35
- **RGB:** 255, 107, 53
- **Usage:** Call-to-action buttons, important highlights, featured content, status badges
- **Represents:** Attention, urgency, action, accessibility

#### Neutrals

**Text Dark**
- **Hex:** #1a1a1a
- **RGB:** 26, 26, 26
- **Usage:** Body text, headings

**Text Light**
- **Hex:** #666666
- **RGB:** 102, 102, 102
- **Usage:** Secondary text, meta information, labels

**Background White**
- **Hex:** #FFFFFF
- **RGB:** 255, 255, 255
- **Usage:** Card backgrounds, content boxes

**Background Light**
- **Hex:** #F8F9FA
- **RGB:** 248, 249, 250
- **Usage:** Page backgrounds, subtle separations

**Border**
- **Hex:** #E0E0E0
- **RGB:** 224, 224, 224
- **Usage:** Borders, dividers

### Color Usage Rules

**Primary Blue (#003366):**
- Logo
- Navigation links
- Section headers
- Primary buttons (secondary style)
- Informational content boxes
- Data visualizations (primary color)

**Accent Orange (#FF6B35):**
- "Apply Now" buttons
- "Featured" tags
- Important alerts
- Progress indicators
- Call-to-action elements

**Success Green:**
- #10B981
- "Online Available" badges
- Success messages
- Completion indicators

**Accessibility:**
- Primary Blue on white: AA compliance ✓
- Accent Orange on white: AA compliance ✓
- All color combinations tested for WCAG 2.1 Level AA

---

## Typography

### Primary Font: Arial Black (System Font)

**Rationale:** 
- Universally available (no font loading)
- Heavy weight = authority
- Excellent legibility
- Fast page load (SEO benefit)

**Fallback Stack:**
```css
font-family: 'Arial Black', 'Helvetica Bold', sans-serif;
```

### Type Scale

**Headings:**
```css
H1: 32-36px, font-weight: 900, letter-spacing: -1px
H2: 24-28px, font-weight: 900, letter-spacing: -1px
H3: 20-22px, font-weight: 700
H4: 18px, font-weight: 700
```

**Body Text:**
```css
Body: 15-16px, font-weight: 400, line-height: 1.6
Small: 13-14px, font-weight: 400, line-height: 1.6
Meta: 12-13px, font-weight: 400, text-transform: uppercase, letter-spacing: 1px
```

**Usage:**
- Logo: Arial Black, 32-72px depending on context
- Headings: Arial Black for H1-H2, Arial Bold for H3-H4
- Body: System sans-serif stack (faster loading)

---

## Visual Elements

### Star Cutout System

The star is our signature brand element, appearing consistently across all touchpoints.

**What it represents:**
- Government (stars on flags, official seals)
- Achievement/certification
- Visual "notch" creating interest without complexity

**Star Positioning Formula:**

For any element with border-radius `R`:
```
top: R × 0.66 (negative value, e.g., -8px for 12px radius)
right: R × 1.5 (e.g., 18px for 12px radius)
width: R × 1.5
height: R × 1.5
```

**Common sizes:**
- 12px border-radius: `top: -8px; right: 18px; width: 18px; height: 18px;`
- 8px border-radius: `top: -5px; right: 12px; width: 12px; height: 12px;`

**Star SVG polygon:**
```svg
<polygon points="50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%" />
```

### Border Radius

**Standard sizes:**
- Large cards/sections: 12px
- Buttons/badges: 8px
- Small elements: 6px
- No border-radius on elements where star is in actual corner

### Shadows

**Elevation system:**
```css
/* Low elevation (cards) */
box-shadow: 0 2px 8px rgba(0,0,0,0.05);

/* Medium elevation (hover states) */
box-shadow: 0 4px 16px rgba(0,0,0,0.1);

/* High elevation (modals) */
box-shadow: 0 8px 24px rgba(0,0,0,0.15);
```

**Never use:**
- Inner shadows
- Colored shadows
- Multiple shadow layers

---

## Design Patterns

### Content Cards

**Standard card with star cutout:**
```css
.star-box {
    background: white;
    padding: 30px;
    border-radius: 12px;
    position: relative;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.star-box::before {
    content: '';
    position: absolute;
    top: -8px;     /* 12px × 66% */
    right: 18px;   /* 12px × 150% */
    width: 18px;
    height: 18px;
    background: #f8f9fa; /* page background color */
    clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
}
```

**Colored cards:**
- Use primary blue or accent orange background
- Star cutout uses page background color
- Text color: white

**Bordered cards:**
- Border: 2px solid primary blue
- Star cutout uses border color (not background)
- Use `overflow: hidden` to show only bottom half of star

### Buttons

**Primary CTA (Orange):**
```css
.star-button {
    padding: 14px 32px;
    background: #FF6B35;
    color: white;
    border-radius: 8px;
    font-weight: 600;
    position: relative;
}

.star-button::before {
    top: -5px;
    right: 12px;
    width: 12px;
    height: 12px;
    background: #f8f9fa;
    /* star polygon */
}
```

**Secondary (Blue):**
- Same structure, background: #003366

**Outline:**
- Border: 2px solid primary
- Background: white
- Color: primary
- Star in border color with `overflow: hidden`

### Status Badges

**Structure:**
```css
.status-badge {
    display: inline-flex;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    position: relative;
}
```

**Types:**
- Success: Background #10B981 (green) - "Online Available"
- Primary: Background #003366 (blue) - "API Ready"  
- Warning: Background #FF6B35 (orange) - "In-Person Required"

All badges include star cutout in top-right.

### Info Cards (Statistics)

**For displaying metrics:**
- White background
- 2px border (#E0E0E0)
- Star cutout in border color
- Large number (32px, font-weight 900, primary color)
- Small label (13px, uppercase, letter-spacing: 1px)

### Section Headers

**Structure:**
```css
.section-header {
    background: white;
    padding: 20px 30px;
    border-radius: 12px;
    position: relative;
}

.section-header::before {
    /* Star on left side for variety */
    left: 18px;
    /* rest same as standard */
}
```

---

## Usage Examples

### Website Header

```html
<header>
    <svg viewBox="0 0 240 40" role="img" aria-label="News123">
        <!-- Inline SVG logo -->
    </svg>
    <nav>
        <a href="#">Home</a>
        <a href="#">Browse Permits</a>
        <a href="#">About</a>
    </nav>
</header>
```

**Styling:**
- Background: White
- Logo: Primary blue
- Nav links: Text light (#666), hover to primary blue
- Border-radius: 12px (if card style)

### Permit Detail Page

**Hero Section:**
- H1: Permit name (32-36px, primary blue)
- Breadcrumbs: Home > State > Permit name
- Star cutout on section background

**Key Info Grid:**
- Cost, Processing Time, Renewal Frequency
- Use info cards with star cutouts
- Primary color for numbers

**Requirements Section:**
- White card with star cutout
- Checklist with checkmarks
- Border for emphasis (optional)

**CTA Button:**
- Orange "Apply Now" with star cutout
- Blue "View Requirements" secondary
- Positioned prominently above fold

---

## Don'ts

### Logo Don'ts
❌ Don't modify the star cutout position
❌ Don't use colors outside the defined palette
❌ Don't add gradients, shadows, or effects
❌ Don't stretch, rotate, or distort
❌ Don't place on busy/patterned backgrounds
❌ Don't make logo smaller than 120px width

### Color Don'ts
❌ Don't use accent orange for large text areas
❌ Don't combine primary blue + accent orange in adjacent elements (too much contrast)
❌ Don't use colors at low opacity (fails accessibility)
❌ Don't create new color variations

### Typography Don'ts
❌ Don't use more than 2 font families
❌ Don't use italic (not in brand)
❌ Don't use all caps except for small labels/meta
❌ Don't use text smaller than 13px
❌ Don't use letter-spacing on body text

### Star Element Don'ts
❌ Don't place star randomly - follow the formula
❌ Don't use full star on bordered elements (show only bottom half)
❌ Don't use star without border-radius context
❌ Don't make star larger than 20px
❌ Don't use multiple stars per element

---

## Quick Reference

### Color Variables (CSS)
```css
:root {
    --primary: #003366;
    --accent: #FF6B35;
    --text: #1a1a1a;
    --text-light: #666666;
    --bg: #ffffff;
    --bg-light: #f8f9fa;
    --border: #e0e0e0;
    --success: #10b981;
}
```

### Star Formula Quick Ref
```
For border-radius R:
- top: R × -0.66
- right: R × 1.5  
- width/height: R × 1.5
```

### Common Border Radius
- Cards: 12px
- Buttons: 8px
- Badges: 8px

### Common Padding
- Cards: 30px
- Buttons: 14px 32px
- Badges: 8px 16px

---

## Contact

For brand questions or asset requests:
- Website: ainews123.com
- Repository: github.com/ynizan/permitindex-site

**Document Version:** 1.0  
**Last Updated:** November 2024  
**Next Review:** Quarterly

---

*These guidelines ensure consistency across all News123 touchpoints while maintaining flexibility for growth.*