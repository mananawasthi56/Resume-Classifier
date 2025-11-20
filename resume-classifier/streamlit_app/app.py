import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.skill_extractor import extract_skills
from src.classifier import train, predict

# -------------------- PAGE CONFIG -------------------------
st.set_page_config(
    page_title="Intelligent Resume Classifier",
    page_icon="📄",
    layout="centered"
)

# -------------------- CUSTOM CSS -------------------------
st.markdown("""
<style>

body {
    background-color: #0e1117 !important;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-top: 20px;
}

.sub-text {
    text-align: center;
    color: #a6a6a6;
    margin-bottom: 30px;
}

.card {
    background: #161a23;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 0px 8px rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
}

textarea {
    background: #1e222f !important;
    color: white !important;
}

.stButton>button {
    width: 100%;
    background-color: #4c8bf5;
    color: white;
    padding: 10px 0px;
    border-radius: 8px;
    border: none;
    font-size: 16px;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #74a7ff;
}

.result-box {
    background: #1b1f2d;
    padding: 20px;
    border-radius: 12px;
    color: white;
    margin-top: 20px;
    border-left: 4px solid #4c8bf5;
}

</style>
""", unsafe_allow_html=True)

# -------------------- PAGE TITLE -------------------------
st.markdown('<div class="main-title">📄 Intelligent Resume Classifier & Skill Extractor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Paste any resume text below & get skills + predicted role instantly.</div>', unsafe_allow_html=True)

# -------------------- DATA LOAD -------------------------
data_path = Path(__file__).resolve().parents[1] / 'data' / 'resumes_sample.csv'
model = train(str(data_path))

# -------------------- INPUT CARD -------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    text = st.text_area("Paste Resume Text Below", height=250)

    submit = st.button("Extract & Predict")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- OUTPUT -------------------------
if submit:
    skills = extract_skills(text)
    pred = predict(model, [text])[0]

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    st.markdown(f"### 🎯 Predicted Role: **{pred}**")
    st.markdown("### 🧩 Extracted Skills:")
    st.write(", ".join(skills) if skills else "No skills found.")

    st.markdown('</div>', unsafe_allow_html=True)
