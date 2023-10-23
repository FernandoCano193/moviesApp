import requests
import environ
import psycopg2
from pathlib import Path
import json
import sys

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
    

def getCredits(idMovie):
    url = f"https://api.themoviedb.org/3/movie/{idMovie}/credits"
    data = getDataAPI(url)

    cast = data['cast'][:10]
    crew = data['crew'][:5]

    credits = cast + crew
    return credits


def getPersonData(idPerson, character):
    gender = None
    photo = None
    url = f"https://api.themoviedb.org/3/person/{idPerson}"
    data = getDataAPI(url)

    if data.get('gender')==0:
        gender = "Not set"
    elif data.get('gender')==1:
        gender = "Female"
    elif data.get('gender')==2:
        gender = "Male"
    else:
        gender = "Non-binary"
    
    if data.get('profile_path') is not None:
        photo = path_image+data.get('profile_path')
    else:
        photo = "N/A"

    personData=(data.get('name'), character, gender, photo, data.get('birthday'), data.get('place_of_birth'), data.get('biography'))
    return personData


def getJobs(credits):
    jobs =[]
    for job in credits:
        if not job.get('job'):
            if "Actor" not in jobs: jobs.append("Actor")
        else:
            if job.get('job'): jobs.append(job.get('job'))
    
    return jobs

def load_movie(id):
    url = f"https://api.themoviedb.org/3/movie/{id}"
    data = getDataAPI(url)
    # # print(json.dumps(data, indent=4))
    
    credits = getCredits(id)

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

        cur.execute("SELECT * FROM movies_genre")
        listGenresBD = cur.fetchall()

        if not listGenresBD:
            genres = getGenreApi()
            #Genera una tupla para poder insertar los valores
            listGenre = [(genre,) for genre in genres]
            sqlQuery = "INSERT INTO movies_genre (name) VALUES (%s);"
            cur.executemany(sqlQuery, listGenre)
        
        listGenre = []
        for gnresName in data.get('genres'):
            listGenre.append(gnresName.get('name'))
        
        # Se recuperan los id de los genres y se almacenan en idGenres
        sqlQuery=("SELECT id FROM movies_genre WHERE name = ANY(%s)")
        cur.execute(sqlQuery, (listGenre,))
        idGenres = cur.fetchall()


        # ----- JOBS ------
        cur.execute("SELECT name FROM movies_job")
        
        #lista de trabajos existentes en la bd
        existingJobs = cur.fetchall()

        # lista de los trabajos en credits
        listJobs = getJobs(credits=credits)

        #Genera una tupla para poder hacer la comparacion
        listJobs=[(job,) for job in listJobs]

        newJobs=[]

        for job in listJobs:
            if job not in existingJobs:
                newJobs.append(job)


        if newJobs:
            sqlQuery = "INSERT INTO movies_job (name) VALUES (%s);"
            cur.executemany(sqlQuery, newJobs)

        sqlQuery = "SELECT id FROM movies_job WHERE name = ANY(%s)"
        cur.execute(sqlQuery, (listJobs,))
        idJobs = cur.fetchall()
        print(idJobs)

        # ----- PERSONS -----
        
        personData=[]
        for person in credits:
            if person.get('character') is not None:
                personData.append(getPersonData(person.get('id'), person.get('character')))
            else:
                personData.append(getPersonData(person.get('id'), person.get('department')))
        
        sqlQuery = "INSERT INTO movies_person (name, character, gender, photo_path, birth_date, place_birth, biography) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        # Ejecuta la inserción
        cur.executemany(sqlQuery, personData)


        # ------ Movie ------
        sqlQuery = """INSERT INTO movies_movie (title, overview, release_date, 
        running_time, budget, tmdb_id, revenue, poster_path) VALUES (%s, %s, %s, %s,
        %s, %s, %s, %s) RETURNING id"""

        movieData = (data['title'], data['overview'], data['release_date'], 
                     data['runtime'], data['budget'], data['id'], data['revenue'], path_image+data['poster_path'])

        print(movieData)

        cur.execute(sqlQuery, movieData)
        idMovie = cur.fetchone()

        # ----- MovieGeneres ------
        for genre in idGenres:
            sqlQuery = """INSERT INTO movies_movie_genres (movie_id, genre_id) VALUES (%s, %s)"""
            cur.execute(sqlQuery, (idMovie, genre))

        # ----- MovieCredit -----
        job = None
        for credit in credits:
            sqlQuery =  """INSERT INTO movies_moviecredit (movie_id, person_id, job_id)
         SELECT movies_movie.id,
         (SELECT id FROM movies_person WHERE name = %s LIMIT 1) as person_id,
         (SELECT id FROM movies_job WHERE name = %s LIMIT 1) as job_id
         FROM movies_movie 
         WHERE title = %s"""
            if credit.get('job') is None:
                job="Actor"
            else:
                job=credit.get('job')
            cur.execute(sqlQuery, (credit.get('name'), job, data['title']))

        #Confirma la transacción
        connect.commit()

        print("PELÍCULA NUEVA AGREGADA A LA BD")

    
    except Exception as Error:
        print(Error)
    finally:
        if cur and connect is not None:
            #Cierre de la conexion de la bd
            cur.close()
            connect.close()
    
if __name__ == "__main__":
    load_movie(sys.argv[1])