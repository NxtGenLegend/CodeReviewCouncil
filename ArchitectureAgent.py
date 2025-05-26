from BaseAgent import BaseAgent

class ArchitectureAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Architecture Agent", 
            "software architecture expert",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Review this code for architectural quality:

{code}

Focus on:
1. SOLID principles adherence
2. Design pattern usage and appropriateness
3. Code modularity and coupling
4. Separation of concerns
5. Dependency management
6. Scalability considerations
7. Maintainability issues

Provide specific architectural improvements."""