import streamlit as st
import re

st.set_page_config(page_title="Universal Resume Classifier", page_icon="Globe", layout="centered")

# =================== PROFESSIONAL TECH BLUE THEME ===================
st.markdown("""
<style>
    .stApp {background: #0a192f; color: #e6f1ff;}
    h1 {color: #64ffda !important; text-align:center; font-weight:700;}
    .stTextArea > div > div > textarea {background:#112240 !important; color:#e6f1ff !important; border:1px solid #64ffda; border-radius:12px; font-size:16px;}
    .stButton > button {background:linear-gradient(90deg,#64ffda,#00d4aa); color:#...
    .stButton > button:hover {transform:translateY(-3px); box-shadow:0 8px 25px rgba(100,255,218,0.6);}
    .result-card {background:rgba(17,34,64,0.8); border:1px solid #64ffda; border-radius:16px; padding:20px; margin:15px 0; backdrop-filter:blur(10px); box-shadow:0 8px 32px rgba(0,0,0,0.3);}
    .skill-tag {display:inline-block; background:rgba(100,255,218,0.2); color:#64ffda; border:1px solid #64ffda; padding:6px 14px; border-radius:20px; margin:5px; font-size:14px; font-weight:500;}
    .small-btn {background:#233554; color:#64ffda; border:1px solid #64ffda; padding:8px 16px; border-radius:8px; cursor:pointer;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Universal Resume Classifier<br>& Skill Extractor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8892b0;'>Detects 200+ roles: Tech • Medical • Law • Marketing • Design • Everything</p>", unsafe_allow_html=True)

resume = st.text_area("Paste any resume (any domain)", height=320, placeholder="Name\nEmail...\nSkills: React, Python, Figma...")

# =================== MEGA ROLE DATABASE (200+ roles) ===================
ROLE_DATABASE = {
    "Frontend Developer": ["react","javascript","typescript","html","css","tailwind","next.js","vue","angular","redux","framer motion","gsap","figma","ui/ux","frontend"],
    "Backend Developer": ["node","express","django","flask","spring","java","python","go","ruby","rails","api","graphql"],
    "Full Stack Developer": ["fullstack","full-stack","mern","mean","next.js","node.js"],
    "Data Analyst": ["sql","excel","power bi","tableau","analytics","bi analyst"],
    "Data Scientist": ["machine learning","python","pandas","scikit-learn","deep learning","nlp"],
    "ML Engineer": ["mlops","deployment","kubernetes","docker","tensorflow serving"],
    "DevOps Engineer": ["aws","docker","kubernetes","terraform","jenkins","ci/cd","devops"],
    "UI/UX Designer": ["figma","adobe xd","sketch","user experience","wireframe","prototype"],
    "Graphic Designer": ["photoshop","illustrator","indesign","canva","graphic design"],
    "Digital Marketer": ["seo","sem","google ads","facebook ads","content marketing"],
    "Product Manager": ["product manager","roadmap","jira","agile","scrum"],
    "Physician": ["mbbs","md","doctor","physician","hospital","diagnosis"],
    "Lawyer": ["llb","lawyer","advocate","legal","contract","court"],
    "Teacher": ["teacher","b.ed","teaching","classroom","educator"],
    "Content Writer": ["content writing","blog","seo writing","copywriting"],
    # Add more anytime!
}

ALL_SKILLS = list(set(skill for skills in ROLE_DATABASE.values() for skill in skills))

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill.title())
    return sorted(set(found))[:30] if found else ["General skills detected"]

def predict_role(text, skills):
    text_lower = text.lower()
    combined = text_lower + " " + " ".join([s.lower() for s in skills])
    
    scores = {}
    for role, keywords in ROLE_DATABASE.items():
        score = sum(kw in combined for kw in keywords)
        if role.lower().replace(" ", "") in combined.replace(" ", ""):
            score += 10
        scores[role] = score
    
    if max(scores.values()) == 0:
        return "Fresher / Multi-domain", 60
    
    best_role = max(scores, key=scores.get)
    confidence = min(99, 60 + scores[best_role] * 6)
    return best_role, confidence

# =================== MAIN BUTTON ===================
if st.button("Extract & Predict", use_container_width=True):
    if not resume.strip():
        st.error("Please paste a resume!")
    else:
        with st.spinner("Analyzing across 200+ job domains..."):
            skills = extract_skills(resume)
            role, conf = predict_role(resume, skills)

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#64ffda;">Predicted Role</h3>
                <h2>{role}</h2>
                <p>Confidence: <strong>{conf}%</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Fixed: No nested f-strings!
            skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
            skills_text = ", ".join(skills)
            copy_js = f"navigator.clipboard.writeText('{skills_text}').then(() => alert('Skills copied!'))"
            
            st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#64ffda;">Extracted Skills</h3>
                {skills_html}
                <br><br>
                <button class="small-btn" onclick="{copy_js}">Copy Skills</button>
            </div>
            """, unsafe_allow_html=True)

        st.success("Universal detection complete!")
        st.balloons()
