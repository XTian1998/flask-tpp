
from flask_restful import Resource, reqparse, fields, marshal, abort
from werkzeug.datastructures import FileStorage

from App.apis.admin.utils import login_required
from App.apis.common.utils import filename_transfer
from App.models.common.movie_model import Movie


parse = reqparse.RequestParser()
parse.add_argument("showname", required=True, help="请提供showname")
parse.add_argument("shownameen", required=True, help="请提供shownameen")
parse.add_argument("director", required=True, help="请提供director")
parse.add_argument("leadingRole", required=True, help="请提供leadingRole")
parse.add_argument("type", required=True, help="请提供type")
parse.add_argument("country", required=True, help="请提供country")
parse.add_argument("language", required=True, help="请提供language")
parse.add_argument("duration", required=True, help="请提供duration")
parse.add_argument("screeningmodel", required=True, help="请提供screeningmodel")
parse.add_argument("openday", required=True, help="请提供openday")
parse.add_argument("backgroundpicture", type=FileStorage, required=True, help="请提供backgroundpicture", location=['files'])

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


class MoviesResource(Resource):

    def get(self):
        movies = Movie.query.all()

        data = {
            "msg": "ok",
            "status": 200,
            "data": movies
        }

        return marshal(data, multi_movies_fileds)

    @login_required
    def post(self):

        args = parse.parse_args()
        showname = args.get("showname")
        shownameen = args.get("shownameen")
        director = args.get("director")
        leadingRole = args.get("leadingRole")
        movie_type = args.get("type")
        country = args.get("country")
        language = args.get("language")
        duration = args.get("duration")
        screeningmodel = args.get("screeningmodel")
        openday = args.get("openday")
        backgroundpicture = args.get("backgroundpicture")

        movie = Movie()
        movie.showname = showname
        movie.shownameen = shownameen
        movie.director = director
        movie.leadingRole = leadingRole
        movie.type = movie_type
        movie.country = country
        movie.language = language
        movie.duration = duration
        movie.screeningmodel = screeningmodel
        movie.openday = openday

        file_info = filename_transfer(backgroundpicture.filename)

        filepath = file_info[0]
        backgroundpicture.save(filepath)
        movie.backgroundpicture = file_info[1]

        if not movie.save():
            abort(400, msg="can't create movie")

        data = {
            "msg": "create success",
            "status": 201,
            "data": marshal(movie, movie_fields)
        }

        return data


class MovieResource(Resource):

    def get(self, id):
        movie = Movie.query.get(id)
        if not movie:
            abort(404, msg="movie not exists")

        data = {
            "msg": "ok",
            "status": 200,
            "data": marshal(movie, movie_fields)
        }

        return data

    @login_required
    def patch(self, id):
        return {"msg": " patch ok"}

    @login_required
    def put(self, id):
        return {"msg": " put ok"}

    @login_required
    def delete(self, id):
        return {"msg": " delete ok"}