#!/usr/bin/env python3
"""
🤖 AI Code Fixer - Streamlit Web UI
A simple web interface for analyzing and fixing buggy code
"""

import streamlit as st
import requests
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="🤖 AI Code Fixer",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stTextArea textarea {
        background-color: #1e2128;
        color: #e6e6e6;
    }
    .bug-highlight {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .bug-critical { border-left: 4px solid #ff4b4b; background: #2d1a1a; }
    .bug-warning { border-left: 4px solid #ffa500; background: #2d2617; }
    .bug-info { border-left: 4px solid #4b9eff; background: #172d47; }
    .fix-success { border-left: 4px solid #4bff4b; background: #1a2d1a; padding: 15px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🤖 AI Code Fixer")
st.sidebar.markdown("---")

# Initialize session state
if "code" not in st.session_state:
    st.session_state.code = ""
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "fixed_code" not in st.session_state:
    st.session_state.fixed_code = None
if "language" not in st.session_state:
    st.session_state.language = "Python"

# Language selector
language = st.sidebar.selectbox(
    "Language",
    ["Python", "JavaScript"],
    index=0
)

# API Configuration
st.sidebar.markdown("### 🔑 API Configuration")
api_base = st.sidebar.text_input(
    "API Base URL",
    value=os.getenv("API_BASE", "https://api.minimax.io")
)
api_key = st.sidebar.text_input(
    "API Key",
    type="password",
    value=os.getenv("OPENAI_API_KEY", "")
)
model = st.sidebar.text_input(
    "Model",
    value="MiniMax-M2.1"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Demo Files")
if st.sidebar.button("Load buggy_calculator.py"):
    demo_file = Path(__file__).parent / "demo_files" / "buggy_calculator.py"
    if demo_file.exists():
        st.session_state.code = demo_file.read_text()
        st.session_state.language = "Python"
if st.sidebar.button("Load sample_code.py"):
    demo_file = Path(__file__).parent / "demo_files" / "sample_code.py"
    if demo_file.exists():
        st.session_state.code = demo_file.read_text()
        st.session_state.language = "Python"

# Initialize session state
if "code" not in st.session_state:
    st.session_state.code = ""
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "fixed_code" not in st.session_state:
    st.session_state.fixed_code = None

# Main UI
st.title("🤖 AI Code Fixer")
st.markdown("**Upload or paste your code, and let AI find and fix the bugs!**")

# File upload and code input
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📁 Upload File")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["py", "js"],
        help="Upload .py or .js files"
    )
    
    if uploaded_file is not None:
        st.session_state.code = uploaded_file.getvalue().decode("utf-8")
        st.session_state.language = "Python" if uploaded_file.name.endswith(".py") else "JavaScript"

with col2:
    st.markdown("### ✏️ Or Paste Code")
    code_input = st.text_area(
        "Paste your code here:",
        value=st.session_state.code,
        height=200,
        placeholder="# Paste your code here..."
    )
    if code_input != st.session_state.code:
        st.session_state.code = code_input

# Language selector for code
st.session_state.language = st.radio(
    "Language:",
    ["Python", "JavaScript"],
    horizontal=True,
    index=0 if st.session_state.language == "Python" else 1
)

# Action buttons
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    analyze_btn = st.button("🔍 Analyze Code", type="primary", use_container_width=True)

with col2:
    fix_btn = st.button("✨ Quick Fix", use_container_width=True)

with col3:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if clear_btn:
    st.session_state.code = ""
    st.session_state.analysis = None
    st.session_state.fixed_code = None
    st.rerun()

# Analyze function
def analyze_code(code, language, api_base, api_key, model):
    """Send code for analysis"""
    if not api_key:
        return {"error": "Please add your API key in the sidebar"}
    
    prompt = f"""You are a code analyzer. Analyze the following {language} code for bugs, errors, and issues.

For each issue found, provide:
1. Line number (if applicable)
2. Severity: critical, warning, or info
3. Description of the issue
4. Suggested fix

Code:
```{language.lower()}
{code}
```

Provide your analysis in this format:
### Issues Found:
1. [SEVERITY] Line X: Description
   - Fix: ...

2. [SEVERITY] Line Y: Description
   - Fix: ..."""

    try:
        url = f"{api_base}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return {"success": response.json()["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}

# Fix function
def fix_code(code, language, api_base, api_key, model):
    """Apply AI fix to code"""
    if not api_key:
        return {"error": "Please add your API key in the sidebar"}
    
    prompt = f"""You are a code fixer. Fix the bugs in the following {language} code.

Provide ONLY the corrected code, without explanations. Keep the same structure and comments.

Code:
```{language.lower()}
{code}
```

Fixed code:"""

    try:
        url = f"{api_base}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return {"success": response.json()["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}

# Handle analyze
if analyze_btn and st.session_state.code:
    with st.spinner("🔍 Analyzing code..."):
        result = analyze_code(
            st.session_state.code,
            st.session_state.language,
            api_base, api_key, model
        )
    st.session_state.analysis = result

# Handle fix
if fix_btn and st.session_state.code:
    with st.spinner("✨ Applying fixes..."):
        result = fix_code(
            st.session_state.code,
            st.session_state.language,
            api_base, api_key, model
        )
    st.session_state.fixed_code = result

# Display results
st.markdown("---")

if st.session_state.analysis:
    st.markdown("### 🔍 Analysis Results")
    
    if "error" in st.session_state.analysis:
        st.error(f"Error: {st.session_state.analysis['error']}")
    else:
        st.markdown(st.session_state.analysis["success"])

if st.session_state.fixed_code:
    st.markdown("### ✨ Fixed Code")
    
    if "error" in st.session_state.fixed_code:
        st.error(f"Error: {st.session_state.fixed_code['error']}")
    else:
        st.markdown('<div class="fix-success">✅ Code has been fixed!</div>', unsafe_allow_html=True)
        st.code(st.session_state.fixed_code["success"], language=st.session_state.language.lower())
        
        # Download button
        st.download_button(
            label="📥 Download Fixed Code",
            data=st.session_state.fixed_code["success"],
            file_name=f"fixed_code.{'py' if st.session_state.language == 'Python' else 'js'}",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>🤖 AI Code Fixer | Part of ai-coding-agent-demo</div>",
    unsafe_allow_html=True
)
