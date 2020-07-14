from App.ext import db
from App.models import BaseModel
from App.models.movie_user import MovieUser

ORDER_STATUS_NOT_PAY = 0
ORDER_STATUS_PAYED_MOT_GET = 1
ORDER_STATUS_GET = 2
ORDER_STATUS_TIMEOUT = 3


class MovieOrder(BaseModel):
    o_user_id = db.Column(db.Integer, db.ForeignKey(MovieUser.id))
    o_hall_movie_id = db.Column(db.Integer, db.ForeignKey("hall_movie.id"))
    o_time= db.Column(db.DateTime)
    o_status = db.Column(db.Integer, default=0)
    o_seats = db.Column(db.String(128))
    o_price = db.Column(db.Float, default=0)
