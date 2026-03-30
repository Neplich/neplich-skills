# Visual Design Instructions

## Overview

This skill defines a visual design system including colors, typography, spacing, components, and copy guidelines. It emphasizes distinctive aesthetics that avoid generic AI patterns.

## Execution Steps

### Step 1: Gather Context

1. **Read PM documents**:
   - BRD: brand tone, target audience, business goals
   - PRD: product type and features
   - UI/UX spec (if exists): component list

2. **Understand product type**:
   - SaaS dashboard → professional, clean
   - E-commerce → vibrant, trustworthy
   - Content platform → readable, engaging
   - Mobile app → touch-friendly, simple

### Step 2: Choose Aesthetic Direction

Ask user about style preference using AskUserQuestion:

```
Question: "What aesthetic direction fits your product best?"
Options:
- "Minimalist" - Clean, spacious, restrained
- "Bold/Brutalist" - Strong typography, high contrast
- "Playful" - Rounded corners, bright colors
- "Professional" - Corporate, trustworthy
- "Modern/Tech" - Gradients, glassmorphism
- "Let the AI decide based on product type"
```

Avoid generic patterns:
- ❌ Inter/Roboto fonts (overused)
- ❌ Purple-blue gradients
- ❌ Generic rounded corners everywhere
- ✅ Distinctive font pairings
- ✅ Purposeful color choices
- ✅ Intentional design decisions


### Step 3: Define Color System

Create a purposeful color palette:

```markdown
## Color System

### Primary Colors
- Primary: #[hex] - Main brand color
- Primary Dark: #[hex] - Hover/active states
- Primary Light: #[hex] - Backgrounds

### Semantic Colors
- Success: #[hex] - Confirmations, success states
- Warning: #[hex] - Warnings, cautions
- Error: #[hex] - Errors, destructive actions
- Info: #[hex] - Information, neutral feedback

### Neutral Colors
- Text Primary: #[hex] - Main text (ensure 4.5:1 contrast)
- Text Secondary: #[hex] - Secondary text
- Border: #[hex] - Dividers, borders
- Background: #[hex] - Page background
- Surface: #[hex] - Card/panel background
```

Accessibility: Ensure WCAG AA contrast ratios (4.5:1 for text, 3:1 for UI elements)


### Step 4: Define Typography System

Choose distinctive font pairings (avoid Inter/Roboto):

```markdown
## Typography

### Font Families
- Heading: [Font Name] - Display/headings
- Body: [Font Name] - Body text, UI
- Mono: [Monospace Font] - Code, technical content

### Font Scale
- Display: 48px / 56px line-height / 700 weight
- H1: 36px / 44px / 700
- H2: 30px / 38px / 600
- H3: 24px / 32px / 600
- H4: 20px / 28px / 600
- Body Large: 18px / 28px / 400
- Body: 16px / 24px / 400
- Body Small: 14px / 20px / 400
- Caption: 12px / 16px / 400
```


### Step 5: Define Spacing System

```markdown
## Spacing Scale

Based on 8px grid:
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px
```

### Step 6: Define Component Styles

```markdown
## Component Styles

### Buttons
- Primary: [background] [text color] [padding] [border-radius]
- Secondary: [styles]
- Ghost: [styles]
- Sizes: sm (32px), md (40px), lg (48px)

### Input Fields
- Border: [color] [width]
- Focus: [border color] [shadow]
- Error: [border color]
- Height: 40px (md), 48px (lg)

### Cards
- Background: [color]
- Border: [style]
- Shadow: [elevation]
- Padding: [spacing]
- Border radius: [value]
```


### Step 7: Define Copy Guidelines

```markdown
## Copy & Tone Guidelines

### Voice & Tone
Based on product type:
- SaaS: Professional, helpful, clear
- Consumer: Friendly, approachable, conversational
- Enterprise: Authoritative, precise, formal

### Button Labels
- Primary actions: "Get Started", "Create Account", "Save Changes"
- Secondary: "Learn More", "Cancel", "Go Back"
- Avoid: "Click Here", "Submit"

### Empty States
- Encouraging: "No items yet. Create your first one!"
- Helpful: "Upload files to get started"

### Error Messages
- Clear: "Email is required"
- Helpful: "Password must be at least 8 characters"
- Avoid: "Error 400", "Invalid input"

### Success Messages
- Specific: "Profile updated successfully"
- Actionable: "Email sent! Check your inbox"
```


### Step 8: Generate Output Document

Create `docs/design/{feature-name}/visual-system.md` with this structure:

```markdown
# Visual Design System

## 1. Aesthetic Direction
[Chosen style and rationale]

## 2. Color System
[Primary, semantic, neutral colors with hex codes]

## 3. Typography
[Font families, scale, weights]

## 4. Spacing
[8px grid scale]

## 5. Component Styles
[Buttons, inputs, cards, etc.]

## 6. Copy Guidelines
[Voice, tone, examples]
```

## Quality Checklist

- [ ] Colors meet WCAG AA contrast requirements
- [ ] Font choices are distinctive (not Inter/Roboto)
- [ ] Spacing follows consistent scale
- [ ] Component styles are complete
- [ ] Copy guidelines match brand tone

## Output Location

Write to: `docs/design/{feature-name}/visual-system.md`
