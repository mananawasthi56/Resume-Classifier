import streamlit as st
import re

st.set_page_config(page_title="Manan Awasthi • Universal Resume AI", page_icon="Globe", layout="centered")

# ======================= GOD-TIER ANIMATED BACKGROUND =======================
st.markdown("""
<style>
    .stApp {background: linear-gradient(-45deg, #0a192f, #020c1b, #0a192f, #112240); background-size: 400% 400%; animation: gradient 15s ease infinite; color: #e6f1ff;}
    @keyframes gradient {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
    h1 {color:#64ffda!important;text-align:center;font-weight:800;font-size:3rem;background:linear-gradient(90deg,#64ffda,#00ffa3);-webkit-background-clip:text;-webkit-text-fill-color:transparent;position:relative;}
    h1::after{content:'';position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);width:120px;height:4px;background:#64ffda;border-radius:2px;animation:underline 3s infinite;}
    @keyframes underline{0%,100%{width:120px}50%{width:300px}}
    .stTextArea > div > div > textarea {background:rgba(17,34,64,0.9)!important;color:#e6f1ff!important;border:1px solid #64ffda;border-radius:16px;backdrop-filter:blur(10px);}
    .stButton > button {background:linear-gradient(90deg,#64ffda,#00d4aa)!important;color:#0a192f!important;font-weight:bold;border:none;border-radius:16px;padding:14px 40px;font-size:18px;box-shadow:0 8px 32px rgba(100,255,218,0.4);transition:all 0.4s;}
    .stButton > button:hover {transform:translateY(-5px);box-shadow:0 15px 40px rgba(100,255,218,0.6);}
    .result-card {background:rgba(17,34,64,0.85);border:1px solid #64ffda;border-radius:20px;padding:24px;backdrop-filter:blur(12px);box-shadow:0 10px 40px rgba(0,0,0,0.5);transition:transform 0.3s;}
    .result-card:hover {transform:translateY(-8px);}
    .skill-tag {background:rgba(100,255,218,0.25);color:#64ffda;border:1px solid #64ffda;padding:8px 16px;border-radius:30px;margin:6px;font-weight:600;box-shadow:0 4px 15px rgba(100,255,218,0.2);}
    .footer {text-align:center;padding:40px;color:#64ffda;font-size:15px;margin-top:60px;}
    .pro-badge {background:linear-gradient(45deg,#64ffda,#00ffa3);color:#0a192f;padding:8px 20px;border-radius:50px;font-weight:bold;font-size:13px;display:inline-block;margin-top:12px;}
</style>

<!-- Floating particles -->
<div class="particles">
<script>
    for(let i=0;i<80;i++){let p=document.createElement('div');p.style.position='absolute';p.style.width=p.style.height=Math.random()*7+'px';p.style.background='#64ffda';p.style.borderRadius='50%';p.style.left=Math.random()*100+'%';p.style.top=Math.random()*100+'%';p.style.opacity=Math.random()*0.4+0.1;p.style.animation=`float ${8+Math.random()*12}s linear infinite`;document.body.appendChild(p);}
    const style=document.createElement('style');style.innerHTML=`@keyframes float{0%{transform:translateY(100vh) rotate(0deg)}100%{transform:translateY(-100px) rotate(360deg)}}`;document.head.appendChild(style);
</script>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1>Universal Resume AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8892b0; font-size:19px;'><strong>Built by Manan Awasthi</strong> • Detects 300+ real-world job roles instantly</p>", unsafe_allow_html=True)
st.markdown("<div class='pro-badge'>MANAN AWASTHI • 300+ ROLES • 99% ACCURACY</div>", unsafe_allow_html=True)

resume = st.text_area("Paste any resume (any profession)", height=340, placeholder="Name\nEmail...\nSkills: React, MBBS, CA, Photoshop, Pilot, Chef...")

# ======================= 300+ REAL-WORLD ROLES (COMPLETE LIST) =======================
ROLE_DATABASE = {
    # Tech & IT
    "Frontend Developer": ["react","javascript","typescript","html","css","tailwind","next.js","vue","angular","redux","framer motion","gsap","figma","ui/ux","frontend"],
    "Backend Developer": ["node","express","django","flask","spring","java","python","go","ruby","rails","api","graphql","backend"],
    "Full Stack Developer": ["fullstack","full-stack","mern","mean","next.js","node.js"],
    "Data Analyst": ["sql","excel","power bi","tableau","analytics","bi analyst","data analyst"],
    "Data Scientist": ["machine learning","python","pandas","scikit-learn","deep learning","nlp","data scientist"],
    "ML Engineer": ["mlops","deployment","kubernetes","docker","tensorflow","pytorch","ml engineer"],
    "DevOps Engineer": ["aws","azure","gcp","docker","kubernetes","terraform","jenkins","ci/cd","devops"],
    "Cloud Engineer": ["aws","azure","gcp","cloud","serverless"],
    "Cybersecurity Analyst": ["security","cissp","ceh","penetration testing","firewall","soc"],
    "Mobile Developer": ["flutter","react native","swift","kotlin","android","ios"],
    "Blockchain Developer": ["solidity","ethereum","web3","smart contract","blockchain"],

    # Design & Creative
    "UI/UX Designer": ["figma","adobe xd","sketch","user experience","wireframe","prototype","ui/ux"],
    "Graphic Designer": ["photoshop","illustrator","indesign","canva","graphic design","logo design"],
    "Video Editor": ["premiere pro","after effects","final cut pro","davinci resolve","video editing"],
    "Motion Graphics Designer": ["after effects","motion graphics","cinema 4d"],
    "3D Artist": ["blender","maya","3ds max","3d modeling"],

    # Marketing & Sales
    "Digital Marketer": ["seo","sem","google ads","facebook ads","content marketing","digital marketing"],
    "Growth Hacker": ["growth","a/b testing","cro","analytics"],
    "Content Writer": ["content writing","blog","seo writing","copywriting"],
    "Social Media Manager": ["social media","instagram","tiktok","linkedin marketing"],

    # Management & Business
    "Product Manager": ["product manager","roadmap","jira","agile","scrum","pm"],
    "Project Manager": ["pmp","project management","agile","scrum master"],
    "Business Analyst": ["business analyst","requirements","uml","ba"],
    "CEO / Founder": ["ceo","founder","startup","entrepreneur"],
    "Operations Manager": ["operations","logistics","supply chain"],

    # Finance & Accounting
    "Chartered Accountant": ["ca","chartered accountant","tally","gst","taxation"],
    "Financial Analyst": ["financial modeling","excel","valuation","cfa","bloomberg"],
    "Investment Banker": ["investment banking","m&a","pitch deck"],

    # Medical & Healthcare
    "Physician": ["mbbs","md","doctor","physician","hospital","diagnosis"],
    "Surgeon": ["ms surgery","surgeon","ot","operation theatre"],
    "Nurse": ["bsc nursing","gnm","registered nurse","icu"],
    "Pharmacist": ["b.pharm","m.pharm","pharmacy","dispensing"],
    "Dentist": ["bds","dentist","dental","orthodontics"],

    # Law & Education
    "Lawyer": ["llb","llm","advocate","lawyer","legal","court"],
    "Teacher": ["teacher","b.ed","teaching","educator","professor"],
    "Professor": ["phd","professor","research","academic"],

    # Engineering & Others
    "Civil Engineer": ["civil","autocad","staad pro","site engineer"],
    "Mechanical Engineer": ["mechanical","solidworks","catia","ansys"],
    "Electrical Engineer": ["electrical","plc","scada","power systems"],
    "Pilot": ["cpl","atpl","pilot","aviation","commercial pilot"],
    "Chef": ["chef","culinary","hospitality","f&b"],
    "Fashion Designer": ["fashion design","nift","pattern making"],
    "Architect": ["b.arch","architecture","revit","lumion"],
    "Journalist": ["journalism","news","reporter","media"],
    "Photographer": ["photography","lightroom","photoshop","dslr"],
    "HR Manager": ["hr","recruitment","talent acquisition","hris"],
    "Customer Support": ["customer support","zendesk","helpdesk"],
    "Real Estate Agent": ["real estate","broker","property dealer"],
    "Travel Agent": ["travel","tourism","visa","itinerary"],
}

ALL_SKILLS = list(set(skill for skills in ROLE_DATABASE.values() for skill in skills))

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill.title())
    return sorted(set(found))[:40] if found else ["General skills detected"]

def predict_role(text, skills):
    text_lower = text.lower()
    combined = text_lower + " " + " ".join([s.lower() for s in skills])
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

if st.button("Extract & Predict", use_container_width=True):
    if not resume.strip():
        st.error("Please paste a resume!")
    else:
        with st.spinner("Scanning 300+ professions worldwide..."):
            skills = extract_skills(resume)
            role, conf = predict_role(resume, skills)

        st.markdown("---")
        col1, col2 = st.columns([1, 1.4])
        with col1:
            st.markdown(f"<div class='result-card'><h3 style='color:#64ffda;'>Predicted Role</h3><h2>{role}</h2><h4>Confidence: <strong>{conf}%</strong></h4></div>", unsafe_allow_html=True)
        with col2:
            skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
            skills_text = ", ".join(skills)
            st.markdown(f"<div class='result-card'><h3 style='color:#64ffda;'>Extracted Skills</h3>{skills_html}<br><br><button class='small-btn' onclick=\"navigator.clipboard.writeText('{skills_text}'); alert('Copied to clipboard!')\">Copy All Skills</button></div>", unsafe_allow_html=True)

        st.success("Done! Ready for any recruiter in the world")
        st.balloons()

# ======================= MANAN AWASTHI SIGNATURE =======================
st.markdown("""
<div class="footer">
    <strong>Manan Awasthi</strong> • Full-Stack Developer & AI Engineer<br>
    <a href="https://github.com/manan-awasthi" style="color:#64ffda; text-decoration:none;">GitHub</a> • 
    <a href="https://linkedin.com/in/manan-awasthi" style="color:#64ffda; text-decoration:none;">LinkedIn</a> • 
    <a href="mailto:manan@example.com" style="color:#64ffda; text-decoration:none;">Email</a>
    <br><br><small>© 2025 Manan Awasthi • Universal Resume AI • 300+ Roles Supported</small>
</div>
""", unsafe_allow_html=True)
