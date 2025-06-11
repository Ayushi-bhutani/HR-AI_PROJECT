import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .utils import extract_text_from_pdf, extract_text_from_docx, clean_text, load_job_description
from typing import List, Dict
import re

class ResumeMatcher:
    def __init__(self, jd_path: str):
        self.jd_text = load_job_description(jd_path)
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        self.required_skills = {
    'python': 0.1,
    'java': 0.1,
    'c\+\+': 0.1,  # Escape special chars
    'machine learning': 0.15,
    'aws': 0.08,
    'azure': 0.08
}
        
    def process_resumes(self, resume_dir: str) -> List[Dict]:
        results = []
        for filename in os.listdir(resume_dir):
            filepath = os.path.join(resume_dir, filename)
            
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(filepath)
            elif filename.endswith(".docx"):
                text = extract_text_from_docx(filepath)
            else:
                continue
                
            cleaned_text = clean_text(text)
            score = self._calculate_match_score(cleaned_text)
            skills_found = self._extract_skills(cleaned_text)
            
            results.append({
                "filename": filename,
                "score": round(score, 2),
                "skills": skills_found,
                "text": cleaned_text[:500] + "..."
            })
        
        return sorted(
            [r for r in results if r['score'] >= 0.3],  # Filter low scores
            key=lambda x: x['score'],
            reverse=True
        )
    
    def _calculate_match_score(self, resume_text: str) -> float:
        tfidf_matrix = self.vectorizer.fit_transform([self.jd_text, resume_text])
        base_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Normalize skill bonus (max 0.3)
        skill_bonus = min(
            sum(0.05 for skill in self.required_skills 
                if re.search(rf'\b{skill}\b', resume_text, re.I)),
                0.3
                )
        return round(base_score * 0.7 + skill_bonus, 2)  # Weighted average
    
    
    def _extract_skills(self, text: str) -> List[str]:
        return [
            skill for skill in self.required_skills
            if re.search(rf'\b{skill}\b', text, re.I)
        ]