from BaseAgent import BaseAgent

class TestingAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Testing Agent", 
            "testing and quality assurance specialist",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Analyze this code for critical testing gaps:

{code}

Focus ONLY on significant testing issues:
1. Untested edge cases that could cause failures
2. Missing validation for critical functions
3. Error handling that needs testing
4. Security-critical code without tests
5. Complex logic without test coverage

DO NOT report on:
- Simple getter/setter testing
- Basic CRUD operations
- Trivial functions

If testing needs are minimal, state "Basic testing adequate for this code."

For each critical gap, specify:
- What needs testing (with line reference)
- Why it's important to test
- One specific test case example"""