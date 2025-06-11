from transformers import pipeline
from typing import List, Dict, Optional, Union
import pandas as pd
import re

class FeedbackAnalyzer:
    def __init__(self):
        self.sentiment_pipeline = pipeline(
            "text-classification",
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )
        # Changed to class-level constant for safety
        self.HR_KEYWORDS = {
            'salary': -0.3,
            'promotion': -0.2,
            'workload': -0.25,
            'manager': -0.15
        }
        
    def analyze_feedback(self, csv_path: str) -> List[Dict]:
        """Main analysis method - interface remains unchanged"""
        df = pd.read_csv(csv_path)
        return self._process_dataframe(df)
    
    def analyze_texts(self, texts: List[str]) -> List[Dict]:
        """New method for API compatibility"""
        df = pd.DataFrame({'feedback': texts})
        return self._process_dataframe(df)
    
    def _process_dataframe(self, df: pd.DataFrame) -> List[Dict]:
        """Shared processing logic"""
        results = []
        for _, row in df.iterrows():
            text = str(row['feedback'])
            result = self._analyze_single(text)
            if result:
                results.append(result)
        return sorted(results, key=lambda x: x['risk'] == 'high', reverse=True)
    
    def _analyze_single(self, text: str) -> Optional[Dict]:
        """Unified single-text analysis"""
        custom = self._apply_hr_rules(text)
        if custom:
            return custom
            
        sentiment = self.sentiment_pipeline(text)[0]
        return {
            "text": text,
            "label": sentiment['label'],
            "score": float(sentiment['score']),  # Ensure serializable
            "risk": self._calculate_risk(sentiment, text),
            # Add keywords for API compatibility
            "keywords": [k for k in self.HR_KEYWORDS if k in text.lower()]
        }
    
    def _apply_hr_rules(self, text: str) -> Optional[Dict]:
        text_lower = text.lower()
        if any(w in text_lower for w in ['salary', 'pay']) and \
           any(w in text_lower for w in ['low', 'below', 'underpaid']):
            return {
                "text": text,
                "label": "NEGATIVE",
                "score": 0.99,
                "risk": "high",
                "keywords": ["salary"]
            }
        return None
    
    def _calculate_risk(self, sentiment: Dict, text: str) -> str:
        text_lower = text.lower()
        if any(phrase in text_lower for phrase in 
               ["quit", "leaving", "resigning"]):
            return "high"
            
        if sentiment['label'] == "NEGATIVE":
            if sentiment['score'] > 0.9:
                return "high"
            if any(kw in text_lower for kw in self.HR_KEYWORDS):
                return "high"
                
        return "medium" if sentiment['score'] > 0.7 else "low"