#!/usr/bin/env python3
"""
AI Coding Agent Demo
=====================
A demonstration of how AI coding agents work for automated coding tasks.

This demo shows:
- Task planning and decomposition
- File analysis and code review
- Autonomous multi-step execution
- Results reporting

Usage:
    python agent_demo.py [--mock] [--file <filename>]
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text: str, color: str = '') -> None:
    """Print colored text to terminal."""
    print(f"{color}{text}{Colors.ENDC}")

@dataclass
class TaskStep:
    """Represents a single step in a task."""
    step_id: int
    description: str
    status: str = "pending"  # pending, executing, completed, failed
    
class CodeAnalyzer:
    """Analyzes Python code for issues and improvements."""
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a Python file and return findings."""
        print_colored(f"\n📁 Analyzing: {filepath}", Colors.CYAN)
        print_colored("━" * 50, Colors.CYAN)
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return {"error": f"File not found: {filepath}"}
        except Exception as e:
            return {"error": str(e)}
        
        # Analyze the code
        findings = self._perform_analysis(content, filepath)
        return findings
    
    def _perform_analysis(self, content: str, filepath: str) -> Dict[str, Any]:
        """Perform actual code analysis."""
        if self.use_mock:
            return self._mock_analysis(content, filepath)
        else:
            return self._ai_analysis(content, filepath)
    
    def _mock_analysis(self, content: str, filepath: str) -> Dict[str, Any]:
        """Mock analysis using rule-based detection."""
        issues = []
        suggestions = []
        stats = {
            "lines": len(content.split('\n')),
            "functions": len(re.findall(r'def\s+(\w+)', content)),
            "classes": len(re.findall(r'class\s+(\w+)', content)),
            "imports": len(re.findall(r'^import\s+|^from\s+', content, re.MULTILINE))
        }
        
        # Check for common issues
        if 'print(' in content and 'logging not in content:
'            issues.append("Using print() instead of proper logging")
            suggestions.append("Consider using the logging module for production code")
        
        if 'except:' in content:
            issues.append("Bare except clause found")
            suggestions.append("Use specific exception types: except ValueError as e:")
        
        if 'global ' in content:
            issues.append("Using global variables")
            suggestions.append("Consider passing variables as parameters or using classes")
        
        if not re.search(r'type\s+\w+\s*=\s*', content) and not re.search(r'def\s+\w+.*\)->', content):
            if stats['functions'] > 0:
                suggestions.append("Consider adding type hints for better code clarity")
        
        if len(content.split('\n')) > 100:
            suggestions.append("File is quite long - consider splitting into modules")
        
        # Check for TODOs
        todos = re.findall(r'#\s*TODO:?\s*(.+)', content, re.IGNORECASE)
        
        return {
            "filepath": filepath,
            "stats": stats,
            "issues": issues,
            "suggestions": suggestions,
            "todos": todos,
            "summary": self._generate_summary(issues, suggestions, stats)
        }
    
    def _ai_analysis(self, content: str, filepath: str) -> Dict[str, Any]:
        """Use AI for analysis (placeholder for API integration)."""
        # This would integrate with OpenAI/Anthropic API
        return self._mock_analysis(content, filepath)
    
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


class AICodingAgent:
    """A simple AI coding agent that demonstrates autonomous coding."""
    
    def __init__(self, name: str = "Agent", use_mock: bool = True):
        self.name = name
        self.use_mock = use_mock
        self.analyzer = CodeAnalyzer(use_mock)
        
    def execute_task(self, task: str, target: str) -> Dict[str, Any]:
        """Execute a coding task on a target (file or directory)."""
        print_colored(f"\n🤖 {self.name} - Executing Task", Colors.HEADER)
        print_colored(f"📌 Task: {task}", Colors.YELLOW)
        print_colored(f"🎯 Target: {target}\n", Colors.YELLOW)
        
        # Step 1: Plan the task
        steps = self._plan_task(task, target)
        
        # Step 2: Execute each step
        results = []
        for step in steps:
            print_colored(f"\n⚡ Executing step {step.step_id}: {step.description}", Colors.BLUE)
            step.status = "executing"
            
            # Simulate work
            import time
            time.sleep(0.3)  # Brief pause for effect
            
            result = self._execute_step(step, target)
            step.status = "completed"
            results.append(result)
            
            print_colored(f"✅ Step {step.step_id} complete", Colors.GREEN)
        
        # Step 3: Summarize results
        summary = self._summarize_results(task, results)
        
        return {
            "task": task,
            "target": target,
            "steps": steps,
            "results": results,
            "summary": summary
        }
    
    def _plan_task(self, task: str, target: str) -> List[TaskStep]:
        """Plan the task by breaking it into steps."""
        print_colored("\n📋 Planning task...", Colors.CYAN)
        
        steps = []
        
        if "analyze" in task.lower() or "review" in task.lower():
            steps = [
                TaskStep(1, "Read and parse the source file"),
                TaskStep(2, "Identify code patterns and structure"),
                TaskStep(3, "Detect potential issues and bugs"),
                TaskStep(4, "Generate improvement suggestions"),
            ]
        elif "fix" in task.lower() or "bug" in task.lower():
            steps = [
                TaskStep(1, "Read the source file"),
                TaskStep(2, "Identify bugs and issues"),
                TaskStep(3, "Generate fix suggestions"),
                TaskStep(4, "Apply fixes to code"),
            ]
        elif "document" in task.lower() or "docs" in task.lower():
            steps = [
                TaskStep(1, "Read source code"),
                TaskStep(2, "Extract function signatures and docstrings"),
                TaskStep(3, "Generate documentation"),
            ]
        else:
            # Default generic task
            steps = [
                TaskStep(1, "Analyze the target"),
                TaskStep(2, "Process the request"),
                TaskStep(3, "Generate output"),
            ]
        
        for step in steps:
            print_colored(f"  → {step.step_id}. {step.description}", Colors.BLUE)
        
        return steps
    
    def _execute_step(self, step: TaskStep, target: str) -> Any:
        """Execute a single step."""
        # In a real agent, this would call AI APIs
        # Here we simulate with our analyzer
        if step.step_id == 1 and "analyze" in self.name.lower():
            return {"status": "read", "content": "File read successfully"}
        
        if step.step_id == 3 and "analyze" in self.name.lower():
            # Return actual analysis
            return self.analyzer.analyze_file(target)
        
        return {"status": "completed", "step": step.step_id}
    
    def _summarize_results(self, task: str, results: List[Any]) -> str:
        """Summarize the execution results."""
        return f"Task '{task}' completed successfully with {len(results)} steps executed."


def print_results(results: Dict[str, Any]) -> None:
    """Print the task results in a nice format."""
    print_colored("\n" + "=" * 50, Colors.HEADER)
    print_colored("✅ Task Complete!", Colors.GREEN)
    print_colored("=" * 50 + "\n", Colors.HEADER)
    
    # Print summary
    print_colored("📝 Summary:", Colors.BOLD)
    print(f"  {results['summary']}\n")
    
    # Print detailed results if analysis was done
    for i, result in enumerate(results['results']):
        if isinstance(result, dict) and 'issues' in result:
            print_colored(f"\n📊 Analysis Results (Step {i+1}):", Colors.BOLD)
            
            if result.get('stats'):
                print_colored("\n📈 Code Statistics:", Colors.CYAN)
                for key, value in result['stats'].items():
                    print(f"  • {key}: {value}")
            
            if result.get('issues'):
                print_colored("\n🚨 Issues Found:", Colors.RED)
                for issue in result['issues']:
                    print(f"  ❌ {issue}")
            
            if result.get('suggestions'):
                print_colored("\n💡 Suggestions:", Colors.YELLOW)
                for suggestion in result['suggestions']:
                    print(f"  💡 {suggestion}")
            
            if result.get('todos'):
                print_colored("\n📌 TODOs:", Colors.BLUE)
                for todo in result['todos']:
                    print(f"  ☑️ {todo}")
    
    print()


def main():
    """Main entry point for the demo."""
    parser = argparse.ArgumentParser(description="AI Coding Agent Demo")
    parser.add_argument('--mock', action='store_true', default=True,
                        help="Use mock AI mode (no API key required)")
    parser.add_argument('--file', type=str, default='demo_files/sample_code.py',
                        help="File to analyze")
    parser.add_argument('--task', type=str, default='analyze',
                        help="Task to perform (analyze, fix, document)")
    
    args = parser.parse_args()
    
    # Print header
    print_colored("""
    🤖 AI Coding Agent Demo
    ═══════════════════════
    """, Colors.HEADER)
    
    print_colored("This demo shows how AI coding agents work!\n", Colors.CYAN)
    
    # Get the demo files directory
    demo_dir = Path(__file__).parent / "demo_files"
    target_file = demo_dir / args.file.replace("demo_files/", "")
    
    if not target_file.exists():
        # Try current directory
        target_file = Path(args.file)
    
    if not target_file.exists():
        print_colored(f"❌ File not found: {target_file}", Colors.RED)
        print("\nAvailable demo files in demo_files/:")
        for f in Path("demo_files").glob("*.py"):
            print(f"  - {f.name}")
        sys.exit(1)
    
    # Create the agent
    agent = AICodingAgent(name="CodeAnalyzer Agent", use_mock=args.mock)
    
    # Execute the task
    results = agent.execute_task(
        task=f"{args.task} code quality and suggest improvements",
        target=str(target_file)
    )
    
    # Print results
    print_results(results)
    
    # Show how different tasks work
    print_colored("\n🔄 Trying different task types...\n", Colors.HEADER)
    
    # Document task
    print_colored("📄 Task: Generate Documentation", Colors.CYAN)
    agent2 = AICodingAgent(name="DocAgent", use_mock=args.mock)
    results2 = agent2.execute_task("document", str(target_file))
    print_results(results2)


if __name__ == "__main__":
    main()
