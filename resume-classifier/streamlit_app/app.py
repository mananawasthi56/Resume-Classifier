
import streamlit as st
import pandas as pd
from src.skill_extractor import extract_skills
from src.classifier import train, predict
from pathlib import Path

st.set_page_config(page_title='Resume Classifier', layout='centered')
st.title('Intelligent Resume Classifier & Skill Extractor (Demo)')

data_path = Path(__file__).parents[2] / 'data' / 'resumes_sample.csv'
model = train(str(data_path))

text = st.text_area('Paste resume text here', height=200)
if st.button('Extract & Predict'):
    skills = extract_skills(text)
    pred = predict(model, [text])[0]
    st.markdown('**Predicted role:** ' + str(pred))
    st.markdown('**Extracted skills:** ' + (', '.join(skills) if skills else 'None found'))
