# Code Review Council - Powered by Claude Haiku 3.5

An AI-powered code review system using Claude Haiku 3.5 with 5 specialized agents.

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
- Wait for all 5 agents to analyze your code
- Choose whether to save results to JSON

## What Each Agent Does

1. **Security Agent** - Finds vulnerabilities and security issues
2. **Performance Agent** - Identifies bottlenecks and optimization opportunities
3. **Architecture Agent** - Reviews design patterns and code structure
4. **Testing Agent** - Suggests test cases and identifies testing gaps
5. **Documentation Agent** - Reviews and improves code documentation

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
Starting code review for: example.py
--------------------------------------------------
Running Security Agent...
✓ Security Agent completed
Running Performance Agent...
✓ Performance Agent completed
Running Architecture Agent...
✓ Architecture Agent completed
Running Testing Agent...
✓ Testing Agent completed
Running Documentation Agent...
✓ Documentation Agent completed
--------------------------------------------------
Review complete!

[Detailed feedback appears here]

Save detailed results to JSON? (y/n): y
Output filename (default: ReviewResults.json): 
Results saved to ReviewResults.json
```

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

## Support

For issues or questions, check the Anthropic documentation at https://docs.anthropic.com