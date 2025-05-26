from BaseAgent import BaseAgent

class DocumentationAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Documentation Agent", 
            "technical documentation specialist",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Review and generate documentation for this code:

{code}

Focus on:
1. Missing or unclear function/class documentation
2. API documentation needs
3. Complex logic that needs explanation
4. Architecture decisions that should be documented
5. Usage examples needed
6. Parameter and return value documentation
7. Error states and exceptions

Provide specific documentation improvements and generate missing docs."""