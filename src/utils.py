import re
import os
from pdfminer.high_level import extract_text
from docx import Document
from typing import List, Dict, Union

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF resumes"""
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error reading {pdf_path}: {str(e)}")
        return ""

def extract_text_from_docx(docx_path: str) -> str:
    """Extract text from DOCX resumes"""
    try:
        doc = Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading {docx_path}: {str(e)}")
        return ""

def clean_text(text: str) -> str:
    """Enhanced text cleaning"""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special chars but preserve @ for emails and + for skills
    text = re.sub(r'[^\w\s@\+-]', ' ', text)
    return text.lower()

def load_job_description(jd_path: str) -> str:
    """Load and clean job description"""
    with open(jd_path, 'r', encoding='utf-8') as f:
        return clean_text(f.read())

def save_results(results: List[Dict], output_path: str):
    """Save analysis results to CSV"""
    import pandas as pd
    pd.DataFrame(results).to_csv(output_path, index=False)