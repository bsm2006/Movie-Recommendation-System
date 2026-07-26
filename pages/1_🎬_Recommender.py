import streamlit as st
import pandas as pd

from recommender import (
    df_master,
    recommend_bert,
    recommend_count,
    recommend_tfidf
)
__all__ = [
    "recommend_count",
    "recommend_tfidf",
    "recommend_bert",
    "movie_index",
    "df_master"
]
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
Discover similar movies using advanced Natural Language Processing
and Machine Learning techniques.
</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Dataset Metrics
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎬 Movies", f"{len(df_master):,}")

with col2:
    st.metric("🤖 Models", "3")

with col3:
    st.metric("🧠 Embedding Size", "384")

with col4:
    st.metric("📂 Dataset", "45K+")

st.divider()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("🎬 Movie Explorer")

st.sidebar.markdown(
    """
Select a movie and choose a recommendation model
to discover similar movies.
"""
)

movie_list = (
    df_master["movie_key"]
    .dropna()
    .astype(str)
    .sort_values()
    .unique()
)

movie = st.sidebar.selectbox(
    "🎬 Search Movie",
    movie_list
)

model = st.sidebar.radio(
    "Recommendation Model",
    [
        "Sentence-BERT",
        "TF-IDF",
        "CountVectorizer"
    ]
)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    min_value=5,
    max_value=20,
    value=10
)

recommend_btn = st.sidebar.button(
    "🚀 Recommend Movies",
    use_container_width=True
)

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "movie" not in st.session_state:
    st.session_state.movie = None

if "selected" not in st.session_state:
    st.session_state.selected = None

if "result" not in st.session_state:
    st.session_state.result = None

# ---------------------------------------------------
# Generate Recommendations
# ---------------------------------------------------

if recommend_btn:

    if model == "Sentence-BERT":
        result = recommend_bert(movie, top_n)

    elif model == "TF-IDF":
        result = recommend_tfidf(movie, top_n)

    else:
        result = recommend_count(movie, top_n)

    selected = df_master[
        df_master["movie_key"] == movie
    ].iloc[0]

    st.session_state.movie = movie
    st.session_state.result = result
    st.session_state.selected = selected

# ---------------------------------------------------
# Wait Until Recommendation
# ---------------------------------------------------

if st.session_state.result is None:

    st.info(
        "👈 Select a movie from the sidebar and click **Recommend Movies**."
    )

    st.stop()

# ---------------------------------------------------
# Retrieve Session Data
# ---------------------------------------------------

movie = st.session_state.movie
selected = st.session_state.selected
result = st.session_state.result

# =====================================================
# SELECTED MOVIE
# =====================================================

st.subheader("🎬 Selected Movie")

st.markdown(f"## {selected['title']}")

# ---------------------------------------------------
# Movie Metrics
# ---------------------------------------------------

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "🎭 Genre",
        selected["primary_genre"]
    )

with metric2:

    year = selected["release_year"]

    if pd.notna(year):
        st.metric(
            "📅 Release Year",
            int(year)
        )
    else:
        st.metric(
            "📅 Release Year",
            "N/A"
        )

with metric3:

    rating = selected["vote_average"]

    if pd.notna(rating):
        st.metric(
            "⭐ TMDB Rating",
            f"{float(rating):.1f}/10"
        )
    else:
        st.metric(
            "⭐ TMDB Rating",
            "N/A"
        )

# ---------------------------------------------------
# Director
# ---------------------------------------------------

director = selected["director"]

if pd.notna(director) and str(director).strip():

    st.markdown(
        f"**🎬 Director:** {director}"
    )

else:

    st.markdown(
        "**🎬 Director:** N/A"
    )

# ---------------------------------------------------
# Cast
# ---------------------------------------------------

cast = selected["cast"]

if isinstance(cast, list) and len(cast) > 0:

    st.markdown(
        f"**👥 Cast:** {', '.join(cast[:5])}"
    )

elif pd.notna(cast) and str(cast).strip():

    st.markdown(
        f"**👥 Cast:** {cast}"
    )

else:

    st.markdown(
        "**👥 Cast:** N/A"
    )

# ---------------------------------------------------
# Overview
# ---------------------------------------------------

st.markdown("### 📝 Overview")

overview = selected["overview"]

if pd.isna(overview) or str(overview).strip() == "":

    st.info(
        "Overview not available."
    )

else:

    st.write(overview)

st.divider()

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.subheader("⭐ Recommended Movies")

cols = st.columns(3)

for i, (_, row) in enumerate(result.iterrows()):

    similarity = float(row["Similarity"]) * 100

    movie_data = df_master[
        df_master["title"] == row["title"]
    ]

    if movie_data.empty:
        continue

    movie_data = movie_data.iloc[0]

    with cols[i % 3]:

        rating = movie_data["vote_average"]

        if pd.notna(rating):
            rating_text = f"{float(rating):.1f}/10"
        else:
            rating_text = "N/A"

        st.markdown(
            f"""
<div class="movie-card">

<h4>{movie_data['title']}</h4>

<p>🎭 {movie_data['primary_genre']}</p>

<p>📅 {movie_data['release_year']}</p>

<p>⭐ {rating_text}</p>

</div>
""",
            unsafe_allow_html=True
        )

        st.progress(similarity / 100)

        st.caption(
            f"Similarity Score: {similarity:.1f}%"
        )

st.divider()

# =====================================================
# MODEL INFORMATION
# =====================================================

st.subheader("🧠 How This Recommendation Works")

if model == "Sentence-BERT":

    st.info("""
### 🧠 Sentence-BERT

Sentence-BERT converts each movie into a dense semantic embedding.

Instead of simply matching keywords, it understands the contextual meaning of movie plots, genres and descriptions. Recommendations are generated using cosine similarity between embedding vectors.

**Advantages**

- Understands semantic meaning
- Produces high-quality recommendations
- Captures contextual relationships
- Less affected by wording differences

**Best Use Case**

Finding movies with similar stories or themes, even when they use different vocabulary.
""")

elif model == "TF-IDF":

    st.info("""
### 📄 TF-IDF

TF-IDF represents each movie as a weighted collection of important words.

Movies sharing distinctive terms receive higher similarity scores. Common words contribute less to the recommendation process.

**Advantages**

- Fast and lightweight
- Easy to interpret
- Strong performance on textual metadata

**Best Use Case**

Finding movies with similar descriptions and overlapping keywords.
""")

else:

    st.info("""
### 🔤 CountVectorizer

CountVectorizer converts movie descriptions into simple word-frequency vectors.

Recommendations are based on the number of common words shared between movies.

**Advantages**

- Extremely fast
- Computationally inexpensive
- Good baseline model

**Best Use Case**

Basic content-based recommendation using keyword frequency.
""")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.divider()

footer_col1, footer_col2 = st.columns([3, 1])

with footer_col1:

    st.caption(
        f"""
Current Recommendation Model: **{model}**

Recommendations Generated: **{len(result)}**
"""
    )

with footer_col2:

    st.metric(
        "Top N",
        top_n
    )

st.markdown(
    """
<div style="text-align:center;
            color:gray;
            padding:20px 0;">

<b>Movie Recommendation System</b><br>

Powered by NLP, Machine Learning & Streamlit

<br><br>

© 2026 Sahibdeep Singh

</div>
""",
    unsafe_allow_html=True
)