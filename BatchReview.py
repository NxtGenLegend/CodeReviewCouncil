import os
import sys
import json
from datetime import datetime
from CodeReviewCouncil import CodeReviewCouncil

def review_directory(directory_path, file_extensions=['.py', '.js', '.java', '.cpp', '.c']):
    council = CodeReviewCouncil()
    all_results = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                print(f"\nReviewing: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    results = council.review_code(code, file_path)
                    all_results.append(results)
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    all_results.append({
                        "filename": file_path,
                        "error": str(e)
                    })
    
    summary_file = f"BatchReview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "review_date": datetime.now().isoformat(),
            "directory": directory_path,
            "total_files": len(all_results),
            "results": all_results
        }, f, indent=2)
    
    print(f"\n\nBatch review complete! Results saved to: {summary_file}")
    print(f"Total files reviewed: {len(all_results)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        directory = input("Enter directory path to review: ").strip()
    else:
        directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)
    
    review_directory(directory)