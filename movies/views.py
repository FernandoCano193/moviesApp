from django.shortcuts import render
from django.http import HttpResponse
from movies.models import Movie, Person, MovieCredit
# Create your views here.


def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, "movies/index.html", context=context)


def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie_credit = MovieCredit.objects.all()
    person = Person.objects.all()
    context = {'movie': movie,
               'movie_credits':movie_credit,
               'person':person}
    return render(request, "movies/basic2.html", context=context)

def prueba(request):
    #movie = Movie.objects.get(pk=movie_id)
    #context = {'movie': movie}
    return render(request, "movies/basic2.html")

def person_detail(request, person_id):
    person = Person.objects.get(pk=person_id)
    context = {'person': person}
    return render(request, "movies/person_detail.html", context=context)
