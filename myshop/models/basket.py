import pendulum
import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from myshop.models import db


class Baskets(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey("users.id"), default=0)

    sub_total = db.Column(db.Integer, default=0)

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

    @property
    def user_json(self):
        return {
            "id": self.user.id,
            "username": self.user.username,
            "fullname": self.user.fullname,
            "avatar": self.user.avatar_url,
            "email": self.user.email,
            "phone_number": self.user.phone_number,
        }

    @property
    def basket_product_json(self):
        result = []
        if self.basketproduct_basket:
            for basket in self.basketproduct_basket:
                result.append({
                    "id": basket.id,
                    "product_id": basket.product_id,
                    "product_title": basket.product.title,
                    "product_description": basket.product.description,
                    "product_price": basket.product.price,
                    "product_image": {
                        "image": basket.product.image_url,
                        "thumb": basket.product.image_thumb_url,
                        "icon": basket.product.image_icon_url,
                    },
                    "totals": basket.total,
                    "created_on": basket.product.created_on.timestamp(),
                    "product_user": basket.product.user_json,
                })

            return result
        else:
            return None

def get_by_userid(user_id: int) -> Baskets:
    return Baskets.query.filter_by(user_id=user_id, is_deleted=0).first()


def get_by_id(basket_id: int) -> Baskets:
    return Baskets.query.filter_by(id=basket_id, is_deleted=0).first()