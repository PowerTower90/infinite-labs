# Infinite Labs Skills Setup Guide

## Overview

This project now uses **4 Anthropic Skills** to maintain consistent, high-quality development standards for design, branding, and testing.

**Skills Directory**: `skills/`
- `frontend-design/` - UI/UX design excellence
- `brand-guidelines/` - Brand consistency
- `theme-factory/` - Professional theme application
- `webapp-testing/` - Automated testing

---

## Quick Start

### For Frontend Development

When building any user-facing interface:

1. **Apply Frontend-Design Skill**
   - Read: `skills/frontend-design/SKILL.md`
   - Choose a BOLD aesthetic direction
   - Use distinctive typography, cohesive colors, thoughtful animations
   - Avoid generic AI aesthetics

2. **Ensure Brand Consistency**
   - Reference: `skills/brand-guidelines/`
   - Use official brand colors (see guide)
   - Apply Poppins (headings) + Lora (body)
   - Maintain visual identity across pages

3. **Consider Theme-Factory for Styling**
   - Reference: `skills/theme-factory/theme-showcase.pdf`
   - Choose a professional theme or create custom
   - Apply consistently across entire site

---

### For Testing

When validating website functionality:

1. **Use Web App Testing Skill**
   - Reference: `skills/webapp-testing/SKILL.md`
   - Start Flask with helper script: `python skills/webapp-testing/scripts/with_server.py --help`
   - Write Playwright scripts for UI automation
   - Capture screenshots and verify functionality

2. **MCP Server Testing (Primary Method)**
   - Always use Chrome DevTools MCP Server for testing
   - Keep browser window visible (never headless)
   - Document test results with screenshots

---

## Skill Details

### 1. Frontend-Design

**File**: `skills/frontend-design/SKILL.md`

**Purpose**: Create distinctive, production-grade interfaces

**Core Principles:**
- **Design Thinking** - Understand context before coding
  - Purpose: What problem does this solve?
  - Tone: Pick an extreme aesthetic direction
  - Constraints: Technical requirements
  - Differentiation: What makes it unforgettable?

- **Frontend Aesthetics**
  - **Typography**: Distinctive, characterful fonts
    - NOT Arial, Inter, Roboto, Arial
    - Pair distinctive display + refined body font
  - **Color & Theme**: Commit to cohesive aesthetic
    - Use CSS variables
    - Dominant colors with sharp accents
  - **Motion**: High-impact animations
    - One well-orchestrated page load > scattered micro-interactions
    - Use scroll-triggering and hover surprises
  - **Spatial Composition**: Unexpected layouts
    - Asymmetry, overlap, diagonal flow, grid-breaking
    - Generous negative space OR controlled density
  - **Backgrounds & Details**: Atmosphere & depth
    - Gradients, noise textures, patterns
    - Dramatic shadows, decorative borders, custom cursors

**NEVER:**
- Use generic AI aesthetics (Inter, purple gradients)
- Create cookie-cutter designs
- Lack intentionality

**Examples for Infinite Labs:**
- Product pages with bold aesthetic direction
- Checkout flow with refined minimalism
- Admin dashboard with tech-forward design

---

### 2. Brand-Guidelines

**File**: `skills/brand-guidelines/SKILL.md`

**Official Colors:**
| Color | Hex | Usage |
|-------|-----|-------|
| Dark | `#141413` | Primary text, dark backgrounds |
| Light | `#faf9f5` | Light backgrounds, text on dark |
| Mid Gray | `#b0aea5` | Secondary elements |
| Light Gray | `#e8e6dc` | Subtle backgrounds |
| Orange | `#d97757` | Primary accent |
| Blue | `#6a9bcc` | Secondary accent |
| Green | `#788c5d` | Tertiary accent |

**Typography:**
- Headings (24pt+): Poppins (fallback: Arial)
- Body Text: Lora (fallback: Georgia)

**When to Apply:**
- Marketing/product pages
- Documentation
- Internal presentations
- Branded artifacts

---

### 3. Theme-Factory

**File**: `skills/theme-factory/SKILL.md`
**Showcase**: `skills/theme-factory/theme-showcase.pdf`

**10 Professional Themes Available:**

1. **Ocean Depths** - Professional and calming maritime theme
2. **Sunset Boulevard** - Warm and vibrant sunset colors
3. **Forest Canopy** - Natural and grounded earth tones
4. **Modern Minimalist** - Clean and contemporary grayscale
5. **Golden Hour** - Rich and warm autumnal palette
6. **Arctic Frost** - Cool and crisp winter-inspired theme
7. **Desert Rose** - Soft and sophisticated dusty tones
8. **Tech Innovation** - Bold and modern tech aesthetic
9. **Botanical Garden** - Fresh and organic garden colors
10. **Midnight Galaxy** - Dramatic and cosmic deep tones

**Theme Details**: Each theme in `skills/theme-factory/themes/` includes:
- Cohesive color palette (hex codes)
- Complementary font pairings
- Distinct visual identity

**Usage Workflow:**
1. Show theme showcase PDF to stakeholders
2. Get confirmation on theme choice
3. Read corresponding theme file
4. Apply colors and fonts consistently

**Create Custom Theme:**
- Use provided inputs (brand colors, audience, context)
- Generate new theme similar to existing ones
- Show for review before applying

**For Infinite Labs:**
- Consider "Tech Innovation" for cutting-edge peptide science brand
- Or "Golden Hour" for luxury product positioning
- Or "Modern Minimalist" for clean, professional aesthetic

---

### 4. Web App Testing

**File**: `skills/webapp-testing/SKILL.md`
**Helper Script**: `skills/webapp-testing/scripts/with_server.py`
**Examples**: `skills/webapp-testing/examples/`
**Playwright Library**: Included in dependencies

**Purpose**: Test Flask application with Python Playwright

**Key Tools:**
- `with_server.py` - Manage Flask server lifecycle
- Playwright - UI automation and testing
- Screenshot capture
- DOM inspection
- Console log monitoring

**Workflow:**

```bash
# Start Flask server + run test
python skills/webapp-testing/scripts/with_server.py \
  --server "python app.py" --port 5000 \
  -- python your_test_script.py
```

**Basic Test Script:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5000')
    page.wait_for_load_state('networkidle')
    
    # Your test logic here
    page.screenshot(path='result.png', full_page=True)
    
    browser.close()
```

**Critical Patterns:**
- Always wait for `networkidle` before DOM inspection
- Use descriptive selectors (text=, role=, CSS)
- Take screenshots for visual verification
- Close browser when done

**Example Tests for Infinite Labs:**
- Product page rendering
- Shopping cart functionality
- Checkout process
- Admin dashboard permissions
- Search functionality

---

## Integration with Copilot

All 4 skills are referenced in `.github/copilot-instructions.md`

**Copilot will:**
- Reference these skills when building UI
- Suggest appropriate skill usage for tasks
- Maintain brand consistency
- Apply frontend design principles automatically
- Recommend testing strategies

---

## File Structure

```
d:\infinite labs\
├── skills/
│   ├── frontend-design/
│   │   ├── SKILL.md
│   │   └── LICENSE.txt
│   ├── brand-guidelines/
│   │   ├── SKILL.md
│   │   └── LICENSE.txt
│   ├── theme-factory/
│   │   ├── SKILL.md
│   │   ├── theme-showcase.pdf
│   │   └── themes/
│   │       ├── ocean-depths.md
│   │       ├── sunset-boulevard.md
│   │       └── ... (10 themes total)
│   └── webapp-testing/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── with_server.py
│       └── examples/
│           ├── element_discovery.py
│           ├── static_html_automation.py
│           └── console_logging.py
├── .github/
│   └── copilot-instructions.md (updated with skills)
├── app.py
├── admin_app.py
├── requirements.txt
├── templates/
├── admin_templates/
└── static/
```

---

## Next Steps

1. **Review each skill:**
   - Frontend Development: Read `skills/frontend-design/SKILL.md`
   - Branding: Study `skills/brand-guidelines/SKILL.md`
   - Themes: Preview `skills/theme-factory/theme-showcase.pdf`
   - Testing: Read `skills/webapp-testing/SKILL.md`

2. **Update Flask templates:**
   - Apply brand colors from brand-guidelines
   - Implement chosen theme
   - Apply frontend-design principles

3. **Set up testing:**
   - Create test scripts using webapp-testing skill
   - Validate Flask app functionality
   - Document testing procedures

4. **Team Training:**
   - Share this guide with team
   - Review skill principles together
   - Establish design/testing standards

---

## Questions?

Refer to the SKILL.md files in each skill directory for detailed documentation.

For questions about integration, see `.github/copilot-instructions.md`
