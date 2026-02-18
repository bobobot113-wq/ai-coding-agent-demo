"""
AI Coding Agent Demo - Streamlit Web UI
========================================
A simple web interface for the AI Coding Agent Demo.

Run with: streamlit run web_app.py
"""

import streamlit as st
import re
from pathlib import Path
from js_analyzer import JavaScriptAnalyzer
from agent_demo import CodeAnalyzer

# Page config
st.set_page_config(
    page_title="🤖 AI Code Agent Demo",
    page_icon="🤖",
    layout="wide"
)

def analyze_python(code: str) -> dict:
    """Analyze Python code."""
    analyzer = CodeAnalyzer(use_mock=True)
    
    # Use the mock analysis logic directly
    issues = []
    suggestions = []
    
    # Check for common issues
    if 'print(' in code and 'logging' not in code:
        issues.append("Using print() instead of proper logging")
        suggestions.append("Consider using the logging module for production code")
    
    if 'except:' in code:
        issues.append("Bare except clause found")
        suggestions.append("Use specific exception types: except ValueError as e:")
    
    if 'global ' in code:
        issues.append("Using global variables")
        suggestions.append("Consider passing variables as parameters or using classes")
    
    if not re.search(r'type\s+\w+\s*=\s*', code) and not re.search(r'def\s+\w+.*\)->', code):
        if len(re.findall(r'def\s+(\w+)', code)) > 0:
            suggestions.append("Consider adding type hints for better code clarity")
    
    if len(code.split('\n')) > 100:
        suggestions.append("File is quite long - consider splitting into modules")
    
    todos = re.findall(r'#\s*TODO:?\s*(.+)', code, re.IGNORECASE)
    
    stats = {
        "lines": len(code.split('\n')),
        "functions": len(re.findall(r'def\s+(\w+)', code)),
        "classes": len(re.findall(r'class\s+(\w+)', code)),
        "imports": len(re.findall(r'^import\s+|^from\s+', code, re.MULTILINE))
    }
    
    return {
        "stats": stats,
        "issues": issues,
        "suggestions": suggestions,
        "todos": todos
    }


def analyze_javascript(code: str) -> dict:
    """Analyze JavaScript code."""
    # Use patterns from js_analyzer
    issues = []
    suggestions = []
    
    stats = {
        "lines": len(code.split('\n')),
        "functions": len(re.findall(r'function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(', code)),
        "classes": len(re.findall(r'class\s+(\w+)', code)),
        "imports": len(re.findall(r'^import\s+|^const\s+\w+\s*=\s*require', code, re.MULTILINE)),
    }
    
    if 'console.log' in code:
        issues.append("Using console.log for debugging")
        suggestions.append("Use a proper logging library or remove in production")
    
    if 'var ' in code:
        issues.append("Using 'var' instead of 'let' or 'const'")
        suggestions.append("Use 'let' for mutable variables, 'const' for immutable")
    
    if '==' in code or '!=' in code:
        issues.append("Using loose equality (==/!=)")
        suggestions.append("Use strict equality (===/!==) for predictable comparisons")
    
    if 'eval(' in code:
        issues.append("⚠️ SECURITY: Using eval() is dangerous")
        suggestions.append("Avoid eval() - it can execute arbitrary code")
    
    if 'innerHTML' in code:
        issues.append("⚠️ Potential XSS: Using innerHTML")
        suggestions.append("Use textContent or sanitize input")
    
    todos = re.findall(r'//\s*TODO:?\s*(.+)', code, re.IGNORECASE)
    
    return {
        "stats": stats,
        "issues": issues,
        "suggestions": suggestions,
        "todos": todos
    }


def main():
    """Main Streamlit app."""
    st.title("🤖 AI Code Agent Demo")
    st.markdown("Analyze Python and JavaScript code for issues and improvements")
    
    # Sidebar
    st.sidebar.header("⚙️ Options")
    language = st.sidebar.selectbox(
        "Select Language",
        ["Python", "JavaScript"]
    )
    
    # Main content
    tab1, tab2 = st.tabs(["📝 Code Input", "📁 File Upload"])
    
    with tab1:
        code_input = st.text_area(
            "Paste your code here:",
            height=300,
            placeholder=f"# Paste {language} code here..."
        )
        
        if st.button("🔍 Analyze Code", type="primary"):
            if code_input:
                with st.spinner("Analyzing..."):
                    if language == "Python":
                        result = analyze_python(code_input)
                    else:
                        result = analyze_javascript(code_input)
                    
                    display_results(result)
            else:
                st.warning("Please enter some code first!")
    
    with tab2:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["py", "js", "ts", "jsx", "tsx"],
            help="Upload Python or JavaScript/TypeScript files"
        )
        
        if uploaded_file is not None:
            code = uploaded_file.getvalue().decode("utf-8")
            st.code(code, language=language.lower())
            
            if st.button("🔍 Analyze Uploaded File", type="primary"):
                with st.spinner("Analyzing..."):
                    if language == "Python":
                        result = analyze_python(code)
                    else:
                        result = analyze_javascript(code)
                    
                    display_results(result)


def display_results(result: dict):
    """Display analysis results."""
    st.divider()
    st.subheader("📊 Analysis Results")
    
    # Stats
    if result.get("stats"):
        st.markdown("### 📈 Code Statistics")
        cols = st.columns(4)
        for i, (key, value) in enumerate(result["stats"].items()):
            cols[i % 4].metric(key.capitalize(), value)
    
    # Issues
    if result.get("issues"):
        st.markdown("### 🚨 Issues Found")
        for issue in result["issues"]:
            if "⚠️" in issue:
                st.error(issue)
            else:
                st.warning(issue)
    
    # Suggestions
    if result.get("suggestions"):
        st.markdown("### 💡 Suggestions")
        for suggestion in result["suggestions"]:
            st.info(f"💡 {suggestion}")
    
    # TODOs
    if result.get("todos"):
        st.markdown("### 📌 TODOs")
        for todo in result["todos"]:
            st.checkbox(todo, value=False)
    
    # Summary
    issue_count = len(result.get("issues", []))
    suggestion_count = len(result.get("suggestions", []))
    
    if issue_count == 0 and suggestion_count == 0:
        st.success("✅ Code looks clean! No major issues found.")
    else:
        st.markdown(f"**Found {issue_count} issue(s) and {suggestion_count} suggestion(s)**")


if __name__ == "__main__":
    main()
