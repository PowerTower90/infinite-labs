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

**Remember**: Testing = MCP Server with Visible Browser
