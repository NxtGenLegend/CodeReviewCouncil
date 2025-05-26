import os
import json
from typing import Dict, Any

def count_issues_in_feedback(feedback: str) -> int:
    """Count number of distinct issues mentioned in feedback"""
    if not feedback:
        return 0
    
    lines = feedback.split('\n')
    issue_count = 0
    
    # Look for numbered items (1., 2., etc.) or bullet points
    for line in lines:
        stripped = line.strip()
        if stripped:
            # Check for numbered lists (1., 2., etc.)
            if len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in '.):':
                issue_count += 1
            # Check for bullet points
            elif stripped.startswith(('-', '•', '*', '►')):
                issue_count += 1
            # Check for specific patterns like "Issue:" or "Problem:"
            elif any(pattern in stripped.lower() for pattern in ['issue:', 'problem:', 'vulnerability:', 'gap:', 'missing:']):
                issue_count += 1
    
    # If no specific patterns found but feedback exists, count as at least 1
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
    
    # Keywords that indicate different severity levels
    critical_keywords = ['critical', 'severe', 'vulnerability', 'injection', 'hardcoded', 'plain text']
    warning_keywords = ['warning', 'issue', 'problem', 'inefficient', 'missing']
    suggestion_keywords = ['suggestion', 'recommend', 'consider', 'improve', 'enhancement']
    
    severity = {
        'critical': 0,
        'warning': 0,
        'suggestion': 0
    }
    
    # Count occurrences
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
    
    # Default to suggestion if no keywords found
    if sum(severity.values()) == 0:
        severity['suggestion'] = 1
    
    return severity