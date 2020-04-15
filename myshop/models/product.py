import pendulum
import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from myshop.models import db


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)

    description = db.Column(db.String(100), nullable=False)
    
    price = db.Column(db.Integer, nullable=False)

    category = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, ForeignKey("users.id"), default=0)

    stok = db.Column(db.Integer, default=0)

    total_view = db.Column(db.Integer, default=0)

    total_review = db.Column(db.Integer, default=0)

    created_on = db.Column(db.DateTime, default=0)

    is_deleted = db.Column(db.Integer, default=0)

    updated_on = db.Column(db.DateTime, default=0)

    user = relationship("Users", backref="products")

    def __init__(self, title, description, price, category, stok, user_id):
        """
        Args:
            title: nama produk
            price: harga produk
            category: kategori produk
        """
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.stok = stok
        self.user_id = user_id
        
        self.created_on = pendulum.now()


def get_by_id(product_id) -> Products:
    product = Products.query.filter_by(id=product_id).first()

    return product