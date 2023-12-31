from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=128)
    character = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10,null=True)
    photo_path = models.URLField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    place_birth = models.CharField(max_length=200, null=True,blank=True)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.character})"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateField()
    running_time = models.IntegerField()
    budget = models.IntegerField(blank=True)
    tmdb_id = models.IntegerField(blank=True, unique=True)
    revenue = models.IntegerField(blank=True)
    poster_path = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Person, through="MovieCredit")

    def __str__(self):
        return self.title


class MovieCredit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title}: {self.person.name} ({self.job.name})"


class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                          MaxValueValidator(100)])
    review = models.TextField(blank=True)
