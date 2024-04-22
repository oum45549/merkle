import streamlit as st
import pandas as pd
import numpy as np
import math
import random

st.title('MERKLE -equipo 4')

#
a = st.radio('Analizar noticia desde:',["URL","Texto"])

# si se ha elegido analizar desde URL
if a == "URL":
    url_noticia=st.text_input("Introduce la dirección web de la noticia")
else: # si se ha elegido analizar desde texto
    txt_noticia=st.text_area("Introduce el texto de la noticia",value="Escribe o pega aquí el texto de la noticia")

