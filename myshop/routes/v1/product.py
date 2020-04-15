from flask import Blueprint, request, jsonify

from myshop.controllers import product as product_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs.ratelimit import ratelimit


bp = Blueprint(__name__, "product")

@bp.route("/product/<int:product_id>", methods=["GET"])
def product_get(product_id):
    """Get product

    """
    product = product_ctrl.get(
        product_id=product_id
    )

    response = {
        "status": 200,
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "user": {
            "id": product.user.id,
            "fullname": product.user.fullname,
            "phone_number": product.user.phone_number,
        },
        "stok": product.stok,
        "total_view": product.total_view,
        "total_review": product.total_review,
        "created_on": product.created_on.timestamp(),
    }

    return jsonify(response)


@bp.route("/product", methods=["GET"])
def product_list():
    """List products

    """
    page = request.form.get("page", "1")
    count = request.form.get("count", "12")
    category = request.form.get("category")
    sort = request.form.get("sort", "-id")

    # type conversion
    page = int(page)
    count = int(count)

    products = product_ctrl.list(
        page=page,
        count=count,
        category=category,
        sort=sort,
    )

    result = []
    if products != None:
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
                "stok": product.stok,
                "total_view": product.total_view,
                "total_review": product.total_review,
                "created_on": product.created_on.timestamp(),
            })

    response = {
        "status": 200,
        "has_next": products.has_next if products else False,
        "has_prev": products.has_prev if products else False,
        "products": result,
        "total": products.total if products else 0,
    }

    return jsonify(response)