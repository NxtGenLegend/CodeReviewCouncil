import json
import os
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import textwrap

from SecurityAgent import SecurityAgent
from PerformanceAgent import PerformanceAgent
from ArchitectureAgent import ArchitectureAgent
from TestingAgent import TestingAgent
from DocumentationAgent import DocumentationAgent

def load_config():
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        "model": "claude-3-5-haiku-20241022",
        "temperature": 0.3,
        "max_tokens": 4096
    }

class CodeReviewCouncil:
    def __init__(self):
        self.config = load_config()
        enable_agents = self.config.get("enable_agents", {})
        
        self.agents = []
        if enable_agents.get("security", True):
            self.agents.append(SecurityAgent(self.config))
        if enable_agents.get("performance", True):
            self.agents.append(PerformanceAgent(self.config))
        if enable_agents.get("architecture", True):
            self.agents.append(ArchitectureAgent(self.config))
        if enable_agents.get("testing", True):
            self.agents.append(TestingAgent(self.config))
        if enable_agents.get("documentation", True):
            self.agents.append(DocumentationAgent(self.config))
        
        self.reviews = []
    
    def add_line_numbers(self, code: str) -> Tuple[str, Dict[int, str]]:
        """Add line numbers to code for reference"""
        lines = code.split('\n')
        numbered_lines = {}
        numbered_code = []
        
        for i, line in enumerate(lines, 1):
            numbered_lines[i] = line
            numbered_code.append(f"{i:4d} | {line}")
        
        return '\n'.join(numbered_code), numbered_lines
    
    def review_code(self, code: str, filename: str = "code.py") -> Dict[str, Any]:
        print(f"\n🔍 Starting code review for: {filename}")
        print("=" * 60)
        
        # Add line numbers for reference
        numbered_code, line_map = self.add_line_numbers(code)
        
        results = {
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
            "code_length": len(code.splitlines()),
            "reviews": [],
            "numbered_code": numbered_code,
            "summary": {
                "total_issues": 0,
                "critical_issues": 0,
                "warnings": 0,
                "suggestions": 0
            }
        }
        
        # Progress bar setup
        total_agents = len(self.agents)
        
        for idx, agent in enumerate(self.agents, 1):
            progress = "█" * (idx * 10 // total_agents) + "░" * ((total_agents - idx) * 10 // total_agents)
            print(f"\r[{progress}] Running {agent.name}... ({idx}/{total_agents})", end="", flush=True)
            
            try:
                review = agent.review(code)
                results["reviews"].append(review)
                
                # Update summary counts (simplified for now)
                if "critical" in review.get("feedback", "").lower():
                    results["summary"]["critical_issues"] += 1
                elif "warning" in review.get("feedback", "").lower():
                    results["summary"]["warnings"] += 1
                else:
                    results["summary"]["suggestions"] += 1
                
                results["summary"]["total_issues"] += 1
                
            except Exception as e:
                results["reviews"].append({
                    "agent": agent.name,
                    "error": str(e)
                })
        
        print(f"\r[{'█' * 10}] Review complete! ({total_agents}/{total_agents})")
        print("=" * 60)
        
        self.reviews.append(results)
        return results
    
    def save_results(self, results: Dict[str, Any], output_file: str = "ReviewResults.json"):
        """Save results as JSON"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 JSON results saved to: {output_file}")
    
    def save_readable_report(self, results: Dict[str, Any], output_file:  Optional[str] = None):
        """Save human-readable report as text file"""
        if not output_file:
            base_name = os.path.splitext(results["filename"])[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{base_name}_review_{timestamp}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("CODE REVIEW REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"File: {results['filename']}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Lines of Code: {results['code_length']}\n")
            f.write("Model: Claude 3.5 Haiku\n")
            f.write("\n" + "=" * 80 + "\n\n")
            
            # Code with line numbers
            f.write("ORIGINAL CODE (with line numbers):\n")
            f.write("-" * 80 + "\n")
            f.write(results.get("numbered_code", "Code not available"))
            f.write("\n\n" + "=" * 80 + "\n\n")
            
            # Summary
            summary = results.get("summary", {})
            f.write("SUMMARY:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Issues Found: {summary.get('total_issues', 0)}\n")
            f.write(f"Critical Issues: {summary.get('critical_issues', 0)}\n")
            f.write(f"Warnings: {summary.get('warnings', 0)}\n")
            f.write(f"Suggestions: {summary.get('suggestions', 0)}\n")
            f.write("\n" + "=" * 80 + "\n\n")
            
            # Detailed reviews from each agent
            f.write("DETAILED ANALYSIS:\n")
            f.write("=" * 80 + "\n\n")
            
            for review in results["reviews"]:
                if "error" in review:
                    f.write(f"[{review['agent']}] - ERROR\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"Error: {review['error']}\n\n")
                else:
                    f.write(f"[{review['agent'].upper()}]\n")
                    f.write("-" * 80 + "\n")
                    
                    # Format the feedback with proper line wrapping
                    feedback = review.get('feedback', 'No feedback available')
                    
                    # Split feedback into paragraphs and wrap each
                    paragraphs = feedback.split('\n\n')
                    for paragraph in paragraphs:
                        if paragraph.strip():
                            # Handle code blocks specially
                            if '```' in paragraph:
                                f.write(paragraph + "\n\n")
                            else:
                                # Wrap normal text
                                wrapped = textwrap.fill(paragraph, width=80, 
                                                       break_long_words=False,
                                                       break_on_hyphens=False)
                                f.write(wrapped + "\n\n")
                    
                    f.write("\n" + "=" * 80 + "\n\n")
            
            # Footer
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"📝 Detailed report saved to: {output_file}")
        return output_file
    
    def print_summary(self, results: Dict[str, Any]):
        """Print concise summary to terminal"""
        print("\n" + "=" * 60)
        print("📊 REVIEW SUMMARY")
        print("=" * 60)
        
        # Summary stats
        summary = results.get("summary", {})
        print("\n📈 Issues Found:")
        print(f"   • Total Issues: {summary.get('total_issues', 0)}")
        print(f"   • Critical: {summary.get('critical_issues', 0)} 🔴")
        print(f"   • Warnings: {summary.get('warnings', 0)} 🟡")
        print(f"   • Suggestions: {summary.get('suggestions', 0)} 🟢")
        
        # Quick summary from each agent (just the first line or key finding)
        print("\n🔍 Key Findings by Agent:")
        for review in results["reviews"]:
            if "error" not in review:
                agent_name = review['agent']
                feedback = review.get('feedback', '')
                # Get first significant line from feedback
                first_line = feedback.split('\n')[0][:60] + "..." if feedback else "No issues found"
                print(f"   • {agent_name}: {first_line}")
        
        print("\n" + "=" * 60)
        print("✅ Review complete! Check the detailed report for full analysis.")
        print("=" * 60)