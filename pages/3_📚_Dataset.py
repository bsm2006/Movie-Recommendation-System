import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from recommender import df_master

# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="Dataset",
    page_icon="📚",
    layout="wide"
)

# =====================================================
# Title
# =====================================================

st.title("📚 Movie Dataset Explorer")

st.markdown(
    """
Explore the dataset powering the Movie Recommendation System.
This page provides an overview of the dataset, feature descriptions,
statistics, missing values, and interactive search capabilities.
"""
)

st.divider()

# =====================================================
# Dataset Overview
# =====================================================

st.header("📈 Dataset Overview")

total_movies = len(df_master)
total_features = df_master.shape[1]

year_min = int(df_master["release_year"].min())
year_max = int(df_master["release_year"].max())

total_genres = df_master["primary_genre"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🎬 Movies",
    f"{total_movies:,}"
)

col2.metric(
    "📋 Features",
    total_features
)

col3.metric(
    "📅 Year Range",
    f"{year_min} – {year_max}"
)

col4.metric(
    "🎭 Genres",
    total_genres
)

st.divider()

# =====================================================
# Feature Summary
# =====================================================

st.header("📋 Feature Summary")

feature_info = pd.DataFrame({
    "Feature": [
        "title",
        "release_year",
        "primary_genre",
        "overview",
        "director",
        "cast",
        "vote_average",
        "vote_count",
        "popularity",
        "runtime"
    ],

    "Data Type": [
        str(df_master["title"].dtype),
        str(df_master["release_year"].dtype),
        str(df_master["primary_genre"].dtype),
        str(df_master["overview"].dtype),
        str(df_master["director"].dtype),
        str(df_master["cast"].dtype),
        str(df_master["vote_average"].dtype),
        str(df_master["vote_count"].dtype),
        str(df_master["popularity"].dtype),
        str(df_master["runtime"].dtype)
    ],

    "Description": [
        "Movie title",
        "Release year",
        "Primary movie genre",
        "Movie synopsis",
        "Director name",
        "Main cast",
        "Average TMDB rating",
        "Total user votes",
        "Popularity score",
        "Runtime (minutes)"
    ]
})

st.dataframe(
    feature_info,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================================
# Dataset Information
# =====================================================

st.header("🗂 Dataset Information")

left, right = st.columns([1,1])

with left:

    st.subheader("Dataset Dimensions")

    st.info(
        f"""
Rows : **{df_master.shape[0]:,}**

Columns : **{df_master.shape[1]}**
"""
    )

with right:

    memory = df_master.memory_usage(deep=True).sum() / (1024**2)

    st.subheader("Memory Usage")

    st.info(
        f"""
Approximate Memory Usage

**{memory:.2f} MB**
"""
    )

st.divider()

# =====================================================
# Interactive Dataset
# =====================================================

st.header("🗃 Interactive Dataset")

rows = st.slider(
    "Number of rows to display",
    min_value=5,
    max_value=100,
    value=10,
    step=5
)

st.dataframe(
    df_master.head(rows),
    use_container_width=True,
    height=450
)

st.divider()

# =====================================================
# Missing Values Analysis
# =====================================================

st.header("🩺 Missing Values Analysis")

missing = (
    df_master.isnull()
    .sum()
    .sort_values(ascending=False)
)

missing = missing[missing > 0]

if missing.empty:

    st.success("✅ No missing values found in the dataset.")

else:

    fig, ax = plt.subplots(figsize=(14,6))

    bars = ax.barh(
        missing.index[::-1],
        missing.values[::-1]
    )

    ax.set_title(
        "Missing Values by Feature",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Missing Values")

    ax.grid(axis="x", alpha=0.3)

    for bar in bars:

        width = bar.get_width()

        ax.text(
            width + 10,
            bar.get_y() + bar.get_height()/2,
            f"{int(width):,}",
            va="center"
        )

    st.pyplot(fig, use_container_width=True)

st.divider()

# =====================================================
# Dataset Statistics
# =====================================================

st.header("📊 Statistical Summary")

stats_option = st.radio(
    "Choose Summary",
    [
        "Numerical Features",
        "Complete Dataset"
    ],
    horizontal=True
)

if stats_option == "Numerical Features":

    st.dataframe(
        df_master.describe(),
        use_container_width=True
    )

else:

    st.dataframe(
        df_master.describe(include="all"),
        use_container_width=True
    )

st.divider()

# =====================================================
# Search Dataset
# =====================================================

st.header("🔍 Search Dataset")

movie_name = st.text_input(
    "Search by Movie Title",
    placeholder="e.g. Inception"
)

if movie_name:

    results = df_master[
        df_master["title"].str.contains(
            movie_name,
            case=False,
            na=False
        )
    ]

    if results.empty:

        st.warning("No matching movie found.")

    else:

        st.success(f"{len(results)} movie(s) found.")

        st.dataframe(
            results[
                [
                    "title",
                    "release_year",
                    "primary_genre",
                    "vote_average",
                    "director"
                ]
            ],
            use_container_width=True
        )

st.divider()

# =====================================================
# Random Movie Explorer
# =====================================================

st.header("🎲 Random Movie Explorer")

if st.button("🎬 Show Random Movie"):

    movie = df_master.sample(1).iloc[0]

    st.subheader(movie["title"])

    left, right = st.columns([2,1])

    with left:

        st.write(f"**📅 Release Year:** {int(movie['release_year'])}")
        st.write(f"**🎭 Genre:** {movie['primary_genre']}")
        st.write(f"**🎬 Director:** {movie['director']}")
        st.write(f"**⭐ Rating:** {movie['vote_average']:.2f}")
        st.write(f"**👥 Votes:** {int(movie['vote_count']):,}")

    with right:

        st.metric(
            "Popularity",
            f"{movie['popularity']:.1f}"
        )

    st.markdown("### 📝 Overview")

    st.write(movie["overview"])

st.divider()

# =====================================================
# Data Dictionary
# =====================================================

st.header("📖 Data Dictionary")

descriptions = {
    "title":"Movie title",
    "release_year":"Year of release",
    "primary_genre":"Primary genre",
    "overview":"Movie synopsis",
    "director":"Director name",
    "cast":"Lead cast",
    "vote_average":"Average TMDB rating",
    "vote_count":"Total votes received",
    "popularity":"TMDB popularity score",
    "runtime":"Movie duration in minutes"
}

dictionary = pd.DataFrame({
    "Column": df_master.columns,
    "Data Type": [str(df_master[col].dtype) for col in df_master.columns],
    "Description": [
        descriptions.get(col, "No description available")
        for col in df_master.columns
    ]
})

st.dataframe(
    dictionary,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption(
    "Dataset used for building the Movie Recommendation System."
)
