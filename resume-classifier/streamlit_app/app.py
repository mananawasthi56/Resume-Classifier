import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path

# FIX: Add parent directory to Python path so Streamlit can find /src
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.skill_extractor import extract_skills
from src.classifier import train, predict

st.set_page_config(page_title='Resume Classifier', layout='centered')
st.title('Intelligent Resume Classifier & Skill Extractor (Demo)')

# FIX: Correct the data path for Streamlit Cloud
data_path = Path(__file__).resolve().parents[1] / 'data' / 'resumes_sample.csv'

model = train(str(data_path))

text = st.text_area('Paste resume text here', height=200)
if st.button('Extract & Predict'):
    skills = extract_skills(text)
    pred = predict(model, [text])[0]
    st.markdown('**Predicted role:** ' + str(pred))
    st.markdown('**Extracted skills:** ' + (', '.join(skills) if skills else 'None found'))
