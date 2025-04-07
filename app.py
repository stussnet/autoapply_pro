import streamlit as st
import pandas as pd
from scrapers.arbeitnow import scrape_arbeitnow
from gpt_writer import generate_cover_letter, save_letter_as_pdf
from job_tracker import load_job_tracker, save_job_tracker, update_tracker, STATUS_OPTIONS
from resume_matcher import score_resume_against_job
from email_writer import generate_outreach_email

st.set_page_config(page_title="AutoApply Pro", layout="wide")
st.title("AutoApply Pro – Remote Job AI Assistant")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Job Search + GPT Letters",
    "📊 Job Tracker",
    "🧠 Resume Matcher",
    "✉️ Email Generator"
])

# ---- Tab 1: Job Search + GPT Cover Letters ----
with tab1:
    keyword = st.text_input("Enter job keyword (e.g. python, react, ai)", "python")
    model = st.selectbox("Choose AI model (Ollama):", ["llama2", "mistral", "codellama", "gemma"])

    if "job_results" not in st.session_state:
        st.session_state.job_results = []

    if "cover_letters" not in st.session_state:
        st.session_state.cover_letters = {}

    if st.button("Search Jobs"):
        with st.spinner("Searching..."):
            jobs = scrape_arbeitnow(keyword)
            st.session_state.job_results = jobs

    if st.session_state.job_results:
        jobs = st.session_state.job_results
        st.success(f"Found {len(jobs)} jobs!")

        for i, job in enumerate(jobs):
            st.markdown(f"### [{job['title']} at {job['company']}]({job['link']})")

            if st.button(f"✍️ Generate Cover Letter #{i+1}", key=f"gen_btn_{i}"):
                letter = generate_cover_letter(job['title'], job['company'], model)
                st.session_state.cover_letters[i] = letter

            if i in st.session_state.cover_letters:
                letter = st.session_state.cover_letters[i]
                edited = st.text_area("✉️ Edit your cover letter below:", letter, height=300, key=f"text_{i}")

                if st.download_button(
                    label="📄 Download as PDF",
                    data=open(save_letter_as_pdf(edited, f"cover_letter_{i+1}.pdf"), "rb").read(),
                    file_name=f"cover_letter_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{i}"
                ):
                    st.success("✅ PDF downloaded!")

        df = pd.DataFrame(jobs)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Jobs as CSV",
            data=csv,
            file_name=f"{keyword}_arbeitnow_jobs.csv",
            mime="text/csv"
        )

# ---- Tab 2: Job Tracker ----
with tab2:
    st.subheader("Your Tracked Applications")
    tracker_df = load_job_tracker()

    if not tracker_df.empty:
        for i, row in tracker_df.iterrows():
            with st.expander(f"{row['title']} at {row['company']}"):
                new_status = st.selectbox("Status", STATUS_OPTIONS, index=STATUS_OPTIONS.index(row["status"]), key=f"status_{i}")
                new_notes = st.text_area("Notes", value=row["notes"], height=100, key=f"note_{i}")
                if st.button("💾 Save", key=f"save_{i}"):
                    tracker_df = update_tracker(tracker_df, i, new_status, new_notes)
                    st.success("Saved!")

        st.download_button(
            "📥 Download Tracker CSV",
            data=tracker_df.to_csv(index=False).encode("utf-8"),
            file_name="job_tracker.csv",
            mime="text/csv"
        )
    else:
        st.info("No tracked jobs yet. Cover letters you generate will appear here once saved.")

# ---- Tab 3: Resume Matcher ----
with tab3:
    st.subheader("🧠 Resume Matcher")
    uploaded = st.file_uploader("Upload your resume (TXT format recommended):", type=["txt"])
    model = st.selectbox("Select GPT model for matching", ["llama2", "mistral", "codellama", "gemma"], key="matcher_model")

    if uploaded:
        resume_text = uploaded.read().decode("utf-8")
        job_title = st.text_input("Job title to match against:", "")
        tags_input = st.text_input("Enter job tags/keywords (comma-separated):", "")

        if st.button("🧠 Score My Resume"):
            tags = [tag.strip() for tag in tags_input.split(",")]
            with st.spinner("Scoring..."):
                result = score_resume_against_job(resume_text, job_title, tags, model)
            st.markdown("### 🔍 Match Result")
            st.text_area("AI Feedback", result, height=300)
    else:
        st.info("Please upload a .txt version of your resume to begin.")

# ---- Tab 4: Email Generator ----
with tab4:
    st.subheader("✉️ Outreach Email Generator")
    model = st.selectbox("Select AI model", ["llama2", "mistral", "codellama", "gemma"], key="email_model")
    job_title = st.text_input("Job Title", "")
    company = st.text_input("Company Name", "")
    contact = st.text_input("Hiring Contact Name (optional)", "")

    if st.button("📧 Generate Email"):
        with st.spinner("Writing..."):
            email = generate_outreach_email(job_title, company, contact, model)
            st.text_area("Generated Email", email, height=300)
