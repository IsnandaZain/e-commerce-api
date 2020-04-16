import pendulum
import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from myshop.models import db


class Baskets(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey("users.id"), default=0)

    is_deleted = db.Column(db.Integer, default=0)

    created_on = db.Column(db.DateTime, default=0)

    updated_on = db.Column(db.DateTime, default=0)

    user = relationship("Users", backref="baskets")

    def __init__(self, user_id):
        """
        Args:
            user_id: user yang memiliki keranjang

        """
        self.user_id = user_id

        self.created_on = pendulum.now()
    

def get_by_userid(user_id: int) -> Baskets:
    return Baskets.query.filter_by(user_id=user_id, is_deleted=0).first()