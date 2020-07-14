from flask_restful import Api

from App.apis.admin.admin_user_api import AdminUsersResource
from App.apis.admin.cinema_auth_api import AdiminCinemaUsersResource, AdiminCinemaUserResource

admin_api = Api(prefix='/admin')

admin_api.add_resource(AdminUsersResource, '/users/')
admin_api.add_resource(AdiminCinemaUsersResource, '/cinemausers/')
admin_api.add_resource(AdiminCinemaUserResource, '/cinemausers/<int:id>/')
