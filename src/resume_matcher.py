import os
import openai

openai.api_key = "sk-..."  # replace with your key

def load_resumes(resumes_path):
    resumes = {}
    for file in os.listdir(resumes_path):
        with open(os.path.join(resumes_path, file), 'r') as f:
            resumes[file] = f.read()
    return resumes

def load_job_description(jd_path):
    with open(jd_path, 'r') as f:
        return f.read()

def match_resume_with_jd(resume_text, jd_text):
    prompt = f"""
You are an AI assistant helping HR. Match the given resume with the job description.

Job Description:
{jd_text}

Resume:
{resume_text}

Return format:
- Match Percentage: XX%
- Missing: ...
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']
