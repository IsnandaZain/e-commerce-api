from flask_sqlalchemy import Pagination

from string import punctuation
from myshop.models import db, Products, Users


def search_product(keyword: str, sort: str = "match", page: int = 1, count: int = 12):
    """Search product

    """
    keyword = keyword.strip(punctuation)
    if keyword == "":
        return None

    sort_collections = {
        "-id": Products.id.desc(),
        "match": db.case(
            (
                (Products.title == keyword, 0),
                (Products.title.like("{}%".format(keyword)), 1),
                (Products.title.like("%{}%".format(keyword)), 2),
                (Products.title.like("%{}".format(keyword)), 3),
            ), else_=4
        ).asc()
    }

    sort_apply = sort_collections[sort]

    product = Products.query.filter(
        Products.title.like("%{}%".format(keyword)),
        Products.is_deleted == 0,
    ).order_by(
        sort_apply
    ).paginate(
        page=page,
        per_page=count,
        error_out=False
    )

    return product