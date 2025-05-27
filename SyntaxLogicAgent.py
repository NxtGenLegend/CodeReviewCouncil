from BaseAgent import BaseAgent

class SyntaxLogicAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Syntax & Logic Agent", 
            "code correctness and logic error detection specialist",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Analyze this code for syntax errors, logic bugs, and correctness issues:

{code}

Focus ONLY on actual errors and bugs:
1. Syntax errors or near-syntax issues
2. Logic errors (off-by-one, incorrect conditions, infinite loops)
3. Type mismatches or incorrect type usage
4. Unreachable code or dead code paths
5. Resource leaks (unclosed files, connections)
6. Race conditions or concurrency issues
7. Incorrect algorithm implementation

DO NOT report on style, naming conventions, or best practices - only actual bugs.
If there are no syntax or logic errors, simply state "No syntax or logic errors found."

For each issue found, specify:
- The line number where it occurs
- What the error is
- Why it's wrong
- How to fix it"""