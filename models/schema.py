from marshmallow import Schema, fields


class MovieSchema(Schema):
    """ Схема для сериализации фильмов """
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Pluck("GenreSchema", "name")
    director = fields.Pluck("DirectorSchema", "name")


class GenreSchema(Schema):
    """ Схема для сериализации жанра """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class DirectorSchema(Schema):
    """ Схема для сериализации режиссёра """
    id = fields.Int(dump_only=True)
    name = fields.Str()
