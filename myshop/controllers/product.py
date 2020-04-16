from typing import List
from flask_sqlalchemy import Pagination

from PIL import Image, ImageOps
from werkzeug.datastructures import FileStorage

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Products
from myshop.models import product as product_mdl


def image_valid_ratio(image) -> bool:
    """Validate image ratio for product

    Ratio 3:4 with pixel compensation 10px
    """
    # 3:4 in xxhdpi is (984, 1312)
    w = 984
    h = 1312
    compensation = 10

    return abs(image.size[1] - h / w * image.size[0]) <= compensation


def create(title: str, description: str, price: int, category: str, stok: int, 
           user_id: int, product_image: FileStorage, product_video: FileStorage):
    product = Products(
        title=title,
        description=description,
        price=price,
        category=category,
        stok=stok,
        user_id=user_id,
    )

    img = Image.open(product_image)
    # convert image agar lebih proper
    if img.mode == "P":
        img = img.convert("RGBA")
    elif img.mode == "L":
        img = img.convert("RGB")

    if not image_valid_ratio(img):
        raise  BadRequest("image ratio salah, gunakan ratio 3:4")

    # for transparent image image
    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background

    # set image for product
    size_image = (960, 1280)
    im = ImageOps.fit(img, size_image, Image.ANTIALIAS)
    product.set_image(im, product_image.filename)

    # set image thumbnail for product
    size_thumb = (135, 180)
    im = ImageOps.fit(img, size_thumb, Image.ANTIALIAS)
    product.set_image_thumb(im, product_image.filename)

    # set image icon for product
    size_icon = (72, 96)
    im = ImageOps.fit(img, size_icon, Image.ANTIALIAS)
    product.set_image_icon(im, product_image.filename)

    # set video for product
    product.set_video(product_video, product_video.filename)

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


def update(product_id: int, title: str, description: str, price: int,
           category: str, stok: int):
    # get data product
    product = product_mdl.get_by_id(product_id=product_id)

    if product.is_deleted == 1:
        raise BadRequest("Product sudah dihapus")

    if title:
        product.title = title

    if description:
        product.description = description

    if price:
        product.price = price

    if category:
        product.category = category

    if stok:
        product.stok = stok

    db.session.add(product)
    db.session.flush()

    return product