"""
AI Coding Agent Demo - Streamlit Web UI
========================================
A simple web interface for the AI Coding Agent Demo.

Run with: streamlit run web_app.py

Supports local Ollama for AI-powered analysis!
"""

import streamlit as st
import re
import json
import requests
from pathlib import Path
from typing import Optional

# Page config
st.set_page_config(
    page_title="🤖 AI Code Agent Demo",
    page_icon="🤖",
    layout="wide"
)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"

def check_ollama_available() -> bool:
    """Check if Ollama is running."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_available_models() -> list:
    """Get list of available Ollama models."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
    except:
        pass
    return []

def analyze_with_ollama(code: str, language: str, model: str) -> dict:
    """Analyze code using local Ollama."""
    
    prompt = f"""You are a code analysis expert. Analyze the following {language} code and provide:
1. Issues/bugs found
2. Suggestions for improvement
3. Security concerns
4. Code quality notes

Provide your response as a JSON object with these keys:
- issues: array of issues found
- suggestions: array of improvement suggestions  
- security: array of security concerns
- quality: array of code quality notes

Code to analyze:
```{language.lower()}
{code}
```

Respond ONLY with valid JSON:"""

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = json.loads(result.get("response", "{}"))
            return {
                "issues": analysis.get("issues", []),
                "suggestions": analysis.get("suggestions", []),
                "security": analysis.get("security", []),
                "quality": analysis.get("quality", []),
                "raw": result.get("response", "")
            }
    except Exception as e:
        return {"error": str(e)}
    
    return {"error": "Failed to get response from Ollama"}


def analyze_python_mock(code: str) -> dict:
    """Analyze Python code (mock/rule-based)."""
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


def analyze_javascript_mock(code: str) -> dict:
    """Analyze JavaScript code (mock/rule-based)."""
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
    
    # Check Ollama availability
    ollama_available = check_ollama_available()
    
    # Sidebar
    st.sidebar.header("⚙️ Options")
    
    # Analysis mode
    analysis_mode = st.sidebar.radio(
        "Analysis Mode",
        ["🤖 Ollama (AI)", "📋 Rule-based (Mock)"],
        disabled=not ollama_available,
        help="Ollama uses local AI model for deeper analysis" if ollama_available else "Start Ollama to enable AI analysis"
    )
    
    use_ollama = analysis_mode.startswith("🤖") and ollama_available
    
    # Model selection (if using Ollama)
    selected_model = DEFAULT_MODEL
    if use_ollama:
        models = get_available_models()
        if models:
            selected_model = st.sidebar.selectbox(
                "Select Model",
                models,
                index=models.index(DEFAULT_MODEL) if DEFAULT_MODEL in models else 0
            )
        else:
            st.sidebar.warning("No models found. Using default.")
    
    language = st.sidebar.selectbox(
        "Select Language",
        ["Python", "JavaScript"]
    )
    
    # Status indicator
    if ollama_available:
        st.sidebar.success("✅ Ollama connected")
    else:
        st.sidebar.warning("⚠️ Ollama not running - using rule-based analysis")
    
    # Main content
    tab1, tab2 = st.tabs(["📝 Code Input", "📁 File Upload"])
    
    with tab1:
        code_input = st.text_area(
            "Paste your code here:",
            height=300,
            placeholder=f"# Paste {language} code here..."
        )
        
        button_label = "🔍 Analyze with Ollama" if use_ollama else "🔍 Analyze Code"
        
        if st.button(button_label, type="primary"):
            if code_input:
                with st.spinner("Analyzing..." + (" (AI)" if use_ollama else "") ):
                    if use_ollama:
                        result = analyze_with_ollama(code_input, language, selected_model)
                    elif language == "Python":
                        result = analyze_python_mock(code_input)
                    else:
                        result = analyze_javascript_mock(code_input)
                    
                    display_results(result, use_ollama)
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
            
            button_label = "🔍 Analyze with Ollama" if use_ollama else "🔍 Analyze Uploaded File"
            
            if st.button(button_label, type="primary"):
                with st.spinner("Analyzing..." + (" (AI)" if use_ollama else "")):
                    if use_ollama:
                        result = analyze_with_ollama(code, language, selected_model)
                    elif language == "Python":
                        result = analyze_python_mock(code)
                    else:
                        result = analyze_javascript_mock(code)
                    
                    display_results(result, use_ollama)


def display_results(result: dict, is_ollama: bool = False):
    """Display analysis results."""
    st.divider()
    st.subheader("📊 Analysis Results")
    
    if result.get("error"):
        st.error(f"Error: {result['error']}")
        return
    
    # For Ollama results
    if is_ollama:
        # Issues
        if result.get("issues"):
            st.markdown("### 🚨 Issues Found")
            for issue in result["issues"]:
                st.warning(f"• {issue}")
        
        # Suggestions
        if result.get("suggestions"):
            st.markdown("### 💡 Suggestions")
            for suggestion in result["suggestions"]:
                st.info(f"💡 {suggestion}")
        
        # Security
        if result.get("security"):
            st.markdown("### 🔒 Security Concerns")
            for sec in result["security"]:
                st.error(f"🔒 {sec}")
        
        # Quality
        if result.get("quality"):
            st.markdown("### 📊 Code Quality")
            for q in result["quality"]:
                st.write(f"• {q}")
        
        # Show raw if needed
        if st.checkbox("Show raw AI response"):
            st.text(result.get("raw", ""))
    
    # For mock/rule-based results
    else:
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
    issue_count = len(result.get("issues", [])) + len(result.get("security", []))
    suggestion_count = len(result.get("suggestions", []))
    
    if issue_count == 0 and suggestion_count == 0:
        st.success("✅ Code looks clean! No major issues found.")
    else:
        st.markdown(f"**Found {issue_count} issue(s) and {suggestion_count} suggestion(s)**")


if __name__ == "__main__":
    main()
