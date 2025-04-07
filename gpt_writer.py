import requests
from config import USER_PROFILE
from fpdf import FPDF
import os

OLLAMA_URL = "http://localhost:11434/api/chat"

def generate_cover_letter(job_title, company_name, model_name="llama2"):
    prompt = f"""
Write a professional, friendly cover letter for:
Job Title: {job_title}
Company: {company_name}

Candidate Profile:
{USER_PROFILE}

The letter should be confident and concise (around 3 paragraphs).
"""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are a professional resume and cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        })

        result = response.json()
        return result["message"]["content"].strip()

    except Exception as e:
        return f"❌ Error from local model ({model_name}): {e}"


def save_letter_as_pdf(text, filename="cover_letter.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    output_path = os.path.join("generated_letters", filename)
    os.makedirs("generated_letters", exist_ok=True)
    pdf.output(output_path)
    return output_path
