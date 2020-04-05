import time

from sqlalchemy.orm import relationship, backref

from myshop.models import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    title = db.Column(db.String, nullable=False)

    price = db.Column(db.Integer, nullable=False)

    category = db.Column(db.String, nullable=False)

    user_id = db.Column(db.String, default=0)

    created_on = db.Column(db.Integer, default=0)

    is_deleted = db.Column(db.Integer, default=0)

    def __init__(self, title, price, category):
        """
        Args:
            title: nama produk
            price: harga produk
            category: kategori produk
        """
        self.title = title
        self.price = price
        self.category = category
        
        self.created_on = time.time()