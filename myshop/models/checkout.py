import pendulum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from myshop.models import db


class Checkouts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    
    receiver_name = db.Column(db.String(50), nullable=False)

    address = db.Column(db.String(150), nullable=False)

    phone_number = db.Column(db.String(15), nullable=False)

    courir = db.Column(db.String(50), nullable=False)

    ongkir = db.Column(db.Integer, nullable=False)

    message = db.Column(db.String(255), default="")

    sub_total = db.Column(db.Integer, default=0)

    is_deleted = db.Column(db.Integer, default=0)

    user = relationship("Users", backref="checkouts_user")


    def __init__(self, user_id, receiver_name, address, phone_number, 
                 courir, ongkir, message, sub_total):
        self.user_id = user_id
        self.receiver_name = receiver_name
        self.address = address
        self.phone_number = phone_number
        self.courir = courir
        self.ongkir = ongkir
        self.message = message
        self.sub_total = sub_total


    @property
    def checkout_product_json(self):
        result = []
        if self.basketproduct_checkout:
            for product_checkout in self.basketproduct_checkout:
                result.append({
                    "id": product_checkout.product.id,
                    "title": product_checkout.product.title,
                    "description": product_checkout.product.description,
                    "category": product_checkout.product.category,
                    "user": product_checkout.product.user_json,
                    "product_image": {
                        "image": product_checkout.product.image_url,
                        "thumb": product_checkout.product.image_thumb_url,
                        "icon": product_checkout.product.image_icon_url,
                    },
                    "price": product_checkout.product.price,
                    "total": product_checkout.total,
                })

            return result

        else:
            return result


def get_by_user(user_id: int) -> Checkouts:
    return Checkouts.query.filter_by(user_id=user_id).first()