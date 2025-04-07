# AutoApply Pro 🚀

AI-powered job application assistant for new grads and self-learners.

## ✨ Features

- 🔍 Remote job scraping (e.g. Arbeitnow)
- 🧠 GPT-powered cover letter generation
- 📄 PDF export
- 📊 Job tracker with status + notes
- 🧠 Resume matching (AI relevance scoring)
- ✉️ Outreach email generation
- ☁️ Deployed to Streamlit Cloud + `.exe` optional packaging

## 🖥️ Built With

- [Streamlit](https://streamlit.io)
- [Ollama](https://ollama.com) for local GPT (LLaMA2, Mistral, etc.)
- Python 3.10+
- fpdf, requests, pandas

## 🚀 Live Demo

[Try AutoApply Pro now](https://autoapply-pro.streamlit.app)

## 🛠️ Getting Started

```bash
git clone https://github.com/your-username/autoapply_pro.git
cd autoapply_pro
pip install -r requirements.txt
streamlit run app.py
```

Make sure you have [Ollama](https://ollama.com) installed and running:
```bash
ollama run llama2
```

## 🧪 Project Structure

```
autoapply_pro/
├── app.py
├── config.py
├── gpt_writer.py
├── email_writer.py
├── resume_matcher.py
├── job_tracker.py
├── scrapers/
│   └── arbeitnow.py
├── requirements.txt
├── runtime.txt
├── README.md
└── .gitignore
```

## 🧳 License

MIT – free to use, modify, and share.
