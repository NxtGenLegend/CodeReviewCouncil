# Setup & Run Instructions

## What You Need to Input

1. **Anthropic API Key** (required)
   - Get it from: https://console.anthropic.com/api-keys
   - It looks like: `sk-ant-api03-xxxxx...`
   - You'll enter this when running `setup.py`

2. **Code File Path** (when running reviews)
   - The path to the file you want to review
   - Example: `example.py` or `/Users/yourname/project/mycode.py`

## How to Run - Step by Step

### First Time Setup (Do This Once)

```bash
# 1. Install the required package
pip install anthropic

# 2. Run setup to configure your API key
python setup.py

# 3. When prompted, enter your Anthropic API key
# 4. Choose option 1 (recommended) to save as environment variable
```

### Running Code Reviews

```bash
# Option 1: Review a single file
python main.py
# Then enter: example.py (or path to your code file)

# Option 2: Try the demo (no API key needed)
python DemoMode.py

# Option 3: Review all files in a directory
python BatchReview.py /path/to/your/project
```

## Quick Test

1. First, try the demo to see how it works:
   ```bash
   python DemoMode.py
   ```

2. Then review the example file:
   ```bash
   python main.py
   # When prompted, type: example.py
   ```

## What Happens

1. The system reads your code file
2. Shows a progress bar as each agent analyzes:
   - Syntax & Logic Agent → finds bugs and logic errors
   - Security Agent → finds vulnerabilities
   - Performance Agent → finds slow code
   - Architecture Agent → checks design
   - Testing Agent → suggests tests
   - Documentation Agent → improves docs
3. Terminal shows only a brief summary
4. Save detailed analysis to a .txt file (recommended)
5. Optionally also save raw data as JSON

## What You'll See

**Terminal (Clean & Informative):**
- Progress bar during analysis
- Total issues found
- Breakdown by type (Syntax: 3, Security: 3, Performance: 2, etc.)
- Breakdown by severity (Critical/Warning/Suggestion)
- Actual findings from each agent (not generic text)

**Text Report File (Full Details):**
- Your code with line numbers
- Complete analysis from each agent
- Specific line references (e.g., "Line 2: SQL injection")
- Code examples and fixes
- Formatted for easy reading

## Files You Can Review

- Python files (`.py`)
- JavaScript files (`.js`)
- Java files (`.java`)
- C/C++ files (`.c`, `.cpp`)
- And more (see config.json)

## Total Time

- Setup: ~2 minutes
- Per file review: ~10-30 seconds (depending on file size)

## Cost

- Using Claude Haiku 3.5 (fastest and cheapest)
- Typical cost: less than $0.01 per file
- Demo mode: FREE (no API calls)

That's it! The system is designed to be simple and straightforward.