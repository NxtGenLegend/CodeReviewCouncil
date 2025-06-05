import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import time

from ReviewGraph import CodeReviewGraph
from ReviewState import ReviewState

class CodeReviewCouncil:
    def __init__(self):
        self.graph = CodeReviewGraph()
        self.reviews = []
    
    def review_code(self, code: str, filename: str = "code.py") -> Dict[str, Any]:
        """Run code review using LangGraph workflow"""
        print(f"\n🔍 Starting code review for: {filename}")
        print("=" * 60)

        start_time = time.time()

        stages = [
            "Initializing review...",
            "Running syntax & logic analysis...",
            "Running security & performance analysis (parallel)...",
            "Running architecture & testing analysis (parallel)...",
            "Analyzing documentation...",
            "Generating report..."
        ]

        print(f"[{'░' * 10}] {stages[0]}", end="\r", flush=True)

        state = self.graph.review_code(code, filename)

        for i in range(1, 6):
            progress = "█" * (i * 2) + "░" * ((5 - i) * 2)
            if i < len(stages):
                print(f"\r[{progress}] {stages[i]}", end="", flush=True)
            time.sleep(0.1)  
        
        print(f"\r[{'█' * 10}] Review complete! (6 agents)")
        print("=" * 60)

        results = self._state_to_results(state, filename)
        self.reviews.append(results)
        
        return results
    
    def _state_to_results(self, state: ReviewState, filename: str) -> Dict[str, Any]:
        """Convert LangGraph state to legacy results format"""
        numbered_lines = []
        for i, line in enumerate(state["code_lines"], 1):
            numbered_lines.append(f"{i:4d} | {line}")
        numbered_code = '\n'.join(numbered_lines)

        reviews = []
        agent_findings = {}
        
        for finding in state["findings"]:
            agent = finding["agent"]
            if agent not in agent_findings:
                agent_findings[agent] = []
            agent_findings[agent].append(finding)

        for agent_name, summary in state["agent_summaries"].items():
            feedback_lines = []
            if agent_name in agent_findings:
                feedback_lines.append(f"Found {len(agent_findings[agent_name])} issues:\n")
                for i, finding in enumerate(agent_findings[agent_name], 1):
                    feedback_lines.append(f"{i}. {finding['issue']}")
                    if finding['fix']:
                        feedback_lines.append(f"   {finding['fix']}")
            else:
                feedback_lines.append("No issues found.")
            
            reviews.append({
                "agent": f"{agent_name} Agent",
                "role": f"{agent_name.lower()} specialist",
                "feedback": "\n".join(feedback_lines),
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "code_length": len(state["code_lines"]),
            "reviews": reviews,
            "numbered_code": numbered_code,
            "summary": {
                "total_issues": state["total_issues"],
                "critical_issues": state["critical_issues"],
                "warnings": state["warnings"],
                "suggestions": state["suggestions"],
                "by_agent": state["issues_by_agent"]
            }
        }
    
    def save_results(self, results: Dict[str, Any], output_file: str = "ReviewResults.json"):
        """Save results as JSON"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 JSON results saved to: {output_file}")
    
    def save_readable_report(self, results: Dict[str, Any], output_file: Optional[str] = None):
        """Save human-readable report as text file"""
        if not output_file:
            base_name = os.path.splitext(results["filename"])[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{base_name}_review_{timestamp}.txt"
        
        # Get the report from the graph state
        if hasattr(self, '_last_state') and self._last_state.get("final_report"):
            report_content = self._last_state["final_report"]
        else:
            # Fallback to generating from results
            report_content = self._generate_report_from_results(results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📝 Report saved to: {output_file}")
        return output_file
    
    def print_summary(self, results: Dict[str, Any]):
        """Print concise summary to terminal"""
        # Get the summary from the graph state
        if hasattr(self, '_last_state') and self._last_state.get("terminal_summary"):
            print(self._last_state["terminal_summary"])
        else:
            # Fallback to generating from results
            self._print_summary_from_results(results)
    
    def _generate_report_from_results(self, results: Dict[str, Any]) -> str:
        """Generate report from results (fallback)"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"CODE REVIEW REPORT - {results['filename']}")
        lines.append("=" * 80)
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Lines: {results['code_length']} | Model: Claude 3.5 Haiku")
        lines.append("=" * 80)
        
        summary = results.get("summary", {})
        if summary.get("total_issues", 0) > 0:
            lines.append(f"\nSUMMARY: {summary['total_issues']} issues found")
            lines.append("-" * 40)
            
            # Issues by type
            by_agent = summary.get("by_agent", {})
            if by_agent:
                issue_parts = [f"{agent}: {count}" for agent, count in by_agent.items() if count > 0]
                lines.append(" | ".join(issue_parts))
            
            # Severity
            severity_parts = []
            if summary.get('critical_issues', 0) > 0:
                severity_parts.append(f"Critical: {summary['critical_issues']}")
            if summary.get('warnings', 0) > 0:
                severity_parts.append(f"Warnings: {summary['warnings']}")
            if summary.get('suggestions', 0) > 0:
                severity_parts.append(f"Suggestions: {summary['suggestions']}")
            lines.append(" | ".join(severity_parts))
        
        lines.append("\n" + "=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _print_summary_from_results(self, results: Dict[str, Any]):
        """Print summary from results (fallback)"""
        print("\n" + "=" * 60)
        print("📊 REVIEW SUMMARY")
        print("=" * 60)
        
        summary = results.get("summary", {})
        print(f"\n📈 Total Issues Found: {summary.get('total_issues', 0)}")
        
        # Issues by type
        print("\n🔍 Issues by Type:")
        by_agent = summary.get("by_agent", {})
        icons = {
            "Syntax & Logic": "🐛",
            "Security": "🔒",
            "Performance": "⚡",
            "Architecture": "🏗️",
            "Testing": "🧪",
            "Documentation": "📝"
        }
        
        for agent_type, count in by_agent.items():
            icon = icons.get(agent_type, "•")
            print(f"   {icon} {agent_type}: {count} issues")

        print("\n⚠️  Severity Breakdown:")
        print(f"   • Critical: {summary.get('critical_issues', 0)} 🔴")
        print(f"   • Warnings: {summary.get('warnings', 0)} 🟡")
        print(f"   • Suggestions: {summary.get('suggestions', 0)} 🟢")
        
        print("\n" + "=" * 60)
        print("✅ Review complete!")
        print("=" * 60)
    
    def review_code(self, code: str, filename: str = "code.py") -> Dict[str, Any]:
        """Run code review using LangGraph workflow"""
        print(f"\n🔍 Starting code review for: {filename}")
        print("=" * 60)
        
        print("🔄 Executing review graph with parallel processing...")
        
        state = self.graph.review_code(code, filename)

        self._last_state = state
        
        print("\n✅ Graph execution complete!")
        print("=" * 60)
        
        results = self._state_to_results(state, filename)
        self.reviews.append(results)
        
        return results