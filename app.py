# app.py

from flask import Flask
from flask_restx import Api

from api.movie.views import movie_ns
from api.genre.views import genre_ns
from api.director.views import director_ns
from models.models import db

app = Flask(__name__)  # Создаём экземпляр flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'  # Путь к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False  # Отключаем использование ASCII в json

db.init_app(app)  # Инициализируем базу данных в app
app.app_context().push()  # Сохраняем настройки app

api = Api(app)  # Создаём экземпляр api

api.add_namespace(movie_ns)  # Добавляем импортированный namespace фильмов в api
api.add_namespace(genre_ns)  # Добавляем импортированный namespace жанров в api
api.add_namespace(director_ns)  # Добавляем импортированный namespace режиссёров в api

if __name__ == '__main__':
    app.run(debug=True)
