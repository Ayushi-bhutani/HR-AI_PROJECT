import sys
from pathlib import Path
import json

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.resume_matcher import ResumeMatcher
from src.utils import save_results

if __name__ == "__main__":
    # Paths relative to project root
    JD_PATH = "data/job_descriptions/software_engineer_jd.txt"
    RESUME_DIR = "data/resumes"
    OUTPUT_PATH = "results/resume_matches.csv"
    
    matcher = ResumeMatcher(JD_PATH)
    results = matcher.process_resumes(RESUME_DIR)
    
    # Save to CSV
    save_results(results, OUTPUT_PATH)
    
    # Print top results
    print("\nTop Matching Resumes:")
    for i, res in enumerate(results[:5], 1):
        print(f"{i}. {res['filename']} (Score: {res['score']})")
        print(f"   Skills: {', '.join(res['skills'][:5])}")
        print(f"   Snippet: {res['text'][:200]}...\n")
        # Add to print statement
        print(f"{i}. {res['filename']} (Score: {res['score']})")
        print(f"   Match: {'★' * int(res['score'] * 5)}")
        
    