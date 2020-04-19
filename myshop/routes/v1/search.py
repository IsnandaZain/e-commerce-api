from flask import Blueprint, request, jsonify

from myshop.controllers import search
from myshop.exceptions import BadRequest
from myshop.libs import auth


bp = Blueprint(__name__, "search")


@bp.route("/search/product")
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