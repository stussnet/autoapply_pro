import requests
from config import USER_PROFILE

OLLAMA_URL = "http://localhost:11434/api/chat"

def generate_outreach_email(job_title, company_name, contact_name=None, model="llama2"):
    prompt = f"""
Write a friendly and professional cold outreach email expressing interest in a job opportunity.
Job Title: {job_title}
Company: {company_name}
Contact Name: {contact_name or "Hiring Manager"}

Candidate Profile:
{USER_PROFILE}

The email should:
- Include a warm intro
- Express genuine interest in the role
- Mention relevant experience
- Include a call to action (e.g. connect, schedule time)
- Be concise and sound human

End with the sender's name as "Your Name".
"""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a professional career email writer."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        })

        result = response.json()
        return result["message"]["content"].strip()

    except Exception as e:
        return f"❌ Error generating email: {e}"
