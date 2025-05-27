import os
import json
from typing import Dict, Any

def extract_key_finding(feedback: str) -> str:
    """Extract the most important finding from feedback"""
    if not feedback:
        return "No issues found"
    
    lines = feedback.split('\n')
    
    for line in lines:
        stripped = line.strip()
        if stripped and len(stripped) > 10:
            # Skip generic introductions
            generic_starts = [
                "after a comprehensive",
                "here's a comprehensive", 
                "here are the",
                "comprehensive analysis",
                "following review",
                "based on analysis"
            ]
            
            if any(start in stripped.lower() for start in generic_starts):
                continue
                
            if any(word in stripped.lower() for word in ['found', 'identified', 'detected', 'issue', 'vulnerability', 'problem']):
                # Clean up and return
                finding = stripped
                if len(finding) > 80:
                    finding = finding[:77] + "..."
                return finding
            
            if len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in '.):':
                finding = stripped.split('.', 1)[1].strip() if '.' in stripped else stripped
                if len(finding) > 80:
                    finding = finding[:77] + "..."
                return finding
    
    for line in lines:
        stripped = line.strip()
        if stripped and len(stripped) > 10:
            generic_starts = ["after", "here's", "comprehensive", "following", "based on"]
            if not any(stripped.lower().startswith(start) for start in generic_starts):
                if len(stripped) > 80:
                    return stripped[:77] + "..."
                return stripped
    
    return "Multiple issues identified"

def count_issues_in_feedback(feedback: str) -> int:
    """Count number of distinct issues mentioned in feedback"""
    if not feedback:
        return 0
    
    lines = feedback.split('\n')
    issue_count = 0
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            if len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in '.):':
                issue_count += 1
            elif stripped.startswith(('-', '•', '*', '►')):
                issue_count += 1
            elif any(pattern in stripped.lower() for pattern in ['issue:', 'problem:', 'vulnerability:', 'gap:', 'missing:']):
                issue_count += 1
    
    return max(issue_count, 1) if feedback.strip() else 0

def ensure_api_key():
    """Check if API key is configured"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key and os.path.exists(".env"):
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("ANTHROPIC_API_KEY")
        except ImportError:
            pass
    
    if not api_key:
        print("\nError: No API key found!")
        print("Please run: python setup.py")
        return False
    
    return True

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load and return JSON file contents"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def save_json_file(data: Dict[str, Any], filepath: str):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def analyze_severity(feedback: str) -> Dict[str, int]:
    """Analyze feedback text for severity indicators"""
    feedback_lower = feedback.lower()
    
    critical_keywords = ['critical', 'severe', 'vulnerability', 'injection', 'hardcoded', 'plain text']
    warning_keywords = ['warning', 'issue', 'problem', 'inefficient', 'missing']
    suggestion_keywords = ['suggestion', 'recommend', 'consider', 'improve', 'enhancement']
    
    severity = {
        'critical': 0,
        'warning': 0,
        'suggestion': 0
    }
    
    for keyword in critical_keywords:
        if keyword in feedback_lower:
            severity['critical'] += 1
            break
    
    for keyword in warning_keywords:
        if keyword in feedback_lower and severity['critical'] == 0:
            severity['warning'] += 1
            break
    
    for keyword in suggestion_keywords:
        if keyword in feedback_lower and severity['critical'] == 0 and severity['warning'] == 0:
            severity['suggestion'] += 1
            break
    
    if sum(severity.values()) == 0:
        severity['suggestion'] = 1
    
    return severity