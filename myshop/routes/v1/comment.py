from flask import Blueprint, request, jsonify

from myshop.controllers import comment as comment_ctrl
from myshop.exceptions import BadRequest
from myshop.libs import auth

bp = Blueprint(__name__, "product_comment")


@bp.route("/product/comment/<int:product_id>", methods=["POST"])
def product_comment_add(product_id: int):
    """Create comment product

    """
    comment_text = request.form.get("comment")

    if not comment_text:
        raise BadRequest("komentar wajib diisi")
    elif len(comment_text.strip()) == 0:
        raise BadRequest("komentar wajib diisi")

    if not len(comment_text) <= 255:
        raise BadRequest("Maksimal panjang komentar 255 karakter")

    comment = comment_ctrl.add(
        user=auth.user,
        product_id=product_id,
        comment_text=comment_text
    )

    response = {
        "status": 200,
        "id": comment.id,
        "text": comment.text,
        "user": comment.user_json,
        "product": comment.product_json,
        "created_at": comment.created_on.timestamp(),
    }

    return jsonify(response)


@bp.route("/product/comment/<int:product_id>", methods=["GET"])
def product_comment_list(product_id: int):
    """List comment product

    """
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")
    
    # type conversion
    page = int(page)
    count = int(count)

    comments = comment_ctrl.get_list(
        product_id=product_id,
        page=page,
        count=count,
    )

    result = []
    for comment in comments.items:
        result.append({
            "id": comment.id,
            "text": comment.text,
            "user": comment.user_json,
            "product": comment.product_json,
            "created_at": comment.created_on.timestamp(),
        })

    response = {
        "status": 200,
        "comment": result,
        "total": comments.total,
    }

    return jsonify(response)



@bp.route("/product/comment/<int:comment_id>", methods=["DELETE"])
def product_comment_delete(comment_id: int):
    """Delete comment product
    
    """
    comment = comment_ctrl.delete(
        role=auth.user.role,
        user_id=auth.user.id,
        comment_id=comment_id
    )

    response = {
        "status": 200,
        "message": "Berhasil menghapus komentar"
    }

    return jsonify(response)