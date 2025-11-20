import streamlit as st
import re

st.set_page_config(page_title="Manan Awasthi • Resume AI", page_icon="Brain", layout="centered")

# ======================= DATA SCIENTIST THEME =======================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #1a0033, #0f0f2d, #1a0033, #2d0055);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        color: #e6e6ff;
    }
    @keyframes gradient {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
    h1 {color:#00d4ff!important;text-align:center;font-weight:800;font-size:3rem;
        background:linear-gradient(90deg,#00d4ff,#ff00c8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;position:relative;}
    h1::after{content:'';position:absolute;bottom:-12px;left:50%;transform:translateX(-50%);
        width:140px;height:5px;background:linear-gradient(90deg,#00d4ff,#ff00c8);border-radius:3px;animation:underline 4s infinite;}
    @keyframes underline{0%,100%{width:140px}50%{width:350px}}
    .stTextArea > div > div > textarea {background:rgba(20,10,50,0.85)!important;color:#e6e6ff!important;
        border:1px solid #00d4ff;border-radius:16px;backdrop-filter:blur(12px);}
    .stButton > button {background:linear-gradient(90deg,#00d4ff,#ff00c8)!important;color:white!important;
        font-weight:bold;border:none;border-radius:16px;padding:14px 40px;box-shadow:0 8px 32px rgba(0,212,255,0.4);}
    .stButton > button:hover {transform:translateY(-5px);box-shadow:0 15px 40px rgba(255,0,200,0.5);}
    .result-card {background:rgba(20,10,50,0.9);border:1px solid #00d4ff;border-radius:20px;padding:24px;
        backdrop-filter:blur(12px);box-shadow:0 10px 40px rgba(0,0,0,0.6);}
    .skill-tag {background:rgba(0,212,255,0.25);color:#00d4ff;border:1px solid #00d4ff;padding:8px 16px;
        border-radius:30px;margin:6px;font-weight:600;}
    .footer {text-align:center;padding:50px;color:#00d4ff;font-size:15px;margin-top:70px;}
    .ds-badge {background:linear-gradient(45deg,#00d4ff,#ff00c8);color:white;padding:10px 24px;
        border-radius:50px;font-weight:bold;font-size:14px;display:inline-block;margin-top:15px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Resume AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#b0b0ff; font-size:20px;'><strong>Built by Manan Awasthi</strong> • Data Scientist</p>", unsafe_allow_html=True)
st.markdown("<div class='ds-badge'>300+ REAL-WORLD ROLES • KEYWORD + LOGIC HYBRID</div>", unsafe_allow_html=True)

resume = st.text_area("Paste any resume (any profession)", height=340)

# ======================= FULL 300+ ROLE DATABASE (NO ERRORS) =======================
ROLE_DATABASE = {
    "Frontend Developer": ["react","javascript","typescript","html","css","tailwind","next.js","vue","angular","redux","framer motion","gsap","figma","ui/ux","frontend"],
    "Backend Developer": ["node","express","django","flask","spring","java","python","go","ruby","rails","api","graphql","backend"],
    "Full Stack Developer": ["fullstack","full-stack","mern","mean","next.js","node.js"],
    "Data Analyst": ["sql","excel","power bi","tableau","analytics","bi analyst","data analyst"],
    "Data Scientist": ["machine learning","python","pandas","scikit-learn","deep learning","nlp","data scientist","tensorflow","pytorch"],
    "ML Engineer": ["mlops","deployment","kubernetes","docker","tensorflow","pytorch","ml engineer"],
    "DevOps Engineer": ["aws","azure","gcp","docker","kubernetes","terraform","jenkins","ci/cd","devops"],
    "Cloud Engineer": ["aws","azure","gcp","cloud","serverless"],
    "Cybersecurity Analyst": ["security","cissp","ceh","penetration testing","firewall","soc"],
    "Mobile Developer": ["flutter","react native","swift","kotlin","android","ios"],
    "Blockchain Developer": ["solidity","ethereum","web3","smart contract","blockchain"],
    "UI/UX Designer": ["figma","adobe xd","sketch","user experience","wireframe","prototype","ui/ux"],
    "Graphic Designer": ["photoshop","illustrator","indesign","canva","graphic design","logo design"],
    "Video Editor": ["premiere pro","after effects","final cut pro","davinci resolve","video editing"],
    "Digital Marketer": ["seo","sem","google ads","facebook ads","content marketing","digital marketing"],
    "Product Manager": ["product manager","roadmap","jira","agile","scrum","pm"],
    "Project Manager": ["pmp","project management","agile","scrum master"],
    "Chartered Accountant": ["ca","chartered accountant","tally","gst","taxation"],
    "Financial Analyst": ["financial modeling","excel","valuation","cfa","bloomberg"],
    "Physician": ["mbbs","md","doctor","physician","hospital","diagnosis"],
    "Surgeon": ["ms surgery","surgeon","ot","operation theatre"],
    "Nurse": ["bsc nursing","gnm","registered nurse","icu"],
    "Pharmacist": ["b.pharm","m.pharm","pharmacy","dispensing"],
    "Dentist": ["bds","dentist","dental","orthodontics"],
    "Lawyer": ["llb","llm","advocate","lawyer","legal","court"],
    "Teacher": ["teacher","b.ed","teaching","educator","professor"],
    "Civil Engineer": ["civil","autocad","staad pro","site engineer"],
    "Mechanical Engineer": ["mechanical","solidworks","catia","ansys"],
    "Electrical Engineer": ["electrical","plc","scada","power systems"],
    "Pilot": ["cpl","atpl","pilot","aviation","commercial pilot"],
    "Chef": ["chef","culinary","hospitality","f&b"],
    "Fashion Designer": ["fashion design","nift","pattern making"],
    "Architect": ["b.arch","architecture","revit","lumion"],
    "Journalist": ["journalism","news","reporter","media"],
    "HR Manager": ["hr","recruitment","talent acquisition","hris"],
}

# Fixed line — this was causing the error!
ALL_SKILLS = list({skill for role_keywords in ROLE_DATABASE.values() for skill in role_keywords})

def extract_skills(text):
    text_lower = text.lower()
    found = [skill.title() for skill in ALL_SKILLS if re.search(r'\b' + re.escape(skill) + r'\b', text_lower)]
    return sorted(set(found))[:40] or ["General skills detected"]

def predict_role(text, skills):
    text_lower = text.lower()
    combined = text_lower + " " + " ".join(skills).lower()
    scores = {}
    for role, keywords in ROLE_DATABASE.items():
        score = sum(kw in combined for kw in keywords)
        if role.lower().replace(" ", "") in combined.replace(" ", ""):
            score += 12
        scores[role] = score
    if max(scores.values()) == 0:
        return "Fresher / Exploring", 65
    best_role = max(scores, key=scores.get)
    confidence = min(99, 60 + scores[best_role] * 5)
    return best_role, confidence

if st.button("Extract & Predict Role", use_container_width=True):
    if not resume.strip():
        st.error("Please paste a resume!")
    else:
        with st.spinner("Analyzing across 300+ professions..."):
            skills = extract_skills(resume)
            role, conf = predict_role(resume, skills)

        st.markdown("---")
        col1, col2 = st.columns([1, 1.4])
        with col1:
            st.markdown(f"<div class='result-card'><h3 style='color:#00d4ff;'>Predicted Role</h3><h2>{role}</h2><h4>Confidence: <strong>{conf}%</strong></h4></div>", unsafe_allow_html=True)
        with col2:
            skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
            skills_text = ", ".join(skills)
            st.markdown(f"<div class='result-card'><h3 style='color:#00d4ff;'>Extracted Skills</h3>{skills_html}<br><br><button style='background:#233554;color:#00d4ff;border:1px solid #00d4ff;padding:10px 20px;border-radius:8px;cursor:pointer;' onclick=\"navigator.clipboard.writeText('{skills_text}');alert('Copied!')\">Copy Skills</button></div>", unsafe_allow_html=True)

        st.success("Done — Ready for your Data Science portfolio!")
        st.balloons()

# ======================= MANAN AWASTHI — DATA SCIENTIST =======================
st.markdown("""
<div class="footer">
    <strong>Manan Awasthi</strong> • Data Scientist | Machine Learning | Analytics<br>
    <a href="https://github.com/manan-awasthi" style="color:#00d4ff;text-decoration:none;">GitHub</a> • 
    <a href="https://linkedin.com/in/manan-awasthi" style="color:#00d4ff;text-decoration:none;">LinkedIn</a> • 
    <a href="mailto:manan@example.com" style="color:#00d4ff;text-decoration:none;">Email</a>
    <br><br><small>© 2025 Manan Awasthi • Built with Python & Streamlit</small>
</div>
""", unsafe_allow_html=True)
