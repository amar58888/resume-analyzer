import streamlit as st
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer ULTIMATE", layout="centered")

# ---------------- TITLE ----------------
st.title("🔥 AI Resume Analyzer ULTIMATE")
st.markdown("### Resume + ATS + Job Matching System")

# ---------------- ROLE ----------------
role = st.selectbox(
    "🎯 Select your target role",
    ["Data Scientist", "Software Developer", "Data Analyst"]
)

# ---------------- JOB DESCRIPTION ----------------
job_desc = st.text_area("📄 Paste Job Description (Optional for ATS Matching)")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# ---------------- ROLE SKILLS ----------------
role_skills = {
    "Data Scientist": [
        "python", "machine learning", "deep learning", "nlp",
        "pandas", "numpy", "tensorflow", "data analysis"
    ],
    "Software Developer": [
        "python", "java", "c", "sql", "git",
        "data structures", "algorithms", "oop"
    ],
    "Data Analyst": [
        "excel", "sql", "tableau", "power bi",
        "data analysis", "statistics", "python"
    ]
}

# ---------------- PROJECT SUGGESTIONS ----------------
def suggest_projects(role):
    if role == "Data Scientist":
        return [
            "Movie Recommendation System",
            "Spam Email Classifier",
            "Stock Price Prediction",
            "Chatbot using NLP"
        ]
    elif role == "Software Developer":
        return [
            "Portfolio Website",
            "To-Do App with Login",
            "Chat Application",
            "E-commerce Website"
        ]
    else:
        return [
            "Sales Dashboard (Tableau)",
            "Excel Data Analysis Project",
            "Customer Segmentation",
            "Business Dashboard"
        ]

# ---------------- ATS MATCH ----------------
def calculate_ats_score(text, job_desc):
    if not job_desc:
        return None, []

    jd_words = job_desc.lower().split()
    resume_words = text.split()

    matched = list(set(jd_words) & set(resume_words))
    score = int((len(matched) / len(jd_words)) * 100)

    missing = list(set(jd_words) - set(resume_words))

    return score, missing[:10]

# ---------------- FEEDBACK ----------------
def generate_feedback(found, missing, score, role):
    feedback = ""

    feedback += "✅ Strengths:\n"
    for skill in found:
        feedback += f"- {skill}\n"

    feedback += "\n❌ Weaknesses:\n"
    for skill in missing:
        feedback += f"- Missing {skill}\n"

    feedback += "\n💡 Suggestions:\n"
    if score > 70:
        feedback += "- Ready for top roles\n"
    elif score > 40:
        feedback += "- Improve skills for better chances\n"
    else:
        feedback += "- Build projects and add skills\n"

    feedback += f"\n🎯 Focus for {role}: Learn missing skills."

    return feedback

# ---------------- MAIN ----------------
if uploaded_file is None:
    st.warning("⚠️ Upload your resume")

else:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text().lower()

    skills = role_skills[role]

    found = []
    missing = []

    for skill in skills:
        if skill in text:
            found.append(skill)
        else:
            missing.append(skill)

    # SCORE
    score = int((len(found) / len(skills)) * 100)

    st.success(f"📊 Resume Score: {score}%")
    st.progress(score)

    # ATS SCORE
    ats_score, ats_missing = calculate_ats_score(text, job_desc)

    if ats_score is not None:
        st.markdown("## 🤖 ATS Match Score")
        st.info(f"ATS Score: {ats_score}%")

        st.markdown("### ❌ Missing Keywords from JD")
        for word in ats_missing:
            st.markdown(f"📌 {word}")

    # RESULT MESSAGE
    if score > 70:
        st.success("🚀 Excellent Resume")
    elif score > 40:
        st.warning("⚡ Good but improve")
    else:
        st.error("❌ Needs improvement")

    # SKILLS
    st.markdown("## ✅ Skills Found")
    for skill in found:
        st.markdown(f"✔️ {skill}")

    st.markdown("## ❌ Missing Skills")
    for skill in missing:
        st.markdown(f"❌ {skill}")

    # FEEDBACK
    st.markdown("## 🤖 Smart Feedback")
    feedback = generate_feedback(found, missing, score, role)
    st.success(feedback)

    # PROJECTS
    st.markdown("## 🚀 Recommended Projects")
    projects = suggest_projects(role)
    for proj in projects:
        st.markdown(f"📌 {proj}")

    # DOWNLOAD
    report = f"""
Role: {role}
Score: {score}%
ATS Score: {ats_score}

Skills Found: {found}
Missing Skills: {missing}

ATS Missing Keywords: {ats_missing}

Projects: {projects}

Feedback:
{feedback}
"""

    st.download_button("📥 Download Report", report)

# FOOTER
st.markdown("---")
st.caption("Built by Amar Jyoth 🚀 (ULTIMATE VERSION)")

