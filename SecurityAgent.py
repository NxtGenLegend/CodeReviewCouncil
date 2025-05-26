from BaseAgent import BaseAgent

class SecurityAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Security Agent", 
            "security expert focused on vulnerabilities and secure coding practices",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Analyze this code for security vulnerabilities:

{code}

Focus on:
1. Authentication and authorization issues
2. Input validation and sanitization
3. SQL injection, XSS, CSRF vulnerabilities
4. Encryption and data protection
5. Secure communication patterns
6. Dependency vulnerabilities
7. Secret management

Provide specific vulnerabilities found and how to fix them."""