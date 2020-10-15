# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 16:09:46 2020

@author: Usuario
"""


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk
import warnings
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

#raices español
spanish_stemmer = SnowballStemmer('spanish')
warnings.filterwarnings('ignore')

def recomendations(producto_buscar,lista_productos):
    product_user_likes = producto_buscar['name']
    description=producto_buscar['description']
    df1 ={'id': 0, 'name': product_user_likes, 'description': description}
    #llevando de variable el arreglo json
    filas=pd.read_json(lista_productos)
    df1=pd.json_normalize(df1)
    frames = [df1, filas ]
    #combinar el dato de entrada con el arreglo en la base de datos
    rows = pd.concat(frames)
    rows.head()
    rows.index = range(rows.shape[0])

    features = ["name","description"]

    #rellenar datos vacios
    for feature in features:
        rows[feature] = rows[feature].fillna('')
    
    #combinar titulo y descripcion
    def combine_features(row):
        try:
            return row['name'] +" "+row['description']
        except:
            print("Error:", row)
    rows["combined_features"] = rows.apply(combine_features,axis=1)
    cleaned_resumes = []
    #eliminador de palabras no claves del español
    stop_words = stopwords.words('spanish')
    #lleva las palabras en un array y las coloca a todas en minuscula
    rows['combined_features'] = rows['combined_features'].str.lower().str.split()
    #aplica la funcion de eliminar palabras no claves en la combinacion de titulo y descripcion
    rows['combined_features']=rows["combined_features"].apply(lambda x: [word for word in x if word not in stop_words])
    #lleva todas las palabra a su raiz
    cleaned_resumes=rows['combined_features'].apply(lambda words: [spanish_stemmer.stem(word) for word in words])
    #elimina las palabras repetidas
    cleaned_resumes_new=cleaned_resumes.apply(lambda words: list(set(words)))
    
    rows['combined_features']=cleaned_resumes_new
    rows["features"]=rows["combined_features"].apply(lambda x: [word for word in x if word not in stop_words])
    #union de las palabras en un string
    rows["features"]=rows["features"].apply(lambda x: " ".join(x))
    #creacion de otro index
    rows['index1'] = rows.index
    #aplicacion de algoritmo de contaje de palabras clave
    cv = CountVectorizer(analyzer='word',)
    # matriz de contaje de palabras
    count_matrix = cv.fit_transform(rows["features"])

    #aplicacion de similaridad del coseno
    cosine_sim = cosine_similarity(count_matrix)

    def get_title_from_index(index):
        return rows[rows.index == index]["name"].values[0]

    def get_home(index):
        return rows[rows.index == index]["description"].values[0]

    def get_index_from_title(title):
        return rows[rows.name == title]["index1"].values[0]

    def get_id_from_index(index):
        return rows[rows.index == index]["id"].values[0]


    #obtencion del index basado en el titulo
    product_index = get_index_from_title(product_user_likes)

    #obtencion de producto similaes
    similar_products =  list(enumerate(cosine_sim[product_index]))

    #mostrar los productos similares a partir del mas parecido
    sorted_similar_products = sorted(similar_products,key=lambda x:x[1],reverse=True)

    #muestra de los productos mas parecidos
    i=0
    recomendaciones = []
    for element in sorted_similar_products:
        if i>0:
            dfnew ={'id': int(get_id_from_index(element[0])), 'name': get_title_from_index(element[0]), 'description': get_home(element[0])}
            recomendaciones.append(dfnew)
        i=i+1
        if i>11:
            break
    return recomendaciones
    

