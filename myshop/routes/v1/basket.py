from flask import Blueprint, request, jsonify

from myshop.controllers import basket as basket_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs import auth


bp = Blueprint(__name__, "basket")

@bp.route("/basket/create_or_add", methods=["POST"])
def basket_create():
    product_id = request.form.get("product_id")
    total = request.form.get("total")

    product_ids = []
    # product_id separate with comma if more than one
    for i in product_id.split(","):
        product_ids.append(int(i))

    totals = []
    # total separate with comma if more than one
    for i in total.split(","):
        totals.append(int(i))

    if None in (product_id, total):
        raise BadRequest("terdapat komponen yang kosong")

    basket = basket_ctrl.create(
        user_id=auth.user.id,
        product_ids=product_ids,
        totals=totals,
    )

    response = {
        "status": 200,
        "id": basket.id,
    }

    return jsonify(response)


@bp.route("/basket/user/<int:user_id>", methods=["GET"])
def basket_by_user(user_id):
    """Get basket

    """
    basket = basket_ctrl.get_by_user(
        user_id=user_id
    )

    if not basket:
        response = {
            "status": 204,
            "message": "Keranjang tidak ditemukan"
        }

    else:
        response = {
            "status": 200,
            "id": basket.id,
            "user": basket.user_json,
            "basket_product": basket.basket_product_json,
            "created_on": basket.created_on.timestamp(),
        }

    return jsonify(response)


@bp.route("/basket/item/delete", methods=["POST"])
def basket_delete():
    basket_id = request.form.get("basket_id")
    product_id = request.form.get("product_id")

    product_ids = []
    # product_id separate with comma if more than one
    for i in product_id.split(","):
        product_ids.append(int(i))

    if None in (basket_id, product_id):
        raise BadRequest("terdapat komponen yang kosong")

    basket_ctrl.item_delete(
        basket_id=basket_id,
        product_ids=product_ids,
    )

    response = {
        "status": 200,
        "message": "Berhasil menghapus product dari keranjang"
    }

    return jsonify(response)