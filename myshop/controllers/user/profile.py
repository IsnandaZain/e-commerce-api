from datetime import datetime

from flask_sqlalchemy import Pagination
from werkzeug.datastructures import FileStorage

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Users
from myshop.models import user as user_mdl

from configuration import MyShopConfig


def get_profile(user_id: int = None, username: str = None, user_actor: Users = None) -> Users:
    # make sure only admin and the user that only access
    if user_actor.role != "admin" or user_actor.id != user_id:
        raise BadRequest("Hanya admin dan si user yang dapat mengakses profile")

    if user_id:
        user = user_mdl.get_by_id(user_id)
    
    elif username:
        user = user_mdl.get_by_username(username)

    # check user exist
    if not user:
        raise NotFound("User tidak ditemukan")

    return user