import pendulum

from typing import List
from flask_sqlalchemy import Pagination

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Baskets, BasketProducts
from myshop.models import basket as basket_mdl
from myshop.models import basket_product as basket_product_mdl
from myshop.models import product as product_mdl


def create(user_id: int, product_ids: List[int], totals: List[int]):
    # check apakah user sudah memiliki keranjang
    basket = basket_mdl.get_by_userid(user_id=user_id)
    if not basket:
        # create keranjang baru
        basket = Baskets(
            user_id=user_id
        )

        db.session.add(basket)
        db.session.flush()
    else:
        basket.updated_on = pendulum.now()

    # create keranjang product
    for i in range(len(product_ids)):
        # make sure product is exist
        product = product_mdl.get_by_id(product_id=product_ids[i])

        if not product:
            raise BadRequest("Product yang diinputkan sudah tidak tersedia")
        else:
            basket_product = BasketProducts(
                basket_id=basket.id,
                product_id=product_ids[i],
                total=totals[i]
            )

            db.session.add(basket_product)
            db.session.flush()

    return basket
