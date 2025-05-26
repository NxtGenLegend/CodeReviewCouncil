from BaseAgent import BaseAgent

class PerformanceAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            "Performance Agent", 
            "performance optimization specialist",
            config
        )
    
    def get_prompt(self, code: str) -> str:
        return f"""Analyze this code for performance issues:

{code}

Focus on:
1. Time complexity analysis
2. Space complexity issues
3. Database query optimization
4. Caching opportunities
5. Algorithmic improvements
6. Resource bottlenecks
7. Async/parallel processing opportunities

Provide specific performance issues and optimization suggestions."""