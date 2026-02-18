# AI Coding Agent Demo - Enhanced

## What's New (v2)

### JavaScript/TypeScript Support
- New `js_analyzer.py` module for JS/TS analysis
- Detects common JS issues: `var` usage, console.log, loose equality, XSS vulnerabilities

### New Demo Files
- `demo_files/buggy_script.js` - JavaScript file with intentional bugs

## Running the Demo

```bash
# Analyze JavaScript
python agent_demo.py --file demo_files/buggy_script.js --task analyze
```

## Issues Detected in buggy_script.js

1. **Using `var`** - Should use `let` or `const`
2. **console.log** - Debugging code left in
3. **Loose equality (==)** - Should use `===`
4. **innerHTML XSS** - Potential security vulnerability
5. **eval()** - Security risk
6. **TypeScript `any`** - Should use specific types
7. **TODO** - Unfinished code

---

## Coming Soon
- Auto-fix capabilities
- Web UI
- More language support (Java, Go, Rust)
