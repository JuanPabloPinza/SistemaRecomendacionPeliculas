import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

peliculas = pickle.load(open("lista_peliculas.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

st.header("SISTEMA DE RECOMENDACIÓN DE PELÍCULAS")
st.header("CINEGENIUS")

lista_peliculas = peliculas['title'].values
selectvalue = st.selectbox("Por favor, selecciona una película", lista_peliculas)

def recomendar(pelicula):
    indice = peliculas[peliculas['title'] == pelicula].index[0]
    distancias = sorted(list(enumerate(similarity[indice])), reverse=True, key=lambda vector: vector[1])
    recomendadas = []
    portadas = []
    for i in distancias[1:6]:
        pelicula_id = peliculas.iloc[i[0]].id
        recomendadas.append(peliculas.iloc[i[0]].title)
        portadas.append(fetch_portadas(pelicula_id))
    return recomendadas, portadas

def fetch_portadas(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data:
            portada_dir = data['poster_path']
            dir_completa = f"https://image.tmdb.org/t/p/w500{portada_dir}"
            return dir_completa
        else:
            return "URL de la portada no disponible"
    except requests.exceptions.RequestException as e:
        return f"Error al obtener la portada: {e}"

if st.button("Mostrar Recomendaciones"):
    nombre_peli, poster_peli = recomendar(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(nombre_peli[0])
        st.image(poster_peli[0])
    with col2:
        st.text(nombre_peli[1])
        st.image(poster_peli[1])
    with col3:
        st.text(nombre_peli[2])
        st.image(poster_peli[2])
    with col4:
        st.text(nombre_peli[3])
        st.image(poster_peli[3])
    with col5:
        st.text(nombre_peli[4])
        st.image(poster_peli[4])
