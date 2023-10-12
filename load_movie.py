import os
import environ
import requests


env = environ.Env()
environ.Env.read_env('.env')
print('CLAVE_API: ', env('CLAVE_API'))
print('TOKEN_API: ', env('TOKEN_API'))

'''
url --request GET \
     --url 'https://api.themoviedb.org/3/movie/76341?language=en-US' \
     --header 'Authorization: Aasdfqwer' \
     --header 'accept: application/json'
'''
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {env('TOKEN_API')}"}

movie_id = 76341
r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US', headers=headers) 
print(r.json())


r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US', headers=headers) 
credits = r.json()
for actor in credits['cast'][:10]:
    print(actor['id'], actor['name'], actor['order'], actor['known_for_department'])

for job in credits['crew'][:15]:
    print(job['name'], job['department'], job['job'])
