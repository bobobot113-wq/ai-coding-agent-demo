# AI Coding Agent Demo 🤖

A simple demonstration of how AI coding agents work, featuring:
- **Task Planning** - AI breaks down complex tasks into steps
- **File Analysis** - Read and analyze source code
- **Code Review** - AI-powered code review suggestions
- **Autonomous Execution** - Agents can execute multi-step tasks

## What's Included

### 1. `agent_demo.py` - Main Demo Script
A Python script that demonstrates a simple AI coding agent that can:
- Analyze Python code files
- Suggest improvements and fixes
- Generate code documentation
- Run autonomously on multiple files

### 2. `demo_files/` - Sample Code to Analyze
- `sample_code.py` - Python code with intentional issues for the agent to analyze
- `buggy_calculator.py` - A simple calculator with bugs for the agent to fix

## How It Works

The demo uses a simple agent architecture:
```
User Request → Task Planning → Execution Loop → Result
                    ↓
              [Analyze] → [Plan] → [Execute] → [Verify]
```

## Running the Demo

```bash
# Install dependencies
pip install openai anthropic

# Set your API key (or use mock mode)
export OPENAI_API_KEY="your-key"
# OR
export ANTHROPIC_API_KEY="your-key"

# Run the demo
python agent_demo.py
```

### Mock Mode
The demo includes a mock AI mode that doesn't require API keys - it demonstrates the agent workflow using rule-based responses.

```bash
python agent_demo.py --mock
```

## Demo Features

1. **Code Analyzer** - Reads and analyzes Python files for issues
2. **Task Decomposer** - Breaks complex tasks into executable steps
3. ** autonomous Runner** - Executes tasks step-by-step
4. **Results Reporter** - Summarizes what the agent did

## Example Output

```
🤖 AI Coding Agent Demo
=======================

📁 Analyzing: demo_files/sample_code.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Task: Analyze code quality and suggest improvements

📋 Steps planned:
  1. Read and parse the source file
  2. Identify code patterns and structure
  3. Detect potential issues
  4. Generate improvement suggestions

⚡ Executing step 1: Reading source file...
⚡ Executing step 2: Analyzing code structure...
⚡ Executing step 3: Detecting issues...
⚡ Executing step 4: Generating suggestions...

✅ Analysis Complete!

📝 Findings:
  - Function 'process_data' could use better error handling
  - Consider adding type hints for better code clarity
  - 2 opportunities for optimization found

💡 Suggestions:
  1. Add try/except around file operations
  2. Add type hints: process_data(data: list) -> dict
  3. Consider using list comprehension for filtering
```

## Requirements

- Python 3.8+
- Optional: OpenAI or Anthropic API key for real AI responses

## Learn More

This demo is inspired by the latest AI coding agents:
- **Claude Code** (Anthropic) - Best for multi-file refactoring
- **GPT-5 Codex** (OpenAI) - Great for precise code implementation
- **Gemini 3 Pro** (Google) - Strong for backend logic

These agents can now autonomously:
- Build entire features with minimal supervision
- Work across multiple large files
- Test and verify their own code
- Handle complex multi-step debugging tasks

## License

MIT License - Feel free to use and modify!

---

## 🌐 Web UI (NEW!)

A Streamlit web interface is now available!

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Features

- 📁 Upload .py and .js files
- ✏️ Paste code directly  
- 🔍 Analyze code for bugs
- ✨ One-click "Quick Fix"
- 📊 Beautiful results display
- 🔑 Configurable API (MiniMax, OpenAI, Anthropic)

### Demo Files

Load sample buggy files directly from the sidebar!
