import pendulum
import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from myshop.models import db


class BasketProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    basket_id = db.Column(db.Integer, ForeignKey("baskets.id"), default=0)

    product_id = db.Column(db.Integer, ForeignKey("products.id"), default=0)

    total = db.Column(db.Integer, default=0)

    is_deleted = db.Column(db.Integer, default=0)

    created_on = db.Column(db.DateTime, default=0)

    updated_on = db.Column(db.DateTime, default=0)

    product = relationship("Products", backref="basketproduct_product")

    basket = relationship("Baskets", backref="basketproduct_basket",
                          primaryjoin="and_(BasketProducts.basket_id==Baskets.id ,"
                                      "BasketProducts.is_deleted==0)")

    def __init__(self, basket_id, product_id, total):
        """
        Args:
            basket_id: id basket yang dipilih
            product_id: id product yang dipilih

        """
        self.basket_id = basket_id
        self.product_id = product_id
        self.total = total

        self.created_on = pendulum.now()