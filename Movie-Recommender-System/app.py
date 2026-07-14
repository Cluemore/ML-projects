import streamlit as st
import pickle
import pandas as pd
import base64

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

movies_dict = pickle.load(open("moviesdict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("../../similarity.pkl", "rb"))

# RECOMMENDATION FUNCTION

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies

#banner

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

banner = get_base64("banner.jpg")

st.markdown(f"""
<style>

#css

#MainMenu {{
visibility:hidden;
}}

footer {{
visibility:hidden;
}}

header {{
visibility:hidden;
}}

.block-container {{
padding-top:2rem;
max-width:1200px;
}}

.hero {{

background-image:
linear-gradient(
rgba(0,0,0,0.65),
rgba(0,0,0,0.65)
),
url("data:image/jpeg;base64,{banner}");

background-size:cover;
background-position:center;
height:360px;

border-radius:18px;

display:flex;
justify-content:center;
align-items:center;
flex-direction:column;

margin-bottom:40px;
}}

.hero h1 {{

color:white;
font-size:56px;
font-weight:700;
margin-bottom:12px;

}}

.hero p {{

color:#f3f4f6;
font-size:20px;

}}

.stSelectbox label {{

font-size:18px;
font-weight:600;

}}

.stButton>button {{

width:100%;
height:55px;

background:#111827;
color:white;

border:none;
border-radius:10px;

font-size:18px;
font-weight:600;

}}

.stButton>button:hover {{

background:#374151;

}}

.movie-card {{

background:#ffffff;
border:1px solid #e5e7eb;
border-radius:12px;

padding:18px;

margin-bottom:16px;

box-shadow:0px 3px 10px rgba(0,0,0,0.08);

}}

.movie-title {{

font-size:18px;
font-weight:600;
color:#111827;

}}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <h1>Movie Recommender System</h1>
    <p>Discover movies similar to the ones you've already enjoyed.</p>
</div>
""", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

st.write("")

#recommendations

if st.button("Recommend Movies"):

    recommendations = recommend(selected_movie)

    st.markdown("### Recommended Movies")

    col1, col2 = st.columns(2)

    for i, movie in enumerate(recommendations):

        card = f"""
        <div class="movie-card">
            <div class="movie-title">{movie}</div>
        </div>
        """

        if i % 2 == 0:
            with col1:
                st.markdown(card, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(card, unsafe_allow_html=True)

st.divider()

import os
import gdown

FILE_ID = "1q3BKpQxn4WfJflimi0arLRg3S9KrF-js"

if not os.path.exists("../../similarity.pkl"):
    gdown.download(
        id=FILE_ID,
        output="similarity.pkl",
        quiet=False
    )
similarity = pickle.load(open("../../similarity.pkl", "rb"))