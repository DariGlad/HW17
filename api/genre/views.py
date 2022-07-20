from flask import request
from flask_restx import Resource, Namespace
from models.models import Genre, db
from models.schema import GenreSchema

genre_ns = Namespace("genres")  # Создаём имя пространства (Namespace) жанров
genre_schema = GenreSchema()  # Схема сериализации одного жанра
genres_schema = GenreSchema(many=True)  # Схема сериализации нескольких жанров


@genre_ns.route("/")
class GenresView(Resource):
    """ CBV жанров
        GET получение данных всех жанров
        POST добавление данных нового жанров
    """

    def get(self):
        genres = db.session.query(Genre).all()
        if not genres:
            return " Out of range ", 404
        return genres_schema.dump(genres), 200

    def post(self):
        json_req = request.json
        new_genre = Genre(**json_req)
        db.session.add(new_genre)
        db.session.commit()
        return genre_schema.dump(new_genre), 201


@genre_ns.route("/<int:genre_id>/")
class GenreView(Resource):
    """ CBV жанра
        GET получение данных жанра по id
        PUT изменяем данные жанра по id
        DELETE удаляем данные жанра по id
    """

    def get(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
            json_req = request.json

            genre.id = json_req.get("id")
            genre.name = json_req.get("name")

            db.session.add(genre)
            db.session.commit()

            return genre_schema.dump(genre), 204
        except Exception as e:
            return str(e), 404

    def delete(self, genre_id):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()

            db.session.delete(genre)
            db.session.commit()

            return "", 204
        except Exception as e:
            return str(e), 404
