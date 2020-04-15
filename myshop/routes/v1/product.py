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
        "pricce": product.price,
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

