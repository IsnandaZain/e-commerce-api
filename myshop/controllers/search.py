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


def search_user(keyword: str, sort: str = "match", role_: str = "user",
                page: int = 1, count: int = 12):
    """Search user

    """
    keyword = keyword.strip(punctuation)
    if keyword == "":
        return None

    filters = [Users.username.like("%{}%".format(keyword))]

    if role_:
        role_map = {
            "user": Users.role == "user",
            "admin": Users.role == "admin"
        }

        filters.append(role_map[role_])

    sort_collections = {
        "-id": Users.id.desc(),
        "id": Users.id.asc(),
        "match": db.case(
            (
                (Users.username == keyword, 0),
                (Users.username.like("{}%".format(keyword)), 1),
                (Users.username.like("%{}%".format(keyword)), 2),
                (Users.username.like("%{}".format(keyword)), 3),
            ), else_=4
        ).asc()
    }

    sort_apply = sort_collections[sort]

    users = Users.query.filter(
        *filters
    ).order_by(
        sort_apply
    ).paginate(
        page=page,
        per_page=count,
        error_out=False
    )

    return users