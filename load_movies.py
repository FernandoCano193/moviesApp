import requests
import environ
import psycopg2
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

env = environ.Env()
environ.Env.read_env(f'{BASE_DIR}/moviesApp/.env')

cur = None

def getGenreApi():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=es"
    headers = {"accept": "application/json"}
    params ={"api_key": env('API_KEY')}

    response = requests.get(url, headers=headers, params=params)
    data=json.loads(response.text)
    listGenre =[]

    for i in range(len(data['genres'])):
        listGenre.append(data['genres'][i]["name"])
    
    # print(listGenre)
    return(listGenre)
    


try:
    # CONEXION A LA BD
    connect = psycopg2.connect(
        host=env("HOST"),
        database=env("DATABASE_NAME"),
        user=env("USER"),
        password=env("PASSWORD"),
        port=env("PORT"))
    
    #Se crea el cursor
    cur = connect.cursor()

    #Genera una tupla para poder insertar los valores
    listGenre =[(genre,) for genre in getGenreApi()]

    #Consulta insert
    sqlQuery = "INSERT INTO movies_genre (name) VALUES (%s);"

    # delete = "DELETE FROM movies_genre"

    #Ejecuta la consulta
    cur.executemany(sqlQuery,listGenre)

    #Confirma la transacción
    connect.commit()

    print("Correcta conexión")

    
except Exception as Error:
    print(Error)
finally:
    if cur and connect is not None:
        #Cierre de la conexion de la bd
        cur.close()
        connect.close()




