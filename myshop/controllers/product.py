from typing import List
from flask_sqlalchemy import Pagination

from werkzeug.datastructures import FileStorage

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Products
from myshop.models import product as product_mdl


def create(title: str, price: int, size: List[int], color: List[str], category: str):
    product = Products(
        title=title,
        price=price,
        category=category,
    )

    db.session.add(product)
    db.session.flush()

    return product    