from typing import List
from flask_sqlalchemy import Pagination

from werkzeug.datastructures import FileStorage

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Products
from myshop.models import product as product_mdl


def create(title: str, description: str, price: int, category: str, stok: int, user_id: int):
    product = Products(
        title=title,
        description=description,
        price=price,
        category=category,
        stok=stok,
        user_id=user_id,
    )

    db.session.add(product)
    db.session.flush()

    return product  


def get(product_id: int):
    product = product_mdl.get_by_id(product_id=product_id)

    if product.is_deleted == 1:
        raise BadRequest("Produk sudah dihapus")

    return product


def delete(product_id: int):
    product = product_mdl.get_by_id(product_id=product_id)

    if product.is_deleted == 1:
        raise BadRequest("Produk sudah dihapus")

    product.is_deleted = 1
    
    db.session.add(product)
    db.session.flush()

    return product


def list(page: int, count: int, category: str, sort: str):
    filters = [
        Products.is_deleted == 0,
    ]

    sort_collections = {
        "-id": Products.id.desc(),
    }

    if category:
        filters.append(Products.category == category)

    sort_apply = sort_collections[sort]
        
    products = Products.query.filter(
        *filters
    ).order_by(
        sort
    ).paginate(
        page=page,
        per_page=count,
        error_out=False,
    )

    return products

