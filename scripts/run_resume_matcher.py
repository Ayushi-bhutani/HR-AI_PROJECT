from src.resume_matcher import load_resumes, load_job_description, match_resume_with_jd

resumes_path = "data/resumes"
jd_path = "data/job_descriptions/software_engineer_jd.txt"

resumes = load_resumes(resumes_path)
jd = load_job_description(jd_path)

for name, resume in resumes.items():
    print(f"\n--- {name} ---")
    result = match_resume_with_jd(resume, jd)
    print(result)
