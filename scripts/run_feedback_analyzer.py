import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.feedback_analyzer import FeedbackAnalyzer
from src.utils import save_results

if __name__ == "__main__":
    analyzer = FeedbackAnalyzer()
    results = analyzer.analyze_feedback("data/feedback/feedback.csv")
    
    # Save to CSV
    save_results(results, "results/sentiment_analysis.csv")
    
    # Print results
    print("\nSentiment Analysis Results:")
    for i, res in enumerate(results[:10], 1):
        risk_color = "\033[91m" if res['risk'] == "high" else "\033[93m" if res['risk'] == "medium" else "\033[92m"
        print(f"{i}. {res['text'][:100]}...")
        print(f"   Sentiment: {res['label']} (Confidence: {res['score']:.2f})")
        print(f"   Attrition Risk: {risk_color}{res['risk']}\033[0m\n")