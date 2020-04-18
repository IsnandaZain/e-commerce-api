from flask import Blueprint, request, jsonify

from myshop.controllers import checkout as checkout_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs import auth


bp = Blueprint(__name__, "checkout")

@bp.route("/checkout/create_order", methods=["POST"])
def checkout_create_order():
    basket_id = request.form.get("basket_id")
    product_id = request.form.get("product_id")
    message = request.form.get("message")
    courir = request.form.get("courir")
    ongkir = request.form.get("ongkir")
    phone_number = request.form.get("phone_number")
    receiver_name = request.form.get("receiver_name")
    address = request.form.get("address")
    sub_total = request.form.get("sub_total")

    # type conversion
    basket_id = int(basket_id)
    ongkir = int(ongkir)
    sub_total = int(sub_total)

    product_ids = []
    # product id separate with comma if more than one
    for i in product_id.split(","):
        product_ids.append(int(i))

    if None in (basket_id, product_id, courir, ongkir, phone_number, receiver_name, address, sub_total):
        raise BadRequest("terdapat komponen yang kosong")

    checkout_data = checkout_ctrl.create_order(
        basket_id=basket_id,
        user_id=auth.user.id,
        product_ids=product_ids,
        message=message,
        courir=courir,
        ongkir=ongkir,
        phone_number=phone_number,
        receiver_name=receiver_name,
        address=address,
        sub_total=sub_total,
    )

    response = {
        "status": 200,
        "message": "Pesanan Berhasil dibuat"
    }

    return jsonify(response)


@bp.route("/checkout/user/<int:user_id>", methods=["GET"])
def checkout_by_user(user_id):
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")

    # type conversion
    page = int(page)
    count = int(count)
    
    checkout_datas = checkout_ctrl.get_by_user(
        user_id=user_id,
        page=page,
        count=count
    )
    
    result = []
    for checkout_data in checkout_datas.items:
        result.append({
            "id": checkout_data.id,
            "product": checkout_data.checkout_product_json,
            "receiver_name": checkout_data.receiver_name,
            "address": checkout_data.address,
            "phone_number": checkout_data.phone_number,
            "courir": checkout_data.courir,
            "ongkir": checkout_data.ongkir,
            "message": checkout_data.message,
            "sub_total": checkout_data.sub_total
        })

    response = {
        "status": 200,
        "checkout": result
    }

    return jsonify(response)