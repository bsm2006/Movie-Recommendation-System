import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from recommender import df_master

# ---------------------------------------------------
# Load CSS
# ---------------------------------------------------

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------

st.title("📊 Analytics Dashboard")

st.markdown("""
Explore insights from **45,000+ movies** using interactive visualizations,
statistical summaries, and trend analysis.
""")

st.divider()

# =====================================================
# Dashboard Statistics
# =====================================================

total_movies = len(df_master)

total_genres = (
    df_master["primary_genre"]
    .dropna()
    .nunique()
)

total_directors = (
    df_master["director"]
    .replace("Unknown", np.nan)
    .dropna()
    .nunique()
)

avg_rating = (
    df_master.loc[
        df_master["vote_count"] > 0,
        "vote_average"
    ]
    .mean()
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "🎬 Movies",
        f"{total_movies:,}"
    )

with c2:
    st.metric(
        "🎭 Genres",
        total_genres
    )

with c3:
    st.metric(
        "🎬 Directors",
        total_directors
    )

with c4:
    st.metric(
        "⭐ Avg Rating",
        f"{avg_rating:.2f}"
    )

st.divider()

# =====================================================
# Theme Constants
# =====================================================

PRIMARY_COLOR = "#2a658a"
BAR_EDGE = "#1d4257"

FIG_SIZE = (15, 8)

TITLE_SIZE = 18
LABEL_SIZE = 12
VALUE_SIZE = 11

GRID_ALPHA = 0.30

# =====================================================
# Genre Insights
# =====================================================

st.subheader("Top Genres")

genre_counts = (
        df_master["primary_genre"]
        .value_counts()
        .head(10)
        .sort_values()
    )

fig, ax = plt.subplots(figsize=FIG_SIZE)

bars = ax.barh(
        genre_counts.index,
        genre_counts.values,
        color=PRIMARY_COLOR,
        edgecolor=BAR_EDGE
    )

ax.set_title(
        "Top 10 Genres",
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

ax.set_xlabel(
        "Number of Movies",
        fontsize=LABEL_SIZE
    )

ax.grid(
        axis="x",
        alpha=GRID_ALPHA
    )

for bar in bars:

        width = bar.get_width()

        ax.text(
            width + 50,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}",
            va="center",
            fontsize=VALUE_SIZE
        )

sns.despine()

st.pyplot(fig)

# =====================================================
# Average Rating by Genre (Lollipop Chart)
# =====================================================

st.subheader("Average Rating by Genre")

genre_stats = (
        df_master[
            (df_master["vote_average"] > 0)
            &
            (df_master["vote_count"] > 0)
        ]
        .groupby("primary_genre")
        .agg(
            Average_Rating=("vote_average", "mean"),
            Movie_Count=("primary_genre", "count")
        )
        .query("Movie_Count >= 50")
        .sort_values("Average_Rating", ascending=True)
    )

fig, ax = plt.subplots(figsize=FIG_SIZE)

ax.hlines(
        y=genre_stats.index,
        xmin=0,
        xmax=genre_stats["Average_Rating"],
        color="lightgray",
        linewidth=2
    )

ax.scatter(
        genre_stats["Average_Rating"],
        genre_stats.index,
        s=120,
        color=PRIMARY_COLOR,
        edgecolor=BAR_EDGE,
        zorder=3
    )

for rating, genre in zip(
        genre_stats["Average_Rating"],
        genre_stats.index
    ):

        ax.text(
            rating + 0.03,
            genre,
            f"{rating:.2f}",
            va="center",
            fontsize=VALUE_SIZE
        )

ax.set_title(
        "Average Rating by Genre",
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

ax.set_xlabel(
        "Average Rating",
        fontsize=LABEL_SIZE
    )

ax.grid(
        axis="x",
        alpha=GRID_ALPHA
    )

sns.despine()

st.pyplot(fig)

st.divider()

# =====================================================
# Director Insights
# =====================================================

st.header("🎬 Director Insights")


# =====================================================
# Top Directors
# =====================================================


director_counts = (
        df_master[df_master["director"] != "Unknown"]["director"]
        .value_counts()
        .head(10)
        .sort_values()
    )

fig, ax = plt.subplots(figsize=FIG_SIZE)

bars = ax.barh(
        director_counts.index,
        director_counts.values,
        color=PRIMARY_COLOR,
        edgecolor=BAR_EDGE
    )

ax.set_title(
        "Top Directors by Number of Movies",
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

ax.set_xlabel(
        "Movies Directed",
        fontsize=LABEL_SIZE
    )

ax.grid(
        axis="x",
        alpha=GRID_ALPHA
    )

for bar in bars:

        width = bar.get_width()

        ax.text(
            width + 0.2,
            bar.get_y() + bar.get_height()/2,
            f"{int(width)}",
            va="center",
            fontsize=VALUE_SIZE
        )

sns.despine()

st.pyplot(fig)

# =====================================================
# Director Performance (Bubble Plot)
# =====================================================

st.header("🎬 Director Performance")

director_stats = (
        df_master[
            (df_master["director"] != "Unknown") &
            (df_master["vote_average"] > 0) &
            (df_master["vote_count"] > 0)
        ]
        .groupby("director")
        .agg(
            Average_Rating=("vote_average", "mean"),
            Movie_Count=("director", "count")
        )
        .query("Movie_Count >= 3")
        .sort_values("Average_Rating", ascending=False)
        .head(10)
    )

fig, ax = plt.subplots(figsize=FIG_SIZE)

sns.scatterplot(
        data=director_stats,
        x="Average_Rating",
        y=director_stats.index,
        size="Movie_Count",
        sizes=(200, 900),
        legend=False,
        color=PRIMARY_COLOR,
        edgecolor=BAR_EDGE,
        ax=ax
    )

for rating, director in zip(
        director_stats["Average_Rating"],
        director_stats.index
    ):
        ax.text(
            rating + 0.02,
            director,
            f"{rating:.2f}",
            va="center",
            fontsize=VALUE_SIZE
        )

ax.set_title(
        "Top Directors by Average Rating",
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

ax.set_xlabel(
        "Average Rating",
        fontsize=LABEL_SIZE
    )

ax.set_ylabel("")

ax.grid(
        axis="x",
        alpha=GRID_ALPHA
    )

sns.despine()

st.pyplot(fig)

st.divider()

# =====================================================
# Movie Trends
# =====================================================

st.header("📈 Movie Production Trends")

# =====================================================
# Movies by Decade
# =====================================================

decade_counts = (
        df_master["decade"]
        .dropna()
        .value_counts()
        .sort_index()
    )

fig, ax = plt.subplots(figsize=FIG_SIZE)

ax.plot(
        decade_counts.index.astype(str),
        decade_counts.values,
        marker="o",
        linewidth=3,
        color=PRIMARY_COLOR
    )

ax.fill_between(
        range(len(decade_counts)),
        decade_counts.values,
        alpha=0.20,
        color=PRIMARY_COLOR
    )

ax.set_title(
        "Movie Production Trend",
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

ax.set_xlabel(
        "Decade",
        fontsize=LABEL_SIZE
    )

ax.set_ylabel(
        "Movies",
        fontsize=LABEL_SIZE
    )

ax.grid(alpha=GRID_ALPHA)

sns.despine()

st.pyplot(fig)

# =====================================================
# Rating Distribution
# =====================================================

st.header(" Rating Distribution")

ratings = df_master[
        (df_master["vote_average"] > 0) &
        (df_master["vote_count"] > 0)
    ]["vote_average"]

fig, ax = plt.subplots(figsize=FIG_SIZE)

ax.hist(
        ratings,
        bins=20,
        edgecolor="black"
    )

ax.set_title(
        "Rating Distribution",
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

ax.set_xlabel(
        "TMDB Rating",
        fontsize=LABEL_SIZE
    )

ax.set_ylabel(
        "Number of Movies",
        fontsize=LABEL_SIZE
    )

ax.grid(alpha=GRID_ALPHA)

sns.despine()

st.pyplot(fig)

st.divider()

# =====================================================
# Ratings vs Vote Count
# =====================================================

st.header("⭐ Ratings & Popularity")

ratings_df = df_master[
    (df_master["vote_average"] > 0) &
    (df_master["vote_count"] > 0)
]

fig, ax = plt.subplots(figsize=(12,7))

ax.scatter(
    ratings_df["vote_count"],
    ratings_df["vote_average"],
    alpha=0.45,
    s=20
)

ax.set_xscale("log")

ax.set_title(
    "Ratings vs Vote Count",
    fontsize=TITLE_SIZE,
    fontweight="bold"
)

ax.set_xlabel(
    "Vote Count (Log Scale)",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Average Rating",
    fontsize=LABEL_SIZE
)

ax.grid(alpha=GRID_ALPHA)

sns.despine()

st.pyplot(fig)

st.divider()

# =====================================================
# Hall of Fame
# =====================================================

st.header("🏆 Hall of Fame")

hall_of_fame = (
    df_master[
        (df_master["vote_average"] > 0) &
        (df_master["vote_count"] >= 1000)
    ]
    .sort_values(
        ["vote_average", "vote_count"],
        ascending=False
    )
    .head(10)
)

medals = [
    "🥇",
    "🥈",
    "🥉"
]

for i, (_, movie) in enumerate(hall_of_fame.iterrows()):

    if i < 3:
        icon = medals[i]
    else:
        icon = f"#{i+1}"

    with st.container(border=True):

        left, right = st.columns([5,1])

        with left:

            st.markdown(
                f"### {icon} {movie['title']}"
            )

            st.write(
                f"🎭 **Genre:** {movie['primary_genre']}"
            )

            st.write(
                f"📅 **Year:** {int(movie['release_year'])}"
            )

            st.write(
                f"🎬 **Director:** {movie['director']}"
            )

        with right:

            st.metric(
                "⭐ Rating",
                f"{movie['vote_average']:.2f}"
            )

            st.metric(
                "👥 Votes",
                f"{int(movie['vote_count']):,}"
            )

st.divider()

st.caption(
    "Movie analytics generated from The Movies Dataset using Pandas, Matplotlib and Streamlit."
)