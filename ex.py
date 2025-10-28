import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

file_path = "C:/Users/manan/Downloads/archive (2)/Resume/Resume.csv"
df = pd.read_csv(file_path)
df = df[['Category', 'Resume_str']]
df.dropna(inplace=True)
df['Resume_str'] = df['Resume_str'].str.replace(r'http\S+|www.\S+', '', regex=True)
df['Resume_str'] = df['Resume_str'].str.replace(r'[^a-zA-Z ]', '', regex=True)
df['Resume_str'] = df['Resume_str'].str.lower()

plt.figure(figsize=(10,5))
sns.countplot(y=df['Category'], order=df['Category'].value_counts().index, palette="coolwarm")
plt.title("Number of Resumes per Category")
plt.xlabel("Count"); plt.ylabel("Category")
plt.tight_layout(); plt.savefig("category_distribution.png"); plt.close()

df["Resume_Length"] = df["Resume_str"].apply(lambda x: len(x.split()))
plt.figure(figsize=(8,5))
sns.histplot(df["Resume_Length"], kde=True, bins=30, color="skyblue")
plt.title("Resume Length Distribution")
plt.xlabel("Number of Words"); plt.ylabel("Frequency")
plt.tight_layout(); plt.savefig("resume_length.png"); plt.close()

vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
X = vectorizer.fit_transform(df['Resume_str'])
y = df['Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier(n_estimators=150, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, zero_division=0)

st.set_page_config(page_title="Intelligent Resume Classifier", layout="wide")
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Dashboard", "🧠 Resume Prediction"])

if page == "🏠 Dashboard":
    st.title("📊 Resume Category Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.image("category_distribution.png", caption="Resumes per Category", use_container_width=True)
    with col2:
        st.image("resume_length.png", caption="Resume Length Distribution", use_container_width=True)
    st.subheader("📈 Model Performance")
    st.write(f"**Accuracy:** {round(accuracy * 100, 2)}%")
    st.text("Classification Report:")
    st.text(report)

elif page == "🧠 Resume Prediction":
    st.title("🧠 Intelligent Resume Classifier")
    resume_input = st.text_area("✍️ Paste Resume Text Here:", height=300)
    if st.button("🔍 Predict Category"):
        if resume_input.strip() == "":
            st.warning("Please enter resume text.")
        else:
            cleaned_resume = resume_input.lower()
            cleaned_resume = " ".join([word for word in cleaned_resume.split() if word.isalpha()])
            input_features = vectorizer.transform([cleaned_resume])
            prediction = rf.predict(input_features)[0]
            st.success(f"🎯 Predicted Resume Category: {prediction}")
            probs = rf.predict_proba(input_features)
            top3 = np.argsort(probs[0])[-3:][::-1]
            st.subheader("🔎 Prediction Confidence:")
            for idx in top3:
                st.write(f"- {rf.classes_[idx]}: {probs[0][idx]*100:.2f}%")
