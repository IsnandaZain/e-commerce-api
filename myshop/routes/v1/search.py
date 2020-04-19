from flask import Blueprint, request, jsonify

from myshop.controllers import search
from myshop.exceptions import BadRequest
from myshop.libs import auth


bp = Blueprint(__name__, "search")


@bp.route("/search/products")
def search_product():
    """Search

    """
    keyword = request.args.get("keyword")
    sort = request.args.get("sort", "match")
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")

    # type conversion
    page = int(page)
    count = int(count)

    if not keyword:
        raise BadRequest("keyword kosong")

    if sort and sort not in ("-id", "match"):
        raise BadRequest("Sorting tidak didukung")

    products = search.search_product(keyword=keyword, sort=sort, page=page, count=count)

    result = []
    for product in products.items:
        result.append({
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "user": {
                    "id": product.user.id,
                    "fullname": product.user.fullname,
                    "phone_number": product.user.phone_number,
                },
                "product_image": {
                    "image": product.image_url,
                    "thumb": product.image_thumb_url,
                    "icon": product.image_icon_url 
                },
                "stok": product.stok,
                "total_view": product.total_view,
                "total_review": product.total_review,
                "created_on": product.created_on.timestamp(),
            })

    response = {
        "status": 200,
        "result": result,
        "has_prev": products.has_prev if products else False,
        "has_next": products.has_next if products else False,
        "total": products.total if products else 0
    }

    return jsonify(response)


@bp.route("/search/users")
def search_user():
    """Search user

    """
    keyword = request.args.get("keyword")
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")
    role_ = request.args.get("role", "user")
    sort = request.args.get("sort", "match")

    if not keyword:
        raise BadRequest("keyword kosong")

    # type conversion
    page = int(page)
    count = int(count)

    users = search.search_user(keyword=keyword, sort=sort, page=page, count=count, role_=role_)

    result = []
    if users != None:
        for user in users.items:
            result.append({
                "status": 200,
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "email": user.email,
                "phone_number": user.phone_number,
                "avatar": user.avatar_url
            })

    response = {
        "status": 200,
        "result": result,
        "has_prev": users.has_prev if users else False,
        "has_next": users.has_next if users else False,
        "total": users.total if users else 0
    }

    return jsonify(response)