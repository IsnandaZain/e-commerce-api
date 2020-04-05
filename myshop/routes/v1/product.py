from flask import Blueprint, request, jsonify

from myshop.controllers import product as product_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs.ratelimit import ratelimit


bp = Blueprint(__name__, "product")

@bp.route("/product/create", methods=["POST"])
def product_create():
    """Create product

    **endpoint**

    .. sourcecode:: http

        POST /product/create
    
    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "id": ,
        }

    :form title: nama produk
    :form price: harga produk
    :form size_: [list] ukuran dari produk
    :form color_: [list] ketersediaan warna dari produk
    :form category: category dari produk (sepatu, baju, celana, tas)
    """
    title = request.form.get("title")
    price = request.form.get("price")
    size_ = request.form.get("size_")
    color_ = request.form.get("color_")
    category = request.form.get("category")

    if None in (title, price, size_, color_, category):
        raise BadRequest("terdapat komponen yang masih kosong")

    # type conversion
    price = int(price)

    size_list_ = []
    for size in size_:
        if not size.isdigit():
            raise BadRequest("nilai size bukan angka")
        
        size_list_.append(int(size))

    color_list_ = []
    for color in color_:
        color_list_.append(color)
    
    product = product_ctrl.create(
        title=title,
        price=price,
        size=size_list_,
        color=color_list_,
        category=category,
    )

    response = {
        "status": 200,
        "id": product.id,
    }

    return jsonify(response)

