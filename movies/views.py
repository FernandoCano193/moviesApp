from django.shortcuts import render
from .models import Movie 

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    print(movies)
    return render(request, 'index.html', {"movies":movies})