from flask import Blueprint, request, jsonify

from myshop.controllers import product as product_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs.ratelimit import ratelimit
from myshop.libs import auth


bp = Blueprint(__name__, "dashboard_product")

@bp.route("/dashboard/product/create", methods=["POST"])
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
    description = request.form.get("description")
    price = request.form.get("price")
    category = request.form.get("category")
    stok = request.form.get("stok")
    product_image = request.files.get("product_image")
    product_video = request.files.get("product_video")

    if None in (title, description, price, category, stok, product_image, product_video):
        raise BadRequest("terdapat komponen yang masih kosong")

    # type conversion
    price = int(price)
    
    product = product_ctrl.create(
        title=title,
        description=description,
        price=price,
        category=category,
        stok=stok,
        user_id=auth.user.id,
        product_image=product_image,
        product_video=product_video,
    )

    response = {
        "status": 200,
        "id": product.id,
        "title": product.title,
    }

    return jsonify(response)


@bp.route("/dashboard/product/update/<int:product_id>", methods=["PUT"])
def product_update(product_id):
    """Update product

    """
    title = request.form.get("title")
    description = request.form.get("description")
    price = request.form.get("price")
    category = request.form.get("category")
    stok = request.form.get("stok")

    total_component = sum(bool(i) for i in (title, description, price, category, stok))
    if total_component == 0:
        raise BadRequest("Tidak ada data yang diubah")

    # type conversion
    if price:
        price = int(price)

    if stok:
        stok = int(stok)

    product = product_ctrl.update(
        product_id=product_id,
        title=title,
        description=description,
        price=price,
        category=category,
        stok=stok
    )

    response = {
        "status": 200,
        "message": "Berhasil mengupdate product"
    }

    return jsonify(response)


@bp.route("/dashboard/product/<int:product_id>", methods=["GET"])
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
        "user": product.user_json,
        "product_image": {
            "image": product.image_url,
            "thumb": product.image_thumb_url,
            "icon": product.image_icon_url,
        },
        "stok": product.stok,
        "total_view": product.total_view,
        "total_review": product.total_review,
        "created_on": product.created_on.timestamp(),
    }

    return jsonify(response)


@bp.route("/dashboard/product/delete/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    """Delete product

    """
    product = product_ctrl.delete(
        product_id=product_id
    )

    response = {
        "status": 200,
        "message": "Berhasil menghapus product"
    }

    return jsonify(response)


@bp.route("/dashboard/product", methods=["GET"])
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