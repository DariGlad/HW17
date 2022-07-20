from flask import request
from flask_restx import Resource, Namespace
from models.models import Movie, db
from models.schema import MovieSchema

movie_ns = Namespace("movies")  # Создаём имя пространства (Namespace) фильмов
movie_schema = MovieSchema()  # Схема сериализации одного фильма
movies_schema = MovieSchema(many=True)  # Схема сериализации нескольких фильмов


@movie_ns.route("/")
class MoviesView(Resource):
    """ CBV фильмов
        GET Получаем данные всех фильмов,
        фильмов по жанрам или режиссёрам,
        фильмов по жанрам и режиссёрам
        POST Добавление данных нового фильма
        """

    # Создаём документацию и параметры для GET
    @movie_ns.doc(description="При заполнении id режиссёра, выведутся фильмы данного режиссёра\n"
                              "При заполнении id жанра, выведутся фильмы данного жанра\n"
                              "При заполнении id жанра и режиссёра, выведутся фильмы по полученным id\n"
                              "При незаполненных полях, выведутся все данные",
                  params={
                      "director_id": "id режиссёра",
                      "genre_id": "id жанра"
                  })
    def get(self):

        director_id = request.values.get("director_id", type=int)  # Получаем id режиссёра
        genre_id = request.values.get("genre_id", type=int)  # Получаем id жанра

        # Поиск по id режиссёра и жанра
        if director_id and genre_id:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id, Movie.genre_id == genre_id).all()

        # Поиск по id режиссёра
        elif director_id:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id).all()

        # Поиск по id жанра
        elif genre_id:
            movies = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()

        # Вывод всех фильмов, если не получены id режиссёра и жанра
        else:
            movies = db.session.query(Movie).all()
        if not movies:  # Если полученные id отсутствуют в списке данных, выведет ошибку
            return " Out of range ", 404
        return movies_schema.dump(movies), 200

    def post(self):

        json_req = request.json
        new_movie = Movie(**json_req)
        db.session.add(new_movie)
        db.session.commit()
        return movie_schema.dump(new_movie), 201


@movie_ns.route("/<int:movie_id>/")
class MovieView(Resource):
    """ CBV фильма
        GET получение данных фильма по id
        PUT изменяем данные фильма по id
        DELETE удаляем данные фильма по id
    """

    def get(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
            json_req = request.json

            movie.id = json_req.get("id")
            movie.title = json_req.get("title")
            movie.description = json_req.get("description")
            movie.trailer = json_req.get("trailer")
            movie.year = json_req.get("year")
            movie.rating = json_req.get("rating")
            movie.genre_id = json_req.get("genre_id")
            movie.director_id = json_req.get("director_id")

            db.session.add(movie)
            db.session.commit()

            return movie_schema.dump(movie), 204
        except Exception as e:
            return str(e), 404

    def delete(self, movie_id):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()

            db.session.delete(movie)
            db.session.commit()

            return "", 204
        except Exception as e:
            return str(e), 404
