from BaseAgent import BaseAgent

class DocumentationAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Documentation Agent", 
            "technical documentation specialist",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Review this code for documentation issues:

{code}

Focus ONLY on significant documentation problems:
1. Missing docstrings for complex functions/classes
2. Incorrect or misleading documentation
3. Missing parameter/return type documentation for public APIs
4. Undocumented exceptions or side effects
5. Complex logic without explanatory comments

DO NOT report on:
- Simple getter/setter methods
- Self-explanatory variable names
- Minor formatting preferences

If documentation is adequate, simply state "Documentation is adequate."

For each issue found, specify:
- The line number
- What documentation is missing or wrong
- A brief suggestion for improvement"""