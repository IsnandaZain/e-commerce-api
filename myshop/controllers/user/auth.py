import logging
from collections import namedtuple
from sqlalchemy import or_

from myshop.exceptions import BadRequest, Conflict, UserNotFound
from myshop.models import db, Users, UserTokens
from myshop.models import user as user_mdl
from myshop.models import user_token as user_token_mdl


def register(email: str, fullname: str, username: str, password: str, role: str):
    """Register new user

    Args:
        email: email user
        fullname: fullname user
        username: username user
        password: password user
        role: role user
    
    Returns:
        Users object
    """
    # check already use
    if Users.query.filter(
        or_(Users.email == email,
            Users.username == username)).first():
        raise Conflict("username atau email suadh dipakai akun lain")

    # save user
    user = Users(username, email, password, fullname)
    user.role = role

    db.session.add(user)
    db.session.flush()

    user.token = user_token_mdl.generate_token(user.id)
    
    return user


def login(identifier: str, password: str) -> Users:
    """Action user login

    Args:
        identifier: username atau email user
        password: password user
        
    Return:
        Users object
    """
    # get user info
    user = user_mdl.get_by_username_or_email(identifier)
    if user is None:
        raise UserNotFound

    # verify password
    if not user.verify_password(password):
        raise BadRequest("Password salah")

    user.token = user_token_mdl.get_by_id(user.id)

    return user