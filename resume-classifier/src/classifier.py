
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from .preprocessing import clean_text

def train(path):
    df = pd.read_csv(path)
    df['clean'] = df['resume_text'].apply(clean_text)
    model = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
    model.fit(df['clean'], df['label'])
    return model

def predict(model, texts):
    cleaned = [clean_text(t) for t in texts]
    return model.predict(cleaned)
