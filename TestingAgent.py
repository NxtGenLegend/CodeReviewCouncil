from BaseAgent import BaseAgent

class TestingAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Testing Agent", 
            "testing and quality assurance specialist",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Analyze this code from a testing perspective:

{code}

Focus on:
1. Missing test cases
2. Edge cases not covered
3. Test coverage gaps
4. Testability issues
5. Mock/stub requirements
6. Integration test needs
7. Error handling validation

Generate specific test cases and identify testing gaps."""