from fastapi import FastAPI, Query, HTTPException
from typing import List
import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.feedback_analyzer import FeedbackAnalyzer

app = FastAPI()
analyzer = FeedbackAnalyzer()

@app.post("/analyze-feedback")
async def analyze_feedback(text: str = Query(..., min_length=5)):
    """Analyze single feedback entry"""
    try:
        result = analyzer.analyze_texts([text])[0]
        return {
            "sentiment": result['label'],
            "confidence": result['score'],
            "risk": result['risk'],
            "keywords": result['keywords'],
            "text_snippet": text[:100] + "..." if len(text) > 100 else text
        }
    except Exception as e:
        raise HTTPException(500, f"Analysis error: {str(e)}")
# In both api_resume.py and api_sentiment.py
@app.get("/")
async def root():
    return {"message": "HR-Tech AI API", "docs": "/docs"}
@app.post("/bulk-analyze")
async def bulk_analyze(texts: List[str]):
    """Batch process feedback"""
    try:
        if not texts:
            raise HTTPException(400, "No texts provided")
            
        results = analyzer.analyze_texts(texts)
        return {
            "count": len(results),
            "high_risk_count": sum(1 for r in results if r['risk'] == 'high'),
            "results": results
        }
    except Exception as e:
        raise HTTPException(500, f"Bulk analysis error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)