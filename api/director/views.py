from flask import request
from flask_restx import Resource, Namespace
from models.models import Director, db
from models.schema import DirectorSchema

director_ns = Namespace("directors")  # Создаём имя пространства (Namespace) режиссёров
director_schema = DirectorSchema()  # Схема сериализации одного режиссёра
directors_schema = DirectorSchema(many=True)  # Схема сериализации нескольких режиссёров


@director_ns.route("/")
class DirectorsView(Resource):
    """ CBV режисcёров
        GET получение данных всех режиссёров
        POST добавление данных нового режиссёра
    """

    def get(self):
        directors = db.session.query(Director).all()
        if not directors:
            return " Out of range ", 404
        return directors_schema.dump(directors), 200

    def post(self):
        json_req = request.json
        new_director = Director(**json_req)
        db.session.add(new_director)
        db.session.commit()
        return director_schema.dump(new_director), 201


@director_ns.route("/<int:director_id>/")
class DirectorView(Resource):
    """ CBV режисcёра
        GET получение данных режиссёра по id
        PUT изменяем данные режиссёра по id
        DELETE удаляем данные режиссёра по id
    """

    def get(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
            json_req = request.json

            director.id = json_req.get("id")
            director.name = json_req.get("name")

            db.session.add(director)
            db.session.commit()

            return director_schema.dump(director), 204
        except Exception as e:
            return str(e), 404

    def delete(self, director_id):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()

            db.session.delete(director)
            db.session.commit()

            return "", 204
        except Exception as e:
            return str(e), 404
