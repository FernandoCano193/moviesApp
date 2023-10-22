from django.shortcuts import render
from .models import Movie, Person, MovieCredit

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    return render(request, 'index.html', {"movies":movies})


def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    movie_credit = MovieCredit.objects.filter(movie=movie)
    context = {'movie': movie,
               'movie_credits':movie_credit}
    return render(request, "movie_detail.html", context=context)


def person_detail(request, person_id):
    person = Person.objects.get(pk=person_id)
    credits = MovieCredit.objects.filter(person=person_id)
    context = {'person': person,
               'credits':credits}
    return render(request, "person_detail.html", context=context)