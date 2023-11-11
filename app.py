import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(
   page_title="Ex-stream-ly Cool App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMjdlYzNkNDYyNmRjNTc5OGI1YmQwNGY3Mzk2OGFiZiIsInN1YiI6IjYyZDNhMTQxMTU4Yzg1MDI5ZDU4YzFhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7QjyyKHDHBrh8cxKaPpG5tE3L_iaAqpBNm-GJJoG2KQ"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path

def recommend(movie):
    movie_index = movies_data[movies_data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        id = movies_data.iloc[i[0]].movie_id
        recommended_movies.append(movies_data.iloc[i[0]].title)
        # fetch poster from movie_id
        recommended_movies_posters.append(fetch_poster(id))

    return recommended_movies, recommended_movies_posters

movies_data = pickle.load(open('movies.pkl', 'rb'))
movies = movies_data['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Search for movie you loved watching',
    movies)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

