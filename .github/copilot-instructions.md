# Copilot Instructions for Infinite Labs Project

## Project-Specific Guidelines

### Testing and Validation Protocol

**MANDATORY**: When asked to validate, test, or check website functionality:

1. **ALWAYS use Chrome DevTools MCP Server** 
   - Never suggest manual testing as the primary method
   - MCP server testing is the default and required approach

2. **Visible Browser Required**
   - Browser window MUST be visible (not headless)
   - User should see all interactions in real-time
   - Configuration: `--headless=false` in MCP settings

3. **Testing Workflow**
   - Start Flask app in background: `python app.py`
   - Use `mcp_io_github_chr_new_page` to open URL
   - Perform interactive testing with visible browser
   - Capture screenshots and snapshots
   - Check console and network requests

4. **When User Says "Validate", "Test", or "Check"**
   - Immediately use MCP server tools
   - Show the browser window working
   - Provide comprehensive test results

### Why This Matters

- User wants to SEE the testing happen
- Transparency and visual confirmation are critical
- MCP server provides both automation and visibility

### Reference Documents

- [TESTING-PROTOCOL.md](TESTING-PROTOCOL.md) - Complete testing guidelines
- [README.md](README.md) - Project overview with testing reference

---

## Anthropic Skills for Infinite Labs

This project uses 4 Anthropic Skills by default for consistent, high-quality development:

### 1. **Frontend-Design** (`skills/frontend-design/`)
Create distinctive, production-grade interfaces that avoid generic AI aesthetics.

**When to use**: Building web components, pages, dashboards, or styling any UI
- Pick a BOLD aesthetic direction (minimalist, luxury, organic, etc.)
- Use distinctive typography (NOT Arial/Inter)
- Apply cohesive color schemes with dominant colors + sharp accents
- Implement thoughtful animations and micro-interactions
- Create unexpected spatial compositions with asymmetry and depth

**Key Principle**: Intentionality and refinement over generic outputs

---

### 2. **Brand-Guidelines** (`skills/brand-guidelines/`)
Apply consistent Anthropic brand identity to all artifacts.

**Official Colors:**
- Dark: `#141413` | Light: `#faf9f5` | Mid Gray: `#b0aea5`
- Orange: `#d97757` | Blue: `#6a9bcc` | Green: `#788c5d`

**Typography:**
- Headings: Poppins
- Body: Lora (fallback: Arial/Georgia)

**When to use**: Creating documents, presentations, or components that should match brand standards

---

### 3. **Theme-Factory** (`skills/theme-factory/`)
Apply professional themes with cohesive color + font combinations.

**10 Available Themes:**
- Ocean Depths | Sunset Boulevard | Forest Canopy | Modern Minimalist | Golden Hour
- Arctic Frost | Desert Rose | Tech Innovation | Botanical Garden | Midnight Galaxy

**When to use**: Need consistent, professional styling across presentation decks, landing pages, or documentation

**Reference**: See `skills/theme-factory/theme-showcase.pdf` for visual examples

---

### 4. **Web App Testing** (`skills/webapp-testing/`)
Test Flask application with Playwright automation.

**Key Tools:**
- `scripts/with_server.py` - Manage Flask server lifecycle during tests
- Python Playwright for UI/UX testing
- Screenshot capture and DOM inspection
- Console log monitoring

**When to use**: Validating product pages, checkout flow, admin dashboard, or any UI functionality

**Workflow:**
1. Use `with_server.py` to start Flask in background
2. Write Playwright script for interactions
3. Capture screenshots and inspect console logs
4. Report test results with evidence

---

**Remember**: Testing = MCP Server with Visible Browser
