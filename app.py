import streamlit as st
import pandas as pd
import joblib
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import requests
from bs4 import BeautifulSoup

# ------------------Cosas visuales------------------------
st.image('MERKLE2x.png')
st.title('MERKLE -equipo 4')
a = st.radio('Analizar noticia desde:',["URL","Texto"])

#------------ Cargar archivos ---------------------
# Cargar el DataFrame con los nombres de los clusters
df_clusters = pd.read_csv('df_muestras_cluster.csv')
# Cargar el modelo KMeans y el vectorizador TF-IDF
modelo_kmeans = joblib.load('modelo_kmeans.joblib')
vectorizador = joblib.load('vectorizador_modelo.joblib')

# Función para preprocesar el texto de la noticia
def preprocess_text(text):
    # Convertir el texto a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales, números y signos de puntuación
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenización (dividir el texto en palabras)
    words = text.split()
    # Unir las palabras preprocesadas nuevamente en una cadena
    preprocessed_text = ' '.join(words)
    return preprocessed_text

# Función para predecir el clúster de la noticia y obtener su nombre
def predict_cluster_with_label(noticia):
    # Preprocesar la noticia
    noticia_procesada = preprocess_text(noticia)
    # Vectorizar la noticia
    noticia_vectorizada = vectorizador.transform([noticia_procesada])
    # Predecir el clúster
    cluster_predicho = modelo_kmeans.predict(noticia_vectorizada)[0]
    # Obtener el nombre del clúster
    nombre_cluster = df_clusters[df_clusters['id'] == cluster_predicho]['cluster_etiqueta'].values[0]
    return nombre_cluster

# Función para obtener el texto de una noticia a partir de una URL
def get_text_from_url(url):
    try:
        # Obtener el contenido HTML de la URL
        response = requests.get(url)
        # Parsear el HTML usando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Encontrar y extraer el texto relevante de la noticia
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text
    except Exception as e:
        print(f"Error al obtener el texto de la URL: {e}")
        return None


#--------------------- Funcionamiento del programa -------------------------
# si se ha elegido analizar desde URL
if a == "URL":
    url_noticia=st.text_input("Introduce la dirección web de la noticia")
    if st.button('Clasificar la noticia:'):
        if url_noticia:
            # Obtener el texto de la noticia desde la URL
            texto_noticia = get_text_from_url(url_noticia)
            if texto_noticia:
                # Predecir el clúster de la noticia
                nombre_cluster_predicho = predict_cluster_with_label(texto_noticia)
                st.write(f'El clúster predicho para la noticia es: {nombre_cluster_predicho}')
            else:
                st.write("No se pudo obtener el texto de la URL proporcionada.")
        else:
            st.write("Por favor, introduce una URL válida.")
else: # si se ha elegido analizar desde texto
    noticia_input = st.text_area("Introduce el texto de la noticia", "Pon aquí el texto de la noticia")
    if st.button('Clasificar la noticia:'):
        # Predecir el clúster de la noticia
        nombre_cluster_predicho = predict_cluster_with_label(noticia_input)
        st.write(f'El clúster predicho para la noticia es: {nombre_cluster_predicho}')

