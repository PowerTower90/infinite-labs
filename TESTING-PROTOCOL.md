# Testing Protocol for Infinite Labs Website

## Default Testing Method

**ALWAYS use Chrome DevTools MCP Server for validation and testing.**

## When to Use MCP Server Testing

The Chrome DevTools MCP server MUST be used whenever:

1. **Validating website functionality** - Testing pages, forms, buttons, links
2. **Checking for errors** - Console errors, network issues, broken features
3. **Verifying user flows** - Add to cart, checkout, login, signup, contact forms
4. **Visual inspection** - Ensuring pages render correctly
5. **Performance testing** - Page load times, resource loading
6. **Bug investigation** - Reproducing and diagnosing issues

## MCP Server Configuration

- **Server**: `io.github.ChromeDevTools/chrome-devtools-mcp`
- **Mode**: Visible browser (NOT headless)
- **Browser**: Chrome/Chromium
- **Configuration**: Set in VS Code MCP settings with `--headless=false`

## Testing Workflow

1. **Start Flask App**: Run `python app.py` in background terminal
2. **Open Browser**: Use `mcp_io_github_chr_new_page` to open the URL
3. **Visible Testing**: Browser window should be PHYSICALLY VISIBLE on screen
4. **Interactive Testing**: Click, fill forms, navigate - all visible in real-time
5. **Capture Evidence**: Take screenshots and snapshots for documentation
6. **Check Console**: Monitor for errors and warnings
7. **Verify Network**: Ensure all resources load successfully

## Why MCP Server Testing?

- **Visual Verification**: User can SEE the browser working in real-time
- **Real Browser**: Tests in actual Chrome, not simulated environment
- **Comprehensive**: Access to DevTools, console, network, and performance data
- **Reliable**: Automated but realistic user interactions
- **Debugging**: Easy to spot visual issues and errors

## Notes

- Browser window MUST be visible during testing (never headless for validation)
- User should be able to watch all interactions happen live
- MCP server provides both automation AND transparency

---

**Last Updated**: February 19, 2026
**Status**: Active Protocol
