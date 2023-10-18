Prueba commit
Preview de archivo html usando tailwind:

![Alt text](https://github.com/FernandoCano193/moviesApp/blob/selvindev/Images/image.png)
![Alt text](image.png)
![Alt text](image.png)
![Alt text](image-1.png)


<link href="moviesApp/output.css" rel="stylesheet">
<link href="{% static 'movies/assets/output.css' %}" rel="stylesheet">


<img src="{% static 'movies/assets/img'|add:movie.poster_path %}" alt="">

return render(request, "movies/movie_detail.html", context=context)