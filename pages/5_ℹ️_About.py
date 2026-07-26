import streamlit as st
import pandas as pd

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
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

st.title("ℹ️ About the Project")

st.markdown("""
Welcome to the **Movie Recommendation System**, a content-based recommendation application
developed using **Natural Language Processing (NLP)**, **Machine Learning**, and **Streamlit**.

The project demonstrates how different recommendation algorithms can be used to suggest
similar movies based on their content, while also allowing users to compare the strengths
of multiple recommendation techniques through an interactive interface.
""")

st.divider()

st.header("🎯 Project Objectives")

col1, col2 = st.columns(2)

with col1:

    st.success("""
- Build a Content-Based Movie Recommendation System
- Compare multiple NLP models
- Demonstrate Machine Learning concepts
- Create an interactive Streamlit application
""")

with col2:

    st.success("""
- Explore movie metadata
- Visualize dataset insights
- Compare recommendation quality
- Deliver a user-friendly experience
""")

st.divider()

st.header("⚙️ Technologies Used")

tech = pd.DataFrame({
    "Category": [
        "Programming Language",
        "Framework",
        "Machine Learning",
        "Natural Language Processing",
        "Deep Learning",
        "Similarity Measure",
        "Data Processing",
        "Visualization",
        "Model Storage"
    ],

    "Technology": [
        "Python",
        "Streamlit",
        "Scikit-learn",
        "CountVectorizer, TF-IDF",
        "Sentence-BERT",
        "Cosine Similarity",
        "Pandas, NumPy",
        "Matplotlib, Plotly",
        "Pickle, SciPy (.npz)"
    ]
})

st.dataframe(
    tech,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.header("🧠 Recommendation Pipeline")

st.markdown("""
```text
Movie Dataset
      │
      ▼
Data Cleaning & Preprocessing
      │
      ▼
Feature Engineering
      │
      ▼
Vector Representation
(CountVectorizer / TF-IDF / Sentence-BERT)
      │
      ▼
Cosine Similarity
      │
      ▼
Top-N Movie Recommendations
""")

st.divider()

st.header("✨ Key Features")

left, right = st.columns(2)

with left:

    st.info("""
### Recommendation Engine

- Content-Based Filtering
- Three Recommendation Models
- Semantic Movie Search
- Similarity-Based Ranking
""")

with right:

    st.info("""
### Interactive Dashboard

- Dataset Exploration
- Analytics Dashboard
- Model Comparison
- Modern Streamlit Interface
""")

st.divider()

st.header("👨‍💻 Developer")

st.markdown("""
### Sahibdeep Singh

**Bachelor of Technology (Computer Science & Engineering)**

Guru Nanak Dev Engineering College, Ludhiana

---

**Areas of Interest**

- Artificial Intelligence
- Machine Learning
- Data Science
- Full-Stack Web Development
- Natural Language Processing

---

This project was developed to explore modern recommendation systems by comparing traditional NLP techniques with transformer-based semantic embeddings through an interactive and user-friendly application.
""")

st.divider()

st.header("Acknowledgements")

st.markdown("""
This project makes use of publicly available movie metadata for educational and research purposes.

Special thanks to the open-source community and the developers of:

- Streamlit
- Scikit-learn
- Sentence-Transformers
- Pandas
- NumPy
- SciPy
- Matplotlib
- Plotly

Their tools and libraries made the development of this application possible.
""")

st.divider()

st.markdown(
"""
<div style="text-align:center; color:gray; padding:20px;">

<h4>Movie Recommendation System</h4>

Content-Based Recommendation using Machine Learning

Thank You.

<br>

2026 Sahibdeep Singh

</div>
""",
unsafe_allow_html=True
)