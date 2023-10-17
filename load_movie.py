import requests
import environ
import psycopg2
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

env = environ.Env()
environ.Env.read_env(f'{BASE_DIR}/moviesApp/.env')

cur = None

path_image = "https://image.tmdb.org/t/p/original"

headers = {"accept": "application/json",
        "Authorization":"Bearer "+env('API_TOKEN')}

params ={
    "api_key":env("API_KEY")
}

def getDataAPI(url):
    response = requests.get(url, headers=headers)
    data= json.loads(response.text)
    return data

def getGenreApi():
    url = "https://api.themoviedb.org/3/genre/movie/list"
    
    data =getDataAPI(url=url)
    genre = ()
    listGenre=[]

    for i in range(len(data['genres'])):
        genre = (data['genres'][i]["name"])
        listGenre.append(genre)
    
    return listGenre
    
def getIDMovies():
    url = "https://api.themoviedb.org/3/discover/movie"
    
    data = getDataAPI(url)

    listID = []

    for movie in data['results']:
        listID.append((movie['id']))
    
    return listID

def getPersonData():
    listIdMovies = getIDMovies()
    dataPersons=[]
    jobs =[]

    # se recuperan los id de las personas
    for id in listIdMovies:
        url = f"https://api.themoviedb.org/3/movie/{id}/credits"
        data = getDataAPI(url)
        jobs = getJobs(data)
        for person in data['cast']:
            gender = person.get('gender')
            if gender == 0:
                gender = "Not set"
            elif gender == 1:
                gender = "Female"
            elif gender == 2:
                gender = "Male"
            else:
                gender = "Non-binary"
            
            if person.get('profile_path') is not None:
                full_path = path_image + person.get('profile_path')
            else:
                full_path = "N/A"
                

            dataPersons.append((person.get('name'), person.get('character'), gender, full_path))
    
    
    return dataPersons, jobs


def getJobs(data):
    jobs =["Actor"]

    for job in data['crew']:
        if(job.get('job') not in jobs):
            jobs.append(job.get('job'))

    return jobs
    



def getDataMovie():
    listID = getIDMovies()
    dataMovies=[]
    listMovies=[]
    for id in listID:
        url =f"https://api.themoviedb.org/3/movie/{id}"
        data = getDataAPI(url)
        dataMovies = (data.get('title'),data.get('overview'), data.get('release_date'), data.get('runtime')
                    ,data.get('budget'),data.get('id'),data.get('revenue'), path_image+data.get('poster_path'))
        listMovies.append(dataMovies)

    print(json.dumps(data, indent=4))

        

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


    # ----- INSERCION A LA BD DE LOS GENEROS -----

    listGenre = getGenreApi()

    #Genera una tupla para poder insertar los valores
    listGenre = [(genre,) for genre in listGenre]
    sqlQuery = "INSERT INTO movies_genre (name) VALUES (%s);"
    
    # Ejecuta la consulta
    cur.executemany(sqlQuery,listGenre)

    # ----- INSERCION A LA BD DE LOS TRABAJOS -----
    listPersons, listJobs = getPersonData()
    listJobs = [(job,) for job in listJobs]
    sqlQuery = "INSERT INTO movies_job (name) VALUES (%s);"
    cur.executemany(sqlQuery, listJobs)

    # ----- INSERCION A LA BD DE LAS PERSONAS
    listPersons = getPersonData()
    sqlQuery = "INSERT INTO movies_person (name, character, gender, photo_path, birth_date, biography,place_birth) VALUES (%s, %s, %s, %s, '2023-10-16', 'biography', 'place_birth');"
    cur.executemany(sqlQuery, listPersons)

    # ----- INSERCION A LA BD DE LAS PELICULAS


    # ----- INSERCION A LA BD DE LAS RELACIONES
    query1 = "ALTER TABLE movies_movie ADD CONSTRAINT FK_GENRE FOREIGN KEY(genres) REFERENCES movies_genre (id)"
    query2 = "ALTER TABLE movies_movie ADD CONSTRAINT FK_CREDITS FOREIGN KEY(credits) REFERENCES movies_moviecredit (id)"

    query3 = "ALTER TABLE movies_moviecredit ADD CONSTRAINT FK_PERSON FOREIGN KEY(person) REFERENCES movies_person (id)"
    query4 = "ALTER TABLE movies_moviecredit ADD CONSTRAINT FK_MOVIE FOREIGN KEY(movie) REFERENCES movies_movie (id)"
    query5 = "ALTER TABLE movies_moviecredit ADD CONSTRAINT FK_JOB FOREIGN KEY(job) REFERENCES movies_job (id)"

    query6 = "ALTER TABLE movies_moviereview ADD CONSTRAINT FK_USER FOREIGN KEY(user) REFERENCES auth_user (id)"
    query7 = "ALTER TABLE movies_moviereview ADD CONSTRAINT FK_MOVIE_REVIEW FOREIGN KEY(movie) REFERENCES movies_movie (id)"

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



