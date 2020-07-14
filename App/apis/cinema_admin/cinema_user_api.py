
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.cinema_admin.utils import get_cinema_user
from App.ext import cache
from App.models.cinema_admin.cinema_user_model import CinemaUser
from App.utils import generate_cinema_user_token

parse_base = reqparse.RequestParser()
parse_base.add_argument("password", type=str, required=True, help="请输入密码")
parse_base.add_argument("action", type=str, required=True, help="请输入请求参数")

parse_register = parse_base.copy()
parse_register.add_argument("phone", type=str, required=True, help="请输入手机号")
parse_register.add_argument("username", type=str, required=True, help="请输入用户名")

parse_login = parse_base.copy()
parse_login.add_argument("phone", type=str, help="请输入手机号")
parse_login.add_argument("username", type=str, help="请输入用户名")

cinema_user_fields = {
    "username": fields.String,
    "password": fields.String(attribute="_password"),
    "phone": fields.String,
    "is_verify": fields.Boolean
}

single_cinema_user_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(cinema_user_fields)
}


class CinemaUsersResource(Resource):

    def post(self):
        args = parse_base.parse_args()

        password = args.get("password")
        action = args.get("action")

        if action == "register":
            register_args = parse_register.parse_args()
            username = register_args.get("username")
            phone = register_args.get("phone")

            cinema_user = CinemaUser()
            cinema_user.username = username
            cinema_user.password = password
            cinema_user.phone = phone

            if not cinema_user.save():
                abort(400, msg="create fail")
            data = {
                "status": '201',
                "msg": "用户创建成功",
                "data": cinema_user
            }
            return marshal(data, single_cinema_user_fields)

        elif action == "login":
            login_args = parse_login.parse_args()
            username = login_args.get("username")
            phone = login_args.get("phone")

            user = get_cinema_user(username) or get_cinema_user(phone)

            if not user:
                abort(400, msg="用户不存在")
            if not user.check_password(password):
                abort(401, msg="密码错误")
            if user.is_delete:
                abort(400, msg="用户不存在")

            token = generate_cinema_user_token()

            cache.set(token, user.id, timeout=60*60*24*7)

            data = {
                "msg": "login success",
                "status": 200,
                "token": token
            }
            return data
        else:
            abort(400, msg="请提供正确的参数")
