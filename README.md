# Code Review Council - Powered by Claude Haiku 3.5

A multi-agent code review system using Claude Haiku 3.5 with 6 specialized agents.

## What You Need

1. **Python 3.7 or higher**
2. **Anthropic API Key** - Get one at https://console.anthropic.com/api-keys

## Quick Setup

### Step 1: Install Dependencies
```bash
pip install anthropic
```

### Step 2: Set Up Your API Key
```bash
python setup.py
```

When prompted:
- Enter your Anthropic API key (starts with "sk-ant-api03-...")
- Choose option 1 (environment variable) or 2 (.env file)

### Step 3: Run the Code Review
```bash
python main.py
```

When prompted:
- Enter the path to the code file you want to review (e.g., `example.py`)
- Wait for all 6 agents to analyze your code
- Choose whether to save results to text file

## What Each Agent Does

1. **Syntax & Logic Agent** - Finds bugs, logic errors, and correctness issues
2. **Security Agent** - Finds vulnerabilities and security issues
3. **Performance Agent** - Identifies bottlenecks and optimization opportunities
4. **Architecture Agent** - Reviews design patterns and code structure
5. **Testing Agent** - Suggests test cases and identifies testing gaps
6. **Documentation Agent** - Reviews and improves code documentation

## Try the Demo (No API Key Needed!)

```bash
python DemoMode.py
```

This shows how the system works without using your API credits.

## Review Multiple Files

```bash
python BatchReview.py /path/to/your/project
```

## File Structure

```
├── main.py              # Main entry point
├── BaseAgent.py         # Base class for all agents
├── SyntaxLogicAgent.py  # Syntax and logic error detection
├── SecurityAgent.py     # Security analysis
├── PerformanceAgent.py  # Performance analysis
├── ArchitectureAgent.py # Architecture review
├── TestingAgent.py      # Testing recommendations
├── DocumentationAgent.py # Documentation review
├── CodeReviewCouncil.py # Orchestrates all agents
├── BatchReview.py       # Review multiple files
├── DemoMode.py          # Demo without API
├── setup.py             # API key setup
├── config.json          # Configuration
├── example.py           # Example code to test
└── README.md            # This file
```

## Configuration

Edit `config.json` to:
- Change the Claude model (default: claude-3-5-haiku-20241022)
- Enable/disable specific agents
- Adjust temperature and max tokens

## Example Usage

```bash
$ python main.py
Enter the path to the code file to review: example.py

📂 Reading example.py...
📏 File size: 37 lines

🔍 Starting code review for: example.py
============================================================
[████████████] Review complete! (6/6)
============================================================

============================================================
📊 REVIEW SUMMARY
============================================================

📈 Total Issues Found: 17

🔍 Issues by Type:
   🐛 Syntax & Logic: 3 issues
   🔒 Security: 3 issues
   ⚡ Performance: 2 issues
   🏗️ Architecture: 3 issues
   🧪 Testing: 3 issues
   📝 Documentation: 3 issues

⚠️  Severity Breakdown:
   • Critical: 5 🔴
   • Warnings: 8 🟡
   • Suggestions: 4 🟢

💡 Key Findings:
   • Syntax & Logic Agent: List Modification During Iteration (Lines 9-12)
   • Security Agent: SQL Injection (Line 2)
   • Performance Agent: O(n²) Algorithm (Lines 9-12)
   • Architecture Agent: Tight Coupling - Data access mixed with business logic
   • Testing Agent: SQL Injection Testing (Line 2) - Security-critical code untested
   • Documentation Agent: Missing Function Docstrings

============================================================
✅ Review complete! Check the detailed report for full analysis.
============================================================

💾 Save Options:
Save detailed report as .txt? (y/n): y

📝 Detailed report saved to: example_review_20241120_143022.txt

✨ Success! Review saved to: example_review_20241120_143022.txt
   Contains:
   • Summary of issues found
   • Detailed findings by agent
   • Line-specific references
   • Recommended fixes

Also save raw data as JSON? (y/n): n

🎉 Done! Thanks for using Code Review Council.
```

## Output Files

The system generates two types of output:

1. **Text Report** (Recommended)
   - Human-readable format
   - Includes line numbers and code references
   - Detailed analysis from each agent
   - Code examples and fixes
   - Example: `example_review_20241120_143022.txt`

2. **JSON File** (Optional)
   - Raw data for integration with other tools
   - Machine-readable format
   - Example: `ReviewResults.json`

## Cost

Claude Haiku 3.5 is very affordable:
- ~$0.25 per million input tokens
- ~$1.25 per million output tokens
- A typical code review costs less than $0.01

## Troubleshooting

**"API key not found" error**
- Make sure you ran `python setup.py` and entered your key
- On Windows, restart your terminal after setup

**"No module named 'anthropic'" error**
- Run: `pip install anthropic`

**"File not found" error**
- Make sure the file path is correct
- Try using the full path to your code file