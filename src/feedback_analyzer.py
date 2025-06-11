from transformers import pipeline
from typing import List, Dict
import pandas as pd
import re

class FeedbackAnalyzer:
    def __init__(self):
        self.sentiment_pipeline = pipeline(
            "text-classification",
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )
        self.hr_keywords = {
            'salary': -0.3,
            'promotion': -0.2,
            'workload': -0.25,
            'manager': -0.15
        }
        
    def analyze_feedback(self, csv_path: str) -> List[Dict]:
        df = pd.read_csv(csv_path)
        results = []
        
        for _, row in df.iterrows():
            text = str(row['feedback'])
            
            # Apply custom HR rules first
            custom_score = self._apply_hr_rules(text)
            if custom_score:
                results.append(custom_score)
                continue
                
            # Default sentiment analysis
            sentiment = self.sentiment_pipeline(text)[0]
            
            results.append({
                "text": text,
                "label": sentiment['label'],
                "score": sentiment['score'],
                "risk": self._calculate_risk(sentiment, text)
            })
            
        return sorted(results, key=lambda x: x['risk'] == 'high', reverse=True)
    
    def _apply_hr_rules(self, text: str) -> Dict:
        """Apply domain-specific rules"""
        text_lower = text.lower()
        
        # Salary complaints
        if any(w in text_lower for w in ['salary', 'pay']) and \
           any(w in text_lower for w in ['low', 'below', 'underpaid']):
            return {
                "text": text,
                "label": "NEGATIVE",
                "score": 0.99,
                "risk": "high"
            }
            
        return None
    
    def _calculate_risk(self, sentiment: Dict, text: str) -> str:
        text_lower = text.lower()
        # Immediate high-risk phrases
        if any(phrase in text_lower for phrase in 
               ["quit", "leaving", "resigning", "looking for new opportunities"]):
            return "high"
        # Sentiment-based risk
        if sentiment['label'] == "NEGATIVE":
            if sentiment['score'] > 0.9:
                return "high"
            elif "manager" in text_lower or "salary" in text_lower:
                return "high"
            return "medium" if sentiment['score'] > 0.7 else "low"