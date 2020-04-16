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