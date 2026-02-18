"""
JavaScript Code Analyzer
========================
Analyzes JavaScript/TypeScript code for common issues and improvements.
"""

import re
from typing import Dict, Any, List


class JavaScriptAnalyzer:
    """Analyzes JavaScript/TypeScript code for issues and improvements."""
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a JavaScript/TypeScript file and return findings."""
        print(f"\n📁 Analyzing JS: {filepath}")
        print("━" * 50)
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return {"error": f"File not found: {filepath}"}
        except Exception as e:
            return {"error": str(e)}
        
        return self._perform_analysis(content, filepath)
    
    def _perform_analysis(self, content: str, filepath: str) -> Dict[str, Any]:
        """Perform JavaScript-specific analysis."""
        issues = []
        suggestions = []
        
        # Count stats
        stats = {
            "lines": len(content.split('\n')),
            "functions": len(re.findall(r'function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(', content)),
            "classes": len(re.findall(r'class\s+(\w+)', content)),
            "imports": len(re.findall(r'^import\s+|^const\s+\w+\s*=\s*require', content, re.MULTILINE)),
            "exports": len(re.findall(r'^export\s+', content, re.MULTILINE)),
        }
        
        # Check for common JS issues
        if 'console.log' in content:
            issues.append("Using console.log for debugging")
            suggestions.append("Use a proper logging library or remove in production")
        
        if 'var ' in content:
            issues.append("Using 'var' instead of 'let' or 'const'")
            suggestions.append("Use 'let' for mutable variables, 'const' for immutable")
        
        if '==' in content or '!=' in content:
            issues.append("Using loose equality (==/!=)")
            suggestions.append("Use strict equality (===/!==) for predictable comparisons")
        
        if 'any' in content and '.ts' in filepath:
            suggestions.append("Consider adding specific types instead of 'any'")
        
        if 'TODO' in content:
            todos = re.findall(r'//\s*TODO:?\s*(.+)', content, re.IGNORECASE)
        
        if not re.search(r'async\s+function|const\s+\w+\s*=\s*async', content) and 'await' in content:
            issues.append("Using 'await' without 'async' function")
        
        # Check for common security issues
        if 'eval(' in content:
            issues.append("⚠️ SECURITY: Using eval() is dangerous")
            suggestions.append("Avoid eval() - it can execute arbitrary code")
        
        if 'innerHTML' in content:
            issues.append("⚠️ Potential XSS: Using innerHTML")
            suggestions.append("Use textContent or sanitize input")
        
        return {
            "filepath": filepath,
            "stats": stats,
            "issues": issues,
            "suggestions": suggestions,
            "summary": self._generate_summary(issues, suggestions, stats)
        }
    
    def _generate_summary(self, issues: List[str], suggestions: List[str], stats: Dict) -> str:
        """Generate a summary of findings."""
        issue_count = len(issues)
        suggestion_count = len(suggestions)
        
        if issue_count == 0 and suggestion_count == 0:
            return "Code looks clean! No major issues found."
        
        parts = []
        if issue_count > 0:
            parts.append(f"Found {issue_count} issue(s)")
        if suggestion_count > 0:
            parts.append(f"{suggestion_count} improvement suggestion(s)")
        
        return ", ".join(parts)
