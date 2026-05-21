
import streamlit as st
import pdfplumber

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

skills = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "data analysis",
    "communication",
    "leadership",
    "streamlit",
    "opencv"
]

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    resume_text = text.lower()

    found_skills = []

    for skill in skills:
        if skill in resume_text:
            found_skills.append(skill)

    score = len(found_skills) * 10

    if score > 100:
        score = 100

    st.subheader("Skills Found")
    st.write(found_skills)

    st.subheader("Resume Score")
    st.write(f"{score} / 100")

    suggestions = []

    if "python" not in found_skills:
        suggestions.append("Add Python skill")

    if "sql" not in found_skills:
        suggestions.append("Add SQL skill")

    if "machine learning" not in found_skills:
        suggestions.append("Add Machine Learning projects")

    if "communication" not in found_skills:
        suggestions.append("Mention communication skills")

    if "streamlit" not in found_skills:
        suggestions.append("Add Streamlit project experience")

    st.subheader("Suggestions")

    for s in suggestions:
        st.write("- ", s)
