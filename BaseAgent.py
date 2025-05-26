from abc import ABC, abstractmethod
from typing import Dict, Any
import anthropic
import os
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, config: Dict[str, Any]):
        self.name = name
        self.role = role
        self.config = config
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    @abstractmethod
    def get_prompt(self, code: str) -> str:
        pass
    
    def review(self, code: str) -> Dict[str, Any]:
        prompt = self.get_prompt(code)
        
        try:
            message = self.client.messages.create(
                model=self.config.get("model", "claude-3-5-haiku-20241022"),
                max_tokens=self.config.get("max_tokens", 4096),
                temperature=self.config.get("temperature", 0.3),
                system=f"You are a {self.role}. Provide specific, actionable feedback.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Get the text content - the API returns a list of content blocks
            # For a text-only response, we just need the first block's text
            if message.content and len(message.content) > 0:
                # Access the first content block and get its text
                content_block = message.content[0]
                # The content block should have a text attribute
                feedback = getattr(content_block, 'text', str(content_block))
            else:
                feedback = "No response generated."
                
        except Exception as e:
            feedback = f"Error during review: {str(e)}"
        
        return {
            "agent": self.name,
            "role": self.role,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }