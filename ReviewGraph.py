from langgraph.graph import StateGraph, END
from typing import Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime

from ReviewState import ReviewState, AgentFinding
from SyntaxLogicAgent import SyntaxLogicAgent
from SecurityAgent import SecurityAgent
from PerformanceAgent import PerformanceAgent
from ArchitectureAgent import ArchitectureAgent
from TestingAgent import TestingAgent
from DocumentationAgent import DocumentationAgent
from utils import analyze_severity, extract_key_finding

class CodeReviewGraph:
    def __init__(self):
        self.config = self.load_config()
        self.workflow = self._build_graph()
        
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            return {
                "model": "claude-3-5-haiku-20241022",
                "temperature": 0.3,
                "max_tokens": 4096
            }
    
    def _build_graph(self) -> StateGraph:
        """Build the review workflow graph"""
        workflow = StateGraph(ReviewState)
        
        workflow.add_node("initialize", self.initialize_review)
        workflow.add_node("syntax_analysis", self.syntax_analysis_node)
        workflow.add_node("security_performance_parallel", self.security_performance_parallel_node)
        workflow.add_node("architecture_testing_parallel", self.architecture_testing_parallel_node)
        workflow.add_node("documentation_analysis", self.documentation_analysis_node)
        workflow.add_node("generate_report", self.generate_report_node)
        
        workflow.set_entry_point("initialize")
        workflow.add_edge("initialize", "syntax_analysis")
        workflow.add_edge("syntax_analysis", "security_performance_parallel")
        workflow.add_edge("security_performance_parallel", "architecture_testing_parallel")
        
        workflow.add_conditional_edges(
            "architecture_testing_parallel",
            lambda state: "documentation_analysis" if not state["skip_documentation"] else "generate_report",
            {
                "documentation_analysis": "documentation_analysis",
                "generate_report": "generate_report"
            }
        )
        
        workflow.add_edge("documentation_analysis", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    def initialize_review(self, state: ReviewState) -> ReviewState:
        """Initialize the review state"""
        code_lines = state["code"].split('\n')
        
        state["code_lines"] = code_lines
        state["findings"] = []
        state["agent_summaries"] = {}
        state["total_issues"] = 0
        state["critical_issues"] = 0
        state["warnings"] = 0
        state["suggestions"] = 0
        state["issues_by_agent"] = {}
        state["has_syntax_errors"] = False
        state["has_security_issues"] = False
        state["needs_performance_review"] = True
        state["skip_documentation"] = len([line for line in code_lines if line.strip() and not line.strip().startswith('#')]) < 10
        
        return state
    
    def syntax_analysis_node(self, state: ReviewState) -> ReviewState:
        """Run syntax & logic analysis first"""
        agent = SyntaxLogicAgent(self.config)
        result = agent.review(state["code"])
        
        findings = self._extract_findings(result["feedback"], "Syntax & Logic")
        state["findings"].extend(findings)
        
        state["issues_by_agent"]["Syntax & Logic"] = len(findings)
        for finding in findings:
            if finding["severity"] == "critical":
                state["has_syntax_errors"] = True
                state["critical_issues"] += 1
            elif finding["severity"] == "warning":
                state["warnings"] += 1
            else:
                state["suggestions"] += 1
        
        state["total_issues"] += len(findings)
        state["agent_summaries"]["Syntax & Logic"] = extract_key_finding(result["feedback"])
        
        return state
    
    def security_performance_parallel_node(self, state: ReviewState) -> ReviewState:
        """Run Security and Performance agents in parallel"""
        with ThreadPoolExecutor(max_workers=2) as executor:
            security_future = executor.submit(self._run_security_agent, state)
            performance_future = executor.submit(self._run_performance_agent, state)
            
            security_findings = security_future.result()
            performance_findings = performance_future.result()
            
            state["findings"].extend(security_findings)
            state["findings"].extend(performance_findings)
            
            for findings, agent_name in [(security_findings, "Security"), (performance_findings, "Performance")]:
                state["issues_by_agent"][agent_name] = len(findings)
                state["total_issues"] += len(findings)
                
                for finding in findings:
                    if finding["severity"] == "critical":
                        state["critical_issues"] += 1
                        if agent_name == "Security":
                            state["has_security_issues"] = True
                    elif finding["severity"] == "warning":
                        state["warnings"] += 1
                    else:
                        state["suggestions"] += 1
        
        return state
    
    def architecture_testing_parallel_node(self, state: ReviewState) -> ReviewState:
        """Run Architecture and Testing agents in parallel"""
        if state["has_syntax_errors"]:
            state["needs_performance_review"] = False
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            architecture_future = executor.submit(self._run_architecture_agent, state)
            testing_future = executor.submit(self._run_testing_agent, state)
            
            architecture_findings = architecture_future.result()
            testing_findings = testing_future.result()
            
            state["findings"].extend(architecture_findings)
            state["findings"].extend(testing_findings)
            
            for findings, agent_name in [(architecture_findings, "Architecture"), (testing_findings, "Testing")]:
                state["issues_by_agent"][agent_name] = len(findings)
                state["total_issues"] += len(findings)
                
                for finding in findings:
                    if finding["severity"] == "critical":
                        state["critical_issues"] += 1
                    elif finding["severity"] == "warning":
                        state["warnings"] += 1
                    else:
                        state["suggestions"] += 1
        
        return state
    
    def documentation_analysis_node(self, state: ReviewState) -> ReviewState:
        """Run documentation analysis if needed"""
        agent = DocumentationAgent(self.config)
        result = agent.review(state["code"])
        
        findings = self._extract_findings(result["feedback"], "Documentation")
        state["findings"].extend(findings)
        
        state["issues_by_agent"]["Documentation"] = len(findings)
        state["total_issues"] += len(findings)
        
        for finding in findings:
            if finding["severity"] == "critical":
                state["critical_issues"] += 1
            elif finding["severity"] == "warning":
                state["warnings"] += 1
            else:
                state["suggestions"] += 1
        
        state["agent_summaries"]["Documentation"] = extract_key_finding(result["feedback"])
        
        return state
    
    def generate_report_node(self, state: ReviewState) -> ReviewState:
        """Generate final reports"""
        terminal_summary = self._generate_terminal_summary(state)
        state["terminal_summary"] = terminal_summary
        
        detailed_report = self._generate_detailed_report(state)
        state["final_report"] = detailed_report
        
        return state
    
    def _run_security_agent(self, state: ReviewState) -> list:
        """Run security agent with context"""
        agent = SecurityAgent(self.config)
        
        context = ""
        if state["has_syntax_errors"]:
            syntax_issues = [f for f in state["findings"] if f["agent"] == "Syntax & Logic"]
            context = f"\nNote: {len(syntax_issues)} syntax/logic errors were found. Focus on security issues only.\n"
        
        result = agent.review(state["code"] + context)
        findings = self._extract_findings(result["feedback"], "Security")
        state["agent_summaries"]["Security"] = extract_key_finding(result["feedback"])
        
        return findings
    
    def _run_performance_agent(self, state: ReviewState) -> list:
        """Run performance agent"""
        agent = PerformanceAgent(self.config)
        result = agent.review(state["code"])
        findings = self._extract_findings(result["feedback"], "Performance")
        state["agent_summaries"]["Performance"] = extract_key_finding(result["feedback"])
        return findings
    
    def _run_architecture_agent(self, state: ReviewState) -> list:
        """Run architecture agent with security context"""
        agent = ArchitectureAgent(self.config)
        
        context = ""
        if state["has_security_issues"]:
            context = "\nNote: Security vulnerabilities were found. Consider architectural changes that improve security.\n"
        
        result = agent.review(state["code"] + context)
        findings = self._extract_findings(result["feedback"], "Architecture")
        state["agent_summaries"]["Architecture"] = extract_key_finding(result["feedback"])
        return findings
    
    def _run_testing_agent(self, state: ReviewState) -> list:
        """Run testing agent with all previous findings context"""
        agent = TestingAgent(self.config)
        
        critical_areas = []
        for finding in state["findings"]:
            if finding["severity"] == "critical":
                critical_areas.append(f"Line {finding['line']}: {finding['issue']}")
        
        context = ""
        if critical_areas:
            context = "\nCritical issues found at:\n" + "\n".join(critical_areas[:3]) + "\nPrioritize tests for these areas.\n"
        
        result = agent.review(state["code"] + context)
        findings = self._extract_findings(result["feedback"], "Testing")
        state["agent_summaries"]["Testing"] = extract_key_finding(result["feedback"])
        return findings
    
    def _extract_findings(self, feedback: str, agent_name: str) -> list:
        """Extract structured findings from agent feedback"""
        findings = []
        lines = feedback.split('\n')
        
        current_finding = None
        for line in lines:
            line = line.strip()
            
            if line and (line[0].isdigit() or line.startswith(('•', '-', '*'))):
                if current_finding:
                    findings.append(current_finding)
                
                line_num = 0
                if "Line" in line and ":" in line:
                    try:
                        line_num = int(line.split("Line")[1].split(":")[0].strip().split()[0].strip(')'))
                    except:
                        pass
                
                severity = "suggestion"
                if any(word in line.lower() for word in ["critical", "vulnerability", "injection", "leak"]):
                    severity = "critical"
                elif any(word in line.lower() for word in ["warning", "issue", "problem", "inefficient"]):
                    severity = "warning"
                
                current_finding = AgentFinding(
                    agent=agent_name,
                    line=line_num,
                    issue=line,
                    severity=severity,
                    fix=""
                )
            elif current_finding and line.startswith(("Fix:", "- Fix:", "Solution:")):
                current_finding["fix"] = line
        
        if current_finding:
            findings.append(current_finding)
        
        if not findings and feedback.strip() and "no" not in feedback.lower() and "adequate" not in feedback.lower():
            findings.append(AgentFinding(
                agent=agent_name,
                line=0,
                issue=feedback.split('\n')[0][:100],
                severity="suggestion",
                fix=""
            ))
        
        return findings
    
    def _generate_terminal_summary(self, state: ReviewState) -> str:
        """Generate terminal summary"""
        summary = []
        summary.append("\n" + "=" * 60)
        summary.append("📊 REVIEW SUMMARY")
        summary.append("=" * 60)
        summary.append(f"\n📈 Total Issues Found: {state['total_issues']}")
        
        summary.append("\n🔍 Issues by Type:")
        icons = {
            "Syntax & Logic": "🐛",
            "Security": "🔒",
            "Performance": "⚡",
            "Architecture": "🏗️",
            "Testing": "🧪",
            "Documentation": "📝"
        }
        
        for agent, count in state["issues_by_agent"].items():
            if count > 0:
                icon = icons.get(agent, "•")
                summary.append(f"   {icon} {agent}: {count} issues")
        
        summary.append("\n⚠️  Severity Breakdown:")
        summary.append(f"   • Critical: {state['critical_issues']} 🔴")
        summary.append(f"   • Warnings: {state['warnings']} 🟡")
        summary.append(f"   • Suggestions: {state['suggestions']} 🟢")
        
        summary.append("\n💡 Key Findings:")
        for agent, finding in state["agent_summaries"].items():
            summary.append(f"   • {agent} Agent: {finding}")
        
        summary.append("\n" + "=" * 60)
        summary.append("✅ Review complete! Check the detailed report for full analysis.")
        summary.append("=" * 60)
        
        return "\n".join(summary)
    
    def _generate_detailed_report(self, state: ReviewState) -> str:
        """Generate detailed report"""
        report = []
        report.append("=" * 80)
        report.append(f"CODE REVIEW REPORT - {state['filename']}")
        report.append("=" * 80)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Lines: {len(state['code_lines'])} | Model: Claude 3.5 Haiku")
        report.append("=" * 80)
        
        if state["total_issues"] > 0:
            report.append(f"\nSUMMARY: {state['total_issues']} issues found")
            report.append("-" * 40)
            
            issue_parts = []
            for agent, count in state["issues_by_agent"].items():
                if count > 0:
                    issue_parts.append(f"{agent}: {count}")
            report.append(" | ".join(issue_parts))
            
            severity_parts = []
            if state["critical_issues"] > 0:
                severity_parts.append(f"Critical: {state['critical_issues']}")
            if state["warnings"] > 0:
                severity_parts.append(f"Warnings: {state['warnings']}")
            if state["suggestions"] > 0:
                severity_parts.append(f"Suggestions: {state['suggestions']}")
            report.append(" | ".join(severity_parts))
            
            report.append("\n" + "=" * 80)
            report.append("\nDETAILED FINDINGS:")
            report.append("=" * 80)
            
            by_agent = {}
            for finding in state["findings"]:
                agent = finding["agent"]
                if agent not in by_agent:
                    by_agent[agent] = []
                by_agent[agent].append(finding)
            
            for agent, findings in by_agent.items():
                if findings:
                    report.append(f"\n[{agent.upper()} AGENT]")
                    report.append("-" * 80)
                    
                    for i, finding in enumerate(findings, 1):
                        issue_text = finding["issue"]
                        if finding["line"] > 0:
                            issue_text = f"Line {finding['line']}: {issue_text}"
                        report.append(f"{i}. {issue_text}")
                        if finding["fix"]:
                            report.append(f"   {finding['fix']}")
                        report.append("")
        
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    async def review_code_async(self, code: str, filename: str = "code.py") -> ReviewState:
        """Run the review asynchronously"""
        initial_state = ReviewState(
            code=code,
            filename=filename,
            code_lines=[],
            findings=[],
            agent_summaries={},
            total_issues=0,
            critical_issues=0,
            warnings=0,
            suggestions=0,
            issues_by_agent={},
            has_syntax_errors=False,
            has_security_issues=False,
            needs_performance_review=True,
            skip_documentation=False,
            final_report=None,
            terminal_summary=None
        )
        
        result = await self.workflow.ainvoke(initial_state)
        return result
    
    def review_code(self, code: str, filename: str = "code.py") -> ReviewState:
        """Run the review synchronously"""
        return asyncio.run(self.review_code_async(code, filename))