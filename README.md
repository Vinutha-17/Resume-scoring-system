# 📄 Resume Scoring System using NLP

A **web-based application** built with **Streamlit** that evaluates resumes against job descriptions using **Natural Language Processing (NLP)** techniques.  
It calculates a relevance score, extracts skills, highlights matching skills, and provides a word cloud visualization of the resume content.

---

## 🚀 Features

- **Resume Upload** – Supports PDF format for resume upload.
- **Job Description Input** – Paste any job description to compare.
- **Relevance Scoring** – Uses **TF-IDF** and **Cosine Similarity** to generate a score (0–100).
- **Skill Extraction** – Extracts skills from resume and job description using **spaCy**.
- **Matching Skills Highlight** – Highlights common skills for quick review.
- **Visual Analytics** – Progress bar for score and word cloud of resume keywords.
- **Interactive UI** – Built with **Streamlit** for ease of use.

---

## 🛠️ Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **Backend / NLP**: Python, scikit-learn, spaCy, NLTK
- **File Processing**: PyMuPDF (PDF parsing)
- **Visualization**: Matplotlib, WordCloud

---

## 📂 Project Structure
```bash
Resume-Scoring-System/
│
├── app.py # Main Streamlit application
├── requirements.txt # Required Python dependencies
├── sample_resume.pdf # Example resume file
└── README.md # Project documentation
```

---

## 📦 Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/yourusername/resume-scoring-system.git
cd resume-scoring-system
```

2️⃣ **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate      # For Mac/Linux
venv\Scripts\activate         # For Windows
```

3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Download required NLP models**
```bash
python -m nltk.downloader stopwords
python -m spacy download en_core_web_sm
```

▶️ **Usage**
```bash
streamlit run app.py
```
Then, open the local URL in your browser:
```bash
http://localhost:8501
```

