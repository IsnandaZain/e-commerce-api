import pendulum

from typing import List

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Checkouts, Baskets, BasketProducts
from myshop.models import basket as basket_mdl
from myshop.models import basket_product as basket_product_mdl
from myshop.models import checkout as checkout_mdl


def create_order(user_id: int, basket_id: int, product_ids: List[int], message: str, courir: str,
           ongkir: int, phone_number: str, receiver_name: str, address: str, sub_total: int):
    checkout_data = Checkouts(
        user_id=user_id,
        receiver_name=receiver_name,
        address=address,
        phone_number=phone_number,
        courir=courir,
        ongkir=ongkir,
        message=message,
        sub_total=sub_total
    )    

    db.session.add(checkout_data)
    db.session.flush()

    # update basket_products to checkout
    reduce_sub_total = 0
    for product_id in product_ids:
        product_to_checkout = basket_product_mdl.get_by_basket_and_product(basket_id=basket_id, product_id=product_id)

        product_to_checkout.is_checkout = 1
        product_to_checkout.is_deleted = 1
        product_to_checkout.checkout_id = checkout_data.id
        db.session.add(product_to_checkout)
        db.session.flush()
        
    return checkout_data


def get_by_user(user_id: int, page: int = 1, count: int = 12):
    checkout_data = Checkouts.query.filter(
        Checkouts.user_id == user_id,
        Checkouts.is_deleted == 0,
    ).order_by(
        Checkouts.id.desc()
    ).paginate(
        page=page,
        per_page=count,
        error_out=False
    )

    return checkout_data