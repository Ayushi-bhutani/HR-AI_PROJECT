from fastapi import FastAPI, UploadFile, File, HTTPException

# from src.resume_matcher import ResumeMatcher
# from src.utils import clean_text, extract_text_from_pdf, extract_text_from_docx
from typing import List
import os
import uvicorn
from src.resume_matcher import ResumeMatcher
from src.utils import clean_text, extract_text_from_pdf, extract_text_from_docx
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
app = FastAPI(title="HR-Tech Resume Screener",
              description="AI-powered resume screening API")

jd_path = "data/job_descriptions/software_engineer_jd.txt"
matcher = ResumeMatcher(jd_path)

SUPPORTED_TYPES = {'.pdf', '.docx'}

async def process_file(file: UploadFile):
    """Helper function to process uploaded files"""
    if not any(file.filename.lower().endswith(ext) for ext in SUPPORTED_TYPES):
        raise HTTPException(400, "Unsupported file type")
    
    file_path = f"temp_{file.filename}"
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_docx(file_path)
            
        return clean_text(text)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/screen-resume", 
          response_model=dict,
          responses={
              200: {"description": "Successful analysis"},
              400: {"description": "Invalid file type"},
              500: {"description": "Processing error"}
          })
async def screen_resume(file: UploadFile = File(...)):
    """Analyze a single resume"""
    try:
        text = await process_file(file)
        score = matcher._calculate_match_score(text)
        return {
            "filename": file.filename,
            "score": score,
            "skills": matcher._extract_skills(text),
            "missing_skills": list(set(matcher.required_skills) - set(matcher._extract_skills(text))),
            "snippet": text[:200] + "..."
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/bulk-screen", 
          response_model=List[dict],
          response_description="List of analyzed resumes")
async def bulk_screen(files: List[UploadFile] = File(...)):
    """Analyze multiple resumes at once"""
    return [await screen_resume(file) for file in files]
# In both api_resume.py and api_sentiment.py
@app.get("/")
async def root():
    return {"message": "HR-Tech AI API", "docs": "/docs"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)