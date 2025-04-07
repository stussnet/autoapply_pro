import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

def score_resume_against_job(resume_text, job_title, job_tags, model="llama2"):
    prompt = f"""
You are a technical recruiter. Review the following resume and determine how well it matches the given job title and tags.

Job Title: {job_title}
Tags: {", ".join(job_tags)}

Resume:
{resume_text}

Give a score from 0 to 100 with a short explanation of relevance (skills, fit, keywords).
"""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI resume matcher."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        })
        result = response.json()
        return result["message"]["content"].strip()

    except Exception as e:
        return f"❌ Error from resume matcher: {e}"
