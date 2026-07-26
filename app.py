import streamlit as st

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Load CSS
# ---------------------------------------------------

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# Hero Section
# ---------------------------------------------------

st.markdown("""
<div class='hero'>
<h1>🎬 Movie Recommendation System</h1>
<p>
An AI-powered movie recommendation platform built using Natural Language Processing,
Machine Learning, and Interactive Data Analytics.
</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Project Statistics
# ---------------------------------------------------

st.subheader("📊 Project Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎬 Movies", "45K+")

with col2:
    st.metric("🤖 Models", "3")

with col3:
    st.metric("🧠 Embedding Size", "384")

with col4:
    st.metric("📈 Analytics", "8+")

st.divider()

# ---------------------------------------------------
# Features
# ---------------------------------------------------

st.subheader("🚀 Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### 🎬 Movie Recommender

- Sentence-BERT Recommendations
- TF-IDF Recommendations
- CountVectorizer Recommendations
- Movie Metadata
- Similarity Scores

### 📊 Analytics Dashboard

- Genre Analysis
- Director Analysis
- Rating Distribution
- Production Trends
- Popularity Analysis
""")

with col2:
    st.markdown("""
### 📚 Dataset Explorer

- Browse Dataset
- Search Movies
- Filter Records
- Interactive Table
- Dataset Statistics

### 🤖 Model Comparison

- Compare Recommendation Models
- Side-by-Side Results
- Similarity Comparison
- Recommendation Quality
""")

st.divider()

# ---------------------------------------------------
# Technology Stack
# ---------------------------------------------------

st.subheader("🛠 Technology Stack")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.info("""
**Frontend**

- Streamlit
- HTML
- CSS
""")

with tech2:
    st.info("""
**Machine Learning**

- Sentence-BERT
- TF-IDF
- CountVectorizer
""")

with tech3:
    st.info("""
**Libraries**

- Pandas
- NumPy
- Scikit-Learn
""")

with tech4:
    st.info("""
**Dataset**

- The Movies Dataset
- 45,000+ Movies
- TMDB Metadata
""")

st.divider()

# ---------------------------------------------------
# Project Pages
# ---------------------------------------------------

st.subheader("📂 Project Modules")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.success("🎬\n\nRecommender")

with col2:
    st.success("📊\n\nAnalytics")

with col3:
    st.success("📚\n\nDataset")

with col4:
    st.success("🤖\n\nModels")

with col5:
    st.success("ℹ️\n\nAbout")

st.divider()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown(
    """
<div style="text-align:center; color:gray; padding:20px;">
<b>Movie Recommendation System</b><br>
Developed by <b>Sahibdeep Singh</b><br>
B.Tech Computer Science & Engineering
</div>
""",
    unsafe_allow_html=True
)