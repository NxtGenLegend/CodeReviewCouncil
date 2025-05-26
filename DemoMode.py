import json
from datetime import datetime
import time

DEMO_RESPONSES = {
    "Security Agent": """Found 3 critical security vulnerabilities:

1. **SQL Injection (Line 2)**: The code uses string formatting to build SQL queries
   - Risk: Attackers can execute arbitrary SQL commands
   - Fix: Use parameterized queries: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))`

2. **Hardcoded Credentials (Line 18)**: Password 'admin123' is stored in plain text
   - Risk: Anyone with code access can see credentials
   - Fix: Use environment variables and password hashing (bcrypt)

3. **No Input Validation (Line 1)**: User input is used directly without sanitization
   - Risk: Various injection attacks possible
   - Fix: Validate and sanitize all user inputs before use""",
    
    "Performance Agent": """Identified 2 major performance issues:

1. **O(n²) Algorithm (Lines 9-12)**: Nested loops for duplicate removal
   - Impact: Quadratic time complexity, slow for large datasets
   - Fix: Use a set for O(n) deduplication: `unique_data = list({tuple(d.items()) for d in user_data})`

2. **No Database Indexing**: Queries without proper indexes
   - Impact: Full table scans on every query
   - Fix: Add index on frequently queried columns: `CREATE INDEX idx_user_id ON users(id)`""",
    
    "Architecture Agent": """Found 3 architectural concerns:

1. **Tight Coupling**: Data access logic mixed with business logic
   - Issue: Hard to test and maintain
   - Fix: Implement Repository pattern to separate concerns

2. **No Dependency Injection**: Direct instantiation of dependencies
   - Issue: Makes unit testing difficult
   - Fix: Pass dependencies through constructor

3. **Missing Error Handling**: No try-except blocks for database operations
   - Issue: Application crashes on database errors
   - Fix: Add proper error handling and logging""",
    
    "Testing Agent": """Generated test cases and identified gaps:

1. **Missing Unit Tests**: No tests for any functions
   - Add tests for: process_user_data(), UserManager.authenticate()
   
2. **Edge Cases Not Covered**:
   - Empty input handling
   - SQL injection attempts
   - Invalid user credentials
   - Concurrent access scenarios

3. **Suggested Test Case**:
   ```python
   def test_sql_injection_prevention():
       malicious_input = "1; DROP TABLE users;"
       result = process_user_data(malicious_input, mock_db)
       assert "DROP TABLE" not in mock_db.last_query
   ```""",
    
    "Documentation Agent": """Documentation improvements needed:

1. **Missing Function Docstrings**: No documentation for any functions
   - Add docstrings explaining purpose, parameters, and return values

2. **No API Documentation**: UserManager class lacks usage examples
   - Add class-level documentation with example usage

3. **Suggested Documentation**:
   ```python
   def process_user_data(user_input: str, db_connection: Connection) -> List[Dict]:
       '''Process user data from database based on input.
       
       Args:
           user_input: User ID to query
           db_connection: Active database connection
           
       Returns:
           List of user dictionaries without duplicates
       '''
   ```"""
}

def save_demo_report(results):
    """Save demo report to text file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"demo_review_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CODE REVIEW REPORT (DEMO)\n")
        f.write("=" * 80 + "\n\n")
        f.write("File: example.py\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("Mode: Demo (Pre-recorded responses)\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        for review in results["reviews"]:
            f.write(f"[{review['agent'].upper()}]\n")
            f.write("-" * 80 + "\n")
            f.write(review['feedback'] + "\n\n")
            f.write("=" * 80 + "\n\n")
    
    return filename

def run_demo():
    print("\n" + "=" * 60)
    print("🎭 CODE REVIEW COUNCIL - DEMO MODE")
    print("=" * 60)
    print("\n📌 This demonstrates the system without using API credits.")
    print("   Real reviews would be specific to your actual code.\n")
    
    input("Press Enter to start the demo...")
    
    print("\n📂 Reading example.py...")
    time.sleep(0.5)
    print("📏 File size: 33 lines")
    
    print("\n🔍 Starting code review for: example.py")
    print("=" * 60)
    
    results = {
        "filename": "example.py",
        "timestamp": datetime.now().isoformat(),
        "code_length": 33,
        "reviews": [],
        "summary": {
            "total_issues": 5,
            "critical_issues": 2,
            "warnings": 2,
            "suggestions": 1
        }
    }
    
    # Simulate progress bar
    agents = list(DEMO_RESPONSES.keys())
    total = len(agents)
    
    for idx, (agent_name, response) in enumerate(DEMO_RESPONSES.items(), 1):
        progress = "█" * (idx * 10 // total) + "░" * ((total - idx) * 10 // total)
        print(f"\r[{progress}] Running {agent_name}... ({idx}/{total})", end="", flush=True)
        time.sleep(0.8)
        
        results["reviews"].append({
            "agent": agent_name,
            "role": f"{agent_name.lower()} specialist",
            "feedback": response,
            "timestamp": datetime.now().isoformat()
        })
    
    print(f"\r[{'█' * 10}] Review complete! ({total}/{total})")
    print("=" * 60)
    
    # Print summary only
    print("\n" + "=" * 60)
    print("📊 REVIEW SUMMARY")
    print("=" * 60)
    
    print("\n📈 Issues Found:")
    print(f"   • Total Issues: {results['summary']['total_issues']}")
    print(f"   • Critical: {results['summary']['critical_issues']} 🔴")
    print(f"   • Warnings: {results['summary']['warnings']} 🟡")
    print(f"   • Suggestions: {results['summary']['suggestions']} 🟢")
    
    print("\n🔍 Key Findings by Agent:")
    for agent in agents:
        print(f"   • {agent}: {DEMO_RESPONSES[agent].split(':')[0]}...")
    
    print("\n" + "=" * 60)
    print("✅ Review complete! Check the detailed report for full analysis.")
    print("=" * 60)
    
    # Save options
    print("\n💾 Save Options:")
    save_txt = input("Save detailed demo report as .txt? (y/n): ").strip().lower()
    
    if save_txt == 'y':
        filename = save_demo_report(results)
        print(f"\n📝 Demo report saved to: {filename}")
        print("✨ Open this file to see the full analysis!")
    
    save_json = input("\nAlso save as JSON? (y/n): ").strip().lower()
    if save_json == 'y':
        with open("DemoResults.json", 'w') as f:
            json.dump(results, f, indent=2)
        print("📄 JSON saved to: DemoResults.json")
    
    print("\n🎉 Demo complete!")
    print("💡 To review your own code with real AI analysis:")
    print("   Run: python main.py")

if __name__ == "__main__":
    run_demo()