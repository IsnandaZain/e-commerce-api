import pendulum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from myshop.models import db


class ProductComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, ForeignKey("products.id"), default=0)

    user_id = db.Column(db.Integer, ForeignKey("users.id"), default=0)

    text = db.Column(db.String(255), nullable=False)

    is_deleted = db.Column(db.Boolean, default=0)

    created_on = db.Column(db.DateTime, default=0)

    user = relationship("Users", backref="productcomments_user")

    product = relationship("Products", backref="productcomments_products")

    def __init__(self, product_id: int, text: str, user_id: int):
        self.product_id = product_id
        self.text = text
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
    def product_json(self):
        return {
            "id": self.product.id,
            "title": self.product.title,
            "product_image": {
                "image": self.product.image_url,
                "thumb": self.product.image_thumb_url,
                "icon": self.product.image_icon_url
            },
            "category": self.product.category,
        }


def get_by_id(comment_id: int) -> ProductComments:
    return ProductComments.query.filter_by(id=comment_id, is_deleted=0).first()
    