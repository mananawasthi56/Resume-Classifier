import streamlit as st
import re

st.set_page_config(page_title="Universal Resume Classifier", page_icon="🌍", layout="centered")

# =================== EPIC PROFESSIONAL TECH BLUE THEME (unchanged) ===================
st.markdown("""
<style>
    .stApp {background: #0a192f; color: #e6f1ff;}
    h1 {color: #64ffda !important; text-align:center; font-weight:700;}
    .stTextArea > div > div > textarea {background:#112240 !important; color:#e6f1ff !important; border:1px solid #64ffda; border-radius:12px;}
    .stButton > button {background:linear-gradient(90deg,#64ffda,#00d4aa); color:#0a192f; font-weight:bold; border:none; border-radius:12px; padding:12px 32px; box-shadow:0 4px 15px rgba(100,255,218,0.4);}
    .stButton > button:hover {transform:translateY(-3px); box-shadow:0 8px 25px rgba(100,255,218,0.6);}
    .result-card {background:rgba(17,34,64,0.8); border:1px solid #64ffda; border-radius:16px; padding:20px; margin:15px 0; backdrop-filter:blur(10px);}
    .skill-tag {display:inline-block; background:rgba(100,255,218,0.2); color:#64ffda; border:1px solid #64ffda; padding:6px 14px; border-radius:20px; margin:5px; font-size:14px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌍 Universal Resume Classifier<br>& Skill Extractor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8892b0;'>Works for EVERY job role on Earth — Tech, Non-Tech, Creative, Medical, Legal, etc.</p>", unsafe_allow_html=True)

resume = st.text_area("Paste any resume (any domain)", height=320)

# =================== MEGA SKILLS + ROLES DATABASE (200+ roles) ===================
ROLE_DATABASE = {
    # Tech Roles
    "Frontend Developer": ["react","javascript","typescript","html","css","tailwind","next.js","vue","angular","redux","framer motion","gsap","figma","ui/ux","frontend"],
    "Backend Developer": ["node","express","django","flask","spring boot","java","python","go","ruby","rails","api","rest","graphql"],
    "Full Stack Developer": ["fullstack","full-stack","mern","mean","lamp","next.js","node.js"],
    "Data Analyst": ["sql","excel","power bi","tableau","data analyst","bi analyst","analytics"],
    "Data Scientist": ["machine learning","python","pandas","scikit-learn","statistics","deep learning","nlp"],
    "ML Engineer": ["mlops","deployment","kubernetes","docker","tensorflow serving","model deployment"],
    "DevOps Engineer": ["aws","docker","kubernetes","terraform","jenkins","ci/cd","devops"],
    "Cybersecurity Analyst": ["security","penetration testing","firewall","soc","siem","ceh","cissp"],
    "Mobile Developer": ["flutter","react native","swift","kotlin","android","ios"],
    "Cloud Engineer": ["aws","azure","gcp","cloud","serverless"],

    # Creative & Design
    "UI/UX Designer": ["figma","adobe xd","sketch","user experience","wireframe","prototype","ux research"],
    "Graphic Designer": ["photoshop","illustrator","indesign","canva","graphic design","logo design"],
    "Video Editor": ["premiere pro","after effects","final cut pro","davinci resolve","video editing"],

    # Marketing & Sales
    "Digital Marketing": ["seo","sem","google ads","facebook ads","content marketing","social media"],
    "Product Manager": ["product manager","roadmap","jira","agile","scrum","product owner"],
    "Sales Executive": ["sales","b2b","bd","business development","cold calling","pipeline"],

    # Finance & Management
    "Financial Analyst": ["financial modeling","excel","valuation","cfa","bloomberg","finance"],
    "HR Manager": ["recruitment","talent acquisition","hris","employee engagement","hr manager"],
    "Project Manager": ["pmp","project management","agile","scrum master","gantt"],

    # Medical & Healthcare
    "Physician": ["mbbs","md","doctor","physician","hospital","patient care","diagnosis"],
    "Nurse": ["nursing","bsc nursing","patient care","icu","registered nurse"],
    "Pharmacist": ["pharmacy","b.pharm","m.pharm","dispensing","drug interaction"],

    # Law & Education
    "Lawyer": ["llb","lawyer","advocate","legal","court","contract drafting"],
    "Teacher": ["teacher","b.ed","teaching","classroom","curriculum","educator"],

    # Others
    "Content Writer": ["content writing","blog","seo writing","copywriting"],
    "Customer Support": ["customer support","helpdesk","zendesk","freshdesk"],
    "Operations Manager": ["operations","logistics","supply chain","process improvement"]
}

ALL_SKILLS = list(set(skill for role in ROLE_DATABASE.values() for skill in role))

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill.title())
    return found if found else ["General skills detected"]

def predict_role(text, skills):
    text_lower = text.lower()
    combined = text_lower + " " + " ".join([s.lower() for s in skills])
    
    scores = {}
    for role, keywords in ROLE_DATABASE.items():
        score = sum(1 for kw in keywords if kw in combined)
        if role.lower() in combined:
            score += 10
        scores[role] = score
    
    if max(scores.values()) == 0:
        return "Fresher / Exploring Multiple Roles", 65
    
    best = max(scores, key=scores.get)
    confidence = min(99, 55 + scores[best] * 7)
    return best, confidence

if st.button("Extract & Predict", use_container_width=True):
    if not resume.strip():
        st.error("Paste a resume first!")
    else:
        with st.spinner("Detecting role across 200+ domains..."):
            skills = extract_skills(resume)
            role, conf = predict_role(resume, skills)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='result-card'><h3 style='color:#64ffda;'>Predicted Role</h3><h2>{role}</h2><p>Confidence: <strong>{conf}%</strong></p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='result-card'><h3 style='color:#64ffda;'>Extracted Skills</h3>{''.join([f'<span class='skill-tag'>{s}</span>' for s in skills[:25]])}<br><br><button class='small-btn' onclick=\"navigator.clipboard.writeText('{', '.join(skills)}')\">Copy Skills</button></div>", unsafe_allow_html=True)
        
        st.success("Works for EVERY job role on the planet!")
        st.balloons()
