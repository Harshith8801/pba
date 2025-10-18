# -----------------------------
# Streamlit News Classifier: PCA vs Factor Analysis
# -----------------------------
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df = df.dropna().reset_index(drop=True)
    # rename column if it's not 'category'
    if 'category' not in df.columns:
        for col in df.columns:
            if col.lower() in ['label', 'class', 'target']:
                df = df.rename(columns={col: 'category'})
                break
    return df

@st.cache_resource
def build_vectorizer(max_features=5000, ngram_range=(1,2)):
    return TfidfVectorizer(max_features=max_features, ngram_range=ngram_range, stop_words='english')

# -----------------------------
# App UI
# -----------------------------
st.title("📊 News / Text Classifier — PCA vs Factor Analysis")

uploaded_file = st.file_uploader("Upload your dataset (CSV with 'text' + 'category/label')", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)
    st.success(f"✅ Dataset Loaded — {len(df)} rows")
    st.write("Columns:", df.columns)
    st.write(df.head())

    # -----------------------------
    # Vectorization
    # -----------------------------
    vectorizer = build_vectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['text'])
    y = df['category']

    # -----------------------------
    # Train-Test Split
    # -----------------------------
    test_size = st.slider("Test set size", min_value=0.1, max_value=0.5, value=0.2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # -----------------------------
    # Dimensionality Reduction Choice
    # -----------------------------
    reduction_method = st.selectbox("Choose Dimensionality Reduction", ["PCA", "Factor Analysis"])
    n_components = st.slider("Number of components", min_value=2, max_value=100, value=20)

    if reduction_method == "PCA":
        reducer = PCA(n_components=n_components)
    else:
        reducer = FactorAnalysis(n_components=n_components)

    X_train_reduced = reducer.fit_transform(X_train.toarray())
    X_test_reduced = reducer.transform(X_test.toarray())

    # -----------------------------
    # Train Classifier
    # -----------------------------
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_reduced, y_train)
    y_pred = clf.predict(X_test_reduced)

    # -----------------------------
    # Metrics
    # -----------------------------
    acc = accuracy_score(y_test, y_pred)
    st.write(f"### ✅ Accuracy ({reduction_method} + Logistic Regression): {acc*100:.2f}%")

    st.write("### Classification Report")
    st.text(classification_report(y_test, y_pred))

    st.write("### Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    st.pyplot(fig)

    # -----------------------------
    # Live Prediction
    # -----------------------------
    st.write("### 📝 Enter a news/article text to classify")
    live_text = st.text_area("Enter your text here")

    if st.button("Predict"):
        if live_text.strip() != "":
            live_vec = vectorizer.transform([live_text])
            live_reduced = reducer.transform(live_vec.toarray())
            live_pred = clf.predict(live_reduced)
            st.success(f"Predicted Category: {live_pred[0]}")
        else:
            st.warning("Please enter some text to classify.")

else:
    st.info("Please upload your dataset to start training and prediction.")
