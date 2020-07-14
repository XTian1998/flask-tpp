from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.cinema_admin.permissions_constant import PERMISSION_WRITE
from App.apis.cinema_admin.utils import require_permission
from App.models.cinema_admin.cinema_address_model import CinemaAddress

parse = reqparse.RequestParser()
parse.add_argument("name", required=True, help="请提供影院名称")
parse.add_argument("phone", required=True, help="请提供联系方式")
parse.add_argument("city", required=True, help="请提供城市")
parse.add_argument("district", required=True, help="请提供所在区域")
parse.add_argument("address", required=True, help="请提供详细地址")

cinema_fields = {
    "c_user_id": fields.Integer,
    "name": fields.String,
    "city": fields.String,
    "district": fields.String,
    "phone": fields.String,
    "score": fields.Float,
    "servicecharge": fields.Float,
    "astrict": fields.Float,
    "hallnum": fields.Integer,
}


class CinemaAddressesResource(Resource):

    def get(self):
        return {"msg": "ok"}

    @require_permission(PERMISSION_WRITE)
    def post(self):
        args = parse.parse_args()

        name = args.get("name")
        phone = args.get("phone")
        city = args.get("city")
        district = args.get("district")
        address = args.get("address")

        cinema_address = CinemaAddress()
        cinema_address.c_user_id = g.user.id
        cinema_address.name = name
        cinema_address.phone = phone
        cinema_address.city = city
        cinema_address.district = district
        cinema_address.address = address

        if not cinema_address.save():
            abort(400, msg="cinema can't create")

        data = {
            "status": 201,
            "msg": "cinema create ok",
            "data": marshal(cinema_address, cinema_fields)
        }

        return data


class CinemaAddressResource(Resource):

    def get(self, id):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass
