from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.movie_user.utils import get_movie_user
from App.ext import cache
from App.models.movie_user import MovieUser
from App.utils import generate_movie_user_token

parse_base = reqparse.RequestParser()
parse_base.add_argument("password", type=str, required=True, help="请输入密码")
parse_base.add_argument("action", type=str, required=True, help="请输入请求参数")

parse_register = parse_base.copy()
parse_register.add_argument("phone", type=str, required=True, help="请输入手机号")
parse_register.add_argument("username", type=str, required=True, help="请输入用户名")

parse_login = parse_base.copy()
parse_login.add_argument("phone", type=str, help="请输入手机号")
parse_login.add_argument("username", type=str, help="请输入用户名")

movie_user_fields = {
    "username": fields.String,
    "password": fields.String(attribute="_password"),
    "phone": fields.String
}

single_movie_user_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(movie_user_fields)
}


class MovieUsersResource(Resource):

    def post(self):
        args = parse_base.parse_args()

        password = args.get("password")
        action = args.get("action")

        if action == "register":
            register_args = parse_register.parse_args()
            username = register_args.get("username")
            phone = register_args.get("phone")

            movie_user = MovieUser()
            movie_user.username = username
            movie_user.password = password
            movie_user.phone = phone

            if not movie_user.save():
                abort(400, msg="create fail")
            data = {
                "status": '201',
                "msg": "用户创建成功",
                "data": movie_user
            }
            return marshal(data, single_movie_user_fields)

        elif action == "login":
            login_args = parse_login.parse_args()
            username = login_args.get("username")
            phone = login_args.get("phone")

            user = get_movie_user(username) or get_movie_user(phone)

            if not user:
                abort(400, msg="用户不存在")
            if not user.check_password(password):
                abort(401, msg="密码错误")
            if user.is_delete:
                abort(400, msg="用户不存在")

            token = generate_movie_user_token()

            cache.set(token, user.id, timeout=60*60*24*7)

            data = {
                "msg": "login success",
                "status": 200,
                "token": token
            }
            return data
        else:
            abort(400, msg="请提供正确的参数")
