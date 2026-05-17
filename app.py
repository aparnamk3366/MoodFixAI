import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MoodFlix AI",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS (NETFLIX STYLE) ----------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* DARK OVERLAY (SOFT) */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.45);
    z-index: -1;
}

/* GLASS MAIN CONTAINER */
.main {
    background-color: rgba(20, 20, 20, 0.35);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 20px;
}

/* TITLE */
h1 {
    color: #ff4b4b;
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    text-shadow: 2px 2px 20px black;
}

/* SUBTITLE */
h3 {
    text-align: center;
    color: white;
    text-shadow: 1px 1px 10px black;
}

/* MOVIE CARD */
.movie-card {
    background-color: rgba(0,0,0,0.55);
    padding: 15px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 0px 15px rgba(255,75,75,0.3);
    transition: 0.3s;
}

.movie-card:hover {
    transform: scale(1.03);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    border: none;
    font-weight: bold;
}

/* TEXT */
p, label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>🎬 MoodFlix AI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Netflix-style Emotion Based Movie Recommender</h3>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
movies = pd.read_csv("tmdb_5000_movies.csv")

# keep needed columns safely
required_cols = ['title', 'genres', 'overview', 'vote_average']
if 'poster_path' in movies.columns:
    required_cols.append('poster_path')

movies = movies[required_cols]
movies.dropna(inplace=True)

# ---------------- MOOD FUNCTION ----------------
def get_mood_keywords(mood):
    mood = mood.lower()

    if "happy" in mood or "good" in mood or "excited" in mood:
        return ["comedy", "family", "romance"]
    elif "sad" in mood or "lonely" in mood:
        return ["drama", "romance"]
    elif "angry" in mood or "stress" in mood:
        return ["action", "thriller"]
    elif "bored" in mood:
        return ["adventure", "comedy"]
    else:
        return ["drama", "action"]

# ---------------- UI INPUT ----------------
mood = st.selectbox(
    "🎭 How are you feeling today?",
    ["Happy 😊", "Sad 😢", "Angry 😡", "Bored 😐", "Excited 🤩", "Neutral"]
)

# ---------------- RECOMMEND BUTTON ----------------
if st.button("🍿 Get My Recommendations"):

    keywords = get_mood_keywords(mood)

    def match_genre(genres):
        return any(k in genres.lower() for k in keywords)

    filtered = movies[movies["genres"].apply(match_genre)]

    if filtered.empty:
        filtered = movies

    top_movies = filtered.sort_values(
        by="vote_average",
        ascending=False
    ).head(12)

    st.success(f"Top picks for your mood: {mood}")

    # ---------------- NETFLIX STYLE GRID ----------------
    cols = st.columns(3)

    TMDB_IMG = "https://image.tmdb.org/t/p/w500"

    for i, (_, row) in enumerate(top_movies.iterrows()):

        with cols[i % 3]:

            poster = ""
            if "poster_path" in row and pd.notna(row["poster_path"]):
                poster = TMDB_IMG + row["poster_path"]
            else:
                poster = "https://via.placeholder.com/300x450?text=No+Image"

            st.markdown(f"""
                <div class="movie-card">
                    <img src="{poster}" style="width:100%; border-radius:12px;">
                    <h3 style="text-align:center;">{row['title']}</h3>
                    <p>⭐ Rating: {row['vote_average']}</p>
                    <p style="font-size:13px;">{row['overview'][:120]}...</p>
                </div>
            """, unsafe_allow_html=True)
            