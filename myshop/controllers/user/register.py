from sqlalchemy import or_

from myshop.exceptions import BadRequest, Conflict
from myshop.models import db, Users
from myshop.models import user as user_mdl


def register(email: str, username: str, password: str, role: str):
    """Register new user

    Args:
        email: email user
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
    user = Users(username, email, password)
    user.fullname = username
    user.role = role
    db.session.add(user)
    db.session.flush()

    return user

