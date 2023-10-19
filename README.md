Prueba commit
Preview de archivo html usando tailwind:

![Alt text](https://github.com/FernandoCano193/moviesApp/blob/selvindev/Images/image.png)
![Alt text](image.png)
![Alt text](image.png)
![Alt text](image-1.png)
![Alt text](image.png)
![Alt text](image.png)
![Alt text](image.png)
![Alt text](image.png)
![Alt text](image.png)
![Alt text](image-1.png)

<link href="moviesApp/output.css" rel="stylesheet">
<link href="{% static 'movies/assets/output.css' %}" rel="stylesheet">


<img src="{% static 'movies/assets/img'|add:movie.poster_path %}" alt="">

return render(request, "movies/movie_detail.html", context=context)

{% for m in movie_credits %}
                    <h1> movie:  {{movie.title}} MOVIECREDITS: {{m.movie}} </h1> 
                    {% if m.movie == movie.title %}
                        <h1> Actor:  {{m.person}} </h1>
                    {% else %}
                        <h1> No entro </h1>
                    {% endif %}
                {% endfor %}

Por hacer:
detalle_movie
detalle_person
- agregar mas detalles a ambos toda la info necesaria