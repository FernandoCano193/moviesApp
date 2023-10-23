from django.urls import path
from . import views

urlpatterns =[
    path('', views.index),
    path("movie/<int:movie_id>/", views.movie_detail),
    path("person/<int:person_id>/", views.person_detail)
]