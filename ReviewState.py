from typing import TypedDict, List, Dict, Optional
from typing_extensions import Annotated
import operator

class AgentFinding(TypedDict):
    agent: str
    line: int
    issue: str
    severity: str  
    fix: str

class ReviewState(TypedDict):
    """Shared state between all agents in the review graph"""
    code: str
    filename: str
    code_lines: List[str]
    
    findings: Annotated[List[AgentFinding], operator.add]
    agent_summaries: Dict[str, str]
    
    total_issues: int
    critical_issues: int
    warnings: int
    suggestions: int
    issues_by_agent: Dict[str, int]
    
    has_syntax_errors: bool
    has_security_issues: bool
    needs_performance_review: bool
    skip_documentation: bool
    
    final_report: Optional[str]
    terminal_summary: Optional[str]