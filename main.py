import os
from CodeReviewCouncil import CodeReviewCouncil
from utils import ensure_api_key

def main():
    if not ensure_api_key():
        return
    
    council = CodeReviewCouncil()
    
    code_file = input("Enter the path to the code file to review: ").strip()
    
    if not os.path.exists(code_file):
        print(f"Error: File '{code_file}' not found")
        return
    
    print(f"\n📂 Reading {code_file}...")
    with open(code_file, 'r') as f:
        code = f.read()
    
    print(f"📏 File size: {len(code.splitlines())} lines")
    
    results = council.review_code(code, os.path.basename(code_file))
    
    council.print_summary(results)
    
    print("\n💾 Save Options:")
    save_txt = input("Save detailed report as .txt? (y/n): ").strip().lower()
    
    if save_txt == 'y':
        txt_file = council.save_readable_report(results)
        print(f"\n✨ Success! Review saved to: {txt_file}")
        print("   Contains:")
        print("   • Summary of issues found")
        print("   • Detailed findings by agent")
        print("   • Line-specific references")
        print("   • Recommended fixes")
    
    save_json = input("\nAlso save raw data as JSON? (y/n): ").strip().lower()
    if save_json == 'y':
        output_file = input("JSON filename (default: ReviewResults.json): ").strip()
        if not output_file:
            output_file = "ReviewResults.json"
        council.save_results(results, output_file)
    
    print("\n🎉 Done! Thanks for using Code Review Council.")

if __name__ == "__main__":
    main()