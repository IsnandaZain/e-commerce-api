from typing import List

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Users, ProductComments
from myshop.models import product as product_mdl
from myshop.models import product_comment as product_comment_mdl


def add(user: Users, product_id: int, comment_text: str):
    """Add comment

    """
    # make sure product is exist
    product = product_mdl.get_by_id(product_id=product_id)
    if not product:
        raise NotFound("Product tidak ditemukan")

    # create comment
    product_comment = ProductComments(
        product_id=product_id,
        text=comment_text,
        user_id=user.id,
    )

    db.session.add(product_comment)
    db.session.flush()

    return product_comment


def get_list(product_id: int, page: int = 1, count: int = 12):
    filters = [
        ProductComments.is_deleted == 0
    ]

    # get comment
    comment = ProductComments.query.filter(
        *filters
    ).order_by(
        ProductComments.id.desc()
    ).paginate(
        page=page,
        per_page=count,
        error_out=False
    )

    return comment


def delete(user_id: int, role: str, comment_id: int):
    # make sure comment exist
    comment = product_comment_mdl.get_by_id(comment_id=comment_id)
    if not comment:
        raise NotFound("Komentar tidak ditemukan")

    # check owner comment
    if comment.user_id != user_id and role != "admin":
        raise BadRequest("Tidak bisa menghapus komentar orang lain")

    comment.is_deleted = 1

    db.session.add(comment)
    db.session.flush()

    return comment