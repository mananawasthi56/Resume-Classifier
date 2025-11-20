import streamlit as st
import re

st.set_page_config(page_title="Manan Awasthi • Resume AI for Data Roles", page_icon="Brain", layout="centered")

# GOD-TIER DATA SCIENCE THEME (Deep purple → teal gradient + neural glow)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #1a0033, #0f0f2d, #1a0033, #2d0055);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        color: #e6e6ff;
    }
    @keyframes gradient {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
    h1 {
        color: #00d4ff !important;
        text-align: center;
        font-weight: 800;
        font-size: 3rem;
        background: linear-gradient(90deg, #00d4ff, #ff00c8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h1::after {
        content: '';
        position: absolute;
        bottom: -12px; left: 50%;
        transform: translateX(-50%);
        width: 140px; height: 5px;
        background: linear-gradient(90deg, #00d4ff, #ff00c8);
        border-radius: 3px;
        animation: underline 4s infinite;
    }
    @keyframes underline {0%,100%{width:140px}50%{width:350px}}
    .stTextArea > div > div > textarea {
        background: rgba(20, 10, 50, 0.85)!important;
        color: #e6e6ff!important;
        border: 1px solid #00d4ff;
        border-radius: 16px;
        backdrop-filter: blur(12px);
    }
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #ff00c8)!important;
        color: white!important;
        font-weight: bold;
        border: none;
        border-radius: 16px;
        padding: 14px 40px;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 0, 200, 0.5);
    }
    .result-card {
        background: rgba(20, 10, 50, 0.9);
        border: 1px solid #00d4ff;
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
    .skill-tag {
        background: rgba(0, 212, 255, 0.25);
        color: #00d4ff;
        border: 1px solid #00d4ff;
        padding: 8px 16px;
        border-radius: 30px;
        margin: 6px;
        font-weight: 600;
    }
    .footer {text-align:center;padding:50px;color:#00d4ff;font-size:15px;margin-top:70px;}
    .ds-badge {
        background: linear-gradient(45deg, #00d4ff, #ff00c8);
        color: white;
        padding: 10px 24px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# HEADER — Pure Data Scientist Energy
st.markdown("<h1>Resume AI for Data Roles</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#b0b0ff; font-size:20px;'><strong>Built by Manan Awasthi</strong> • Data Scientist | ML | Analytics | Python</p>", unsafe_allow_html=True)
st.markdown("<div class='ds-badge'>DATA SCIENTIST PROJECT • 300+ ROLES • KEYWORD + NLP HYBRID</div>", unsafe_allow_html=True)

resume = st.text_area("Paste any resume (Tech • Medical • Finance • Marketing • Any Domain)", height=340)

# Keep your full 300+ role database here (same as last version)
ROLE_DATABASE = { ... }  # ← Paste the full 300+ roles from my previous message

ALL_SKILLS = list(set(skill for skills in ROLE_DATABASE.values() for skill in skills))

def extract_skills(text): ...   # same as before
def predict_role(text, skills): ...  # same as before

if st.button("Extract & Predict Role", use_container_width=True):
    if not resume.strip():
        st.error("Paste a resume first!")
    else:
        with st.spinner("Running inference across 300+ global roles..."):
            skills = extract_skills(resume)
            role, conf = predict_role(resume, skills)

        st.markdown("---")
        col1, col2 = st.columns([1, 1.4])
        with col1:
            st.markdown(f"<div class='result-card'><h3 style='color:#00d4ff;'>Predicted Role</h3><h2>{role}</h2><h4>Confidence: <strong>{conf}%</strong></h4></div>", unsafe_allow_html=True)
        with col2:
            skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
            skills_text = ", ".join(skills)
            st.markdown(f"<div class='result-card'><h3 style='color:#00d4ff;'>Extracted Skills</h3>{skills_html}<br><br><button class='small-btn' onclick=\"navigator.clipboard.writeText('{skills_text}'); alert('Copied!')\">Copy Skills</button></div>", unsafe_allow_html=True)

        st.success("Inference Complete — Ready for your Data Science Portfolio")
        st.balloons()

# DATA SCIENTIST FOOTER
st.markdown("""
<div class="footer">
    <strong>Manan Awasthi</strong> • Data Scientist | Machine Learning | Analytics<br>
    <a href="https://github.com/manan-awasthi" style="color:#00d4ff; text-decoration:none;">GitHub</a> • 
    <a href="https://linkedin.com/in/manan-awasthi" style="color:#00d4ff; text-decoration:none;">LinkedIn</a> • 
    <a href="mailto:manan@example.com" style="color:#00d4ff; text-decoration:none;">Email</a>
    <br><br><small>© 2025 Manan Awasthi • Built with Python, Streamlit & Pure Data Science Passion</small>
</div>
""", unsafe_allow_html=True)
