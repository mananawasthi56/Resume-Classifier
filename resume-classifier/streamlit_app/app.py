import streamlit as st
import re
import json
from datetime import datetime

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Resume Classifier & Skill Extractor",
    page_icon="📄",
    layout="centered"
)

# ------------------- Custom CSS (Pro Tech Blue Theme) -------------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: #0a192f;
        color: #e6f1ff;
    }
    
    /* Headers */
    h1 {
        color: #64ffda !important;
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        text-align: center;
        font-weight: 700;
    }
    h3 {
        color: #ccd6f6;
    }
    
    /* Input Box */
    .stTextArea > div > div > textarea {
        background-color: #112240 !important;
        color: #e6f1ff !important;
        border: 1px solid #64ffda;
        border-radius: 12px;
        font-size: 16px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #64ffda, #00d4aa);
        color: #0a192f;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-size: 18px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(100, 255, 218, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(100, 255, 218, 0.6);
    }
    
    /* Result Cards */
    .result-card {
        background: rgba(17, 34, 64, 0.8);
        border: 1px solid #64ffda;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: rgba(100, 255, 218, 0.2);
        color: #64ffda;
        border: 1px solid #64ffda;
        padding: 6px 14px;
        border-radius: 20px;
        margin: 5px;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Copy & Download Buttons */
    .small-btn {
        background: #233554;
        color: #64ffda;
        border: 1px solid #64ffda;
        padding: 8px 16px;
        border-radius: 8px;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- Title -------------------
st.markdown("<h1>📄 Intelligent Resume Classifier<br>& Skill Extractor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8892b0;'>Paste your resume → Get predicted role + skills instantly</p>", unsafe_allow_html=True)
st.markdown("---")

# ------------------- Input -------------------
resume_text = st.text_area(
    "Paste Resume Text Below",
    height=300,
    placeholder="Manan Awasthi\nEmail: manan@example.com\nPhone: +91 9876543210\nLocation: India\n\nProfessional Summary\nData-driven and detail-oriented Data Analyst with hands-on experience in Python..."
)

# ------------------- Skill Database (Common for Data Roles) -------------------
SKILLS_DB = [
    "python", "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "machine learning",
    "sql", "excel", "power bi", "tableau", "data visualization", "data cleaning", "etl",
    "statistics", "r", "tensorflow", "pytorch", "nlp", "deep learning", "aws", "git", "docker"
]

ROLE_KEYWORDS = {
    "Data Analyst": ["analyst", "analytics", "bi", "visualization", "sql", "excel", "tableau", "power bi"],
    "Data Scientist": ["machine learning", "ml", "deep learning", "python", "statistics", "model"],
    "Data Engineer": ["etl", "pipeline", "spark", "airflow", "warehouse", "big data"],
    "ML Engineer": ["deployment", "mlops", "kubernetes", "docker", "production", "tensorflow"],
    "Business Analyst": ["requirements", "stakeholder", "jira", "agile", "ba"]
}

# ------------------- Extraction Logic -------------------
def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill.capitalize())
    return found if found else ["No strong technical skills detected"]

def predict_role(text, skills):
    text_lower = text.lower()
    scores = {}
    for role, keywords in ROLE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower or kw in " ".join(skills).lower())
        scores[role] = score
    if max(scores.values()) == 0:
        return "Fresher / General Role", 60
    best_role = max(scores, key=scores.get)
    confidence = min(95, 50 + scores[best_role] * 10)
    return best_role, confidence

# ------------------- Process Button -------------------
if st.button("🚀 Extract & Predict", use_container_width=True):
    if not resume_text.strip():
        st.error("Please paste your resume text first!")
    else:
        with st.spinner("Analyzing your resume..."):
            skills = extract_skills(resume_text)
            role, confidence = predict_role(resume_text, skills)
        
        # ------------------- Results -------------------
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#64ffda;">✨ Predicted Role</h3>
                <h2>{role}</h2>
                <p>Confidence: <strong>{confidence}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#64ffda;">Extracted Skills</h3>
                <div>
                    {''.join([f'<span class="skill-tag">{s}</span>' for s in skills[:20]])}
                </div>
                <br>
                <button class="small-btn" onclick="navigator.clipboard.writeText('{', '.join(skills)}')">
                    📋 Copy Skills
                </button>
                <button class="small-btn" onclick="alert('Download coming soon!')">
                    💾 Export JSON
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        st.success("Analysis Complete! Use this to tailor your resume & LinkedIn.")
        st.balloons()

# ------------------- Footer -------------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:#64ffda; font-size:14px;'>Built with ❤️ for Job-Ready Portfolios</p>", unsafe_allow_html=True)
