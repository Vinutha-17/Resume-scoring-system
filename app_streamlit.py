import streamlit as st
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re


dark_mode = st.toggle("🌙 Dark Mode")

# Inject background CSS
def set_background(is_dark):
    if is_dark:
        # Dark mode
        st.markdown("""
            <style>
            body {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            .stApp {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Light mode
        st.markdown("""
            <style>
            body {
                background-color: #f0f2f6;
                color: #000000;
            }
            .stApp {
                background-color: #f0f2f6;
                color: #000000;
            }
            </style>
        """, unsafe_allow_html=True)

# Call background setter
set_background(dark_mode)

# --------------------- #
# Text Extraction
# --------------------- #
def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception:
        return ""

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

# --------------------- #
# Utility Functions
# --------------------- #
def extract_keywords(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    return list(set(words))

def calculate_similarity(jd_text, resume_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([jd_text, resume_text])
    sim_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(sim_score * 100, 2)

def highlight_text(text, keywords):
    highlighted = text
    for word in sorted(keywords, key=len, reverse=True):
        highlighted = re.sub(f"(?i)\\b({re.escape(word)})\\b", r"<mark>\1</mark>", highlighted)
    return highlighted

# --------------------- #
# Streamlit App
# --------------------- #
st.set_page_config(page_title="Resume Relevance Scorer", layout="wide")
st.title("📄 Resume Relevance Scorer")

st.header("1️⃣ Upload Job Description")
jd_file = st.file_uploader("Upload JD (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], key="jd")

st.header("2️⃣ Upload Resumes")
resume_files = st.file_uploader("Upload Resume Files (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True, key="resumes")

# Toggle Buttons
show_jd_keywords = st.toggle("📌 Show JD Keywords", value=True)
show_keywords = st.toggle("📊 Show Matched Keywords Table", value=True)
show_highlight = st.toggle("🖍️ Show Highlighted Resume Snippets", value=True)

if jd_file and resume_files:
    # Extract JD text
    if jd_file.name.endswith(".pdf"):
        jd_text = extract_text_from_pdf(jd_file)
    elif jd_file.name.endswith(".docx"):
        jd_text = extract_text_from_docx(jd_file)
    elif jd_file.name.endswith(".txt"):
        jd_text = extract_text_from_txt(jd_file)
    else:
        st.error("Unsupported JD file format")
        st.stop()

    jd_keywords = extract_keywords(jd_text)

    if show_jd_keywords:
        st.success("✅ Extracted Keywords from JD:")
        st.write(", ".join(jd_keywords))

    # Process Resumes
    results = []
    for resume in resume_files:
        if resume.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume)
        elif resume.name.endswith(".docx"):
            resume_text = extract_text_from_docx(resume)
        elif resume.name.endswith(".txt"):
            resume_text = extract_text_from_txt(resume)
        else:
            st.warning(f"Skipping unsupported file format: {resume.name}")
            continue

        similarity = calculate_similarity(jd_text, resume_text)
        resume_keywords = extract_keywords(resume_text)
        matched_keywords = set(jd_keywords).intersection(resume_keywords)
        results.append({
            "Resume File": resume.name,
            "Similarity (%)": similarity,
            "Matched Keywords": ", ".join(matched_keywords),
            "Full Text": resume_text,
            "Highlights": highlight_text(resume_text.replace('\n', ' <br> '), matched_keywords)
        })

    df = pd.DataFrame(results)

    if show_keywords:
        st.header("📊 Resume Similarity Scores")
        st.dataframe(df[["Resume File", "Similarity (%)", "Matched Keywords"]])

    if show_highlight:
        st.header("📌 Resume Highlight Viewer")
        for i, row in df.iterrows():
            st.subheader(f"🔸 {row['Resume File']} — {row['Similarity (%)']}% Match")
            st.markdown(
    f"""
    <div style='
        background-color:#fefefe;
        padding:16px;
        border: 1px solid #ddd;
        border-radius:10px;
        max-height:600px;
        overflow:auto;
        line-height:1.6;
        font-family:monospace;
        white-space:pre-wrap;
    '>
        {row['Highlights']}
    </div>
    """,
    unsafe_allow_html=True
)



else:
    st.info("Upload both Job Description and Resumes to get started.")
