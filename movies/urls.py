from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("person/<int:person_id>/",views.person_detail, name="person_detail" )
]