from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.cinema_admin.utils import login_required
from App.models.cinema_admin.cinema_movie_model import CinemaMovie
from App.models.common.movie_model import Movie

parse = reqparse.RequestParser()
parse.add_argument("movie_id", required=True, help="请选择要购买的电影")

movie_fields = {
    "showname": fields.String,
    "shownameen": fields.String,
    "director": fields.String,
    "leadingRole": fields.String,
    "type": fields.String,
    "country": fields.String,
    "language": fields.String,
    "duration": fields.Integer,
    "screeningmodel": fields.String,
    "openday": fields.DateTime,
    "backgroundpicture": fields.String,
}

multi_movies_fileds = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.List(fields.Nested(movie_fields))
}


class CinemaMoviesResource(Resource):

    @login_required
    def get(self):
        user_id = g.user.id
        cinema_movies = CinemaMovie.query.filter(CinemaMovie.c_cinema_id==user_id).all()

        movies = []

        for cinema_movie in cinema_movies:
            movies.append(Movie.query.get(cinema_movie.c_movie_id))


        data = {
            "msg": "ok",
            "status": 200,
            "data": movies
        }

        return marshal(data, multi_movies_fileds)

    @login_required
    def post(self):
        user_id = g.user.id

        args = parse.parse_args()
        movie_id = args.get("movie_id")
        cinema_movies = CinemaMovie.query.filter(CinemaMovie.c_cinema_id==user_id).filter(CinemaMovie.c_movie_id==movie_id).all()

        if cinema_movies:
            abort(400, msg="已经购买了此电影")

        cinema_movie = CinemaMovie()

        cinema_movie.c_movie_id = movie_id
        cinema_movie.c_cinema_id = user_id

        if not cinema_movie.save():
            abort(400, msg="购买失败")

        data = {
            "msg": "购买成功",
            "status": 201
        }

        return data
