import pickle
import numpy as np

from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity


# ----------------------------
# Load Resources
# ----------------------------

with open("models/movie_data.pkl", "rb") as f:
    df_master = pickle.load(f)

with open("models/movie_index.pkl", "rb") as f:
    movie_index = pickle.load(f)

with open("models/count_vectorizer.pkl", "rb") as f:
    cv = pickle.load(f)

with open("models/tfidf_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

count_vectors = load_npz("models/count_vectors.npz")
tfidf_vectors = load_npz("models/tfidf_vectors.npz")

embeddings = np.load("models/bert_embeddings.npy")

def search_movies(query):

    return df_master[
        df_master["movie_key"]
        .str.contains(query, case=False, na=False)
    ]["movie_key"].tolist()


def recommend_bert(movie_key, top_n=10):

    if movie_key not in movie_index.index:
        raise ValueError(f"Movie '{movie_key}' not found.")

    idx = movie_index[movie_key]

    sim = cosine_similarity(
        embeddings[idx].reshape(1, -1),
        embeddings
    ).flatten()

    indices = sim.argsort()[::-1][1:top_n+1]

    result = df_master.iloc[indices][
        [
            "movie_key",
            "title",
            "release_year",
            "primary_genre"
        ]
    ].copy()

    result["Similarity"] = sim[indices]

    return result


def recommend_tfidf(movie_key, top_n=10):

    if movie_key not in movie_index.index:
        raise ValueError(f"Movie '{movie_key}' not found.")

    idx = movie_index[movie_key]

    sim = cosine_similarity(
        tfidf_vectors[idx],
        tfidf_vectors
    ).flatten()

    indices = sim.argsort()[::-1][1:top_n+1]

    result = df_master.iloc[indices][
        [
            "movie_key",
            "title",
            "release_year",
            "primary_genre"
        ]
    ].copy()

    result["Similarity"] = sim[indices]

    return result


def recommend_count(movie_key, top_n=10):

    if movie_key not in movie_index.index:
        raise ValueError(f"Movie '{movie_key}' not found.")

    idx = movie_index[movie_key]

    sim = cosine_similarity(
        count_vectors[idx],
        count_vectors
    ).flatten()

    indices = sim.argsort()[::-1][1:top_n+1]

    result = df_master.iloc[indices][
        [
            "movie_key",
            "title",
            "release_year",
            "primary_genre"
        ]
    ].copy()

    result["Similarity"] = sim[indices]

    return result


