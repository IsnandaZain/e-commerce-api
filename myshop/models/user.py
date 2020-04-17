import random
import string
from typing import List

import pendulum
from passlib.hash import md5_crypt as pwd_context
from sqlalchemy import or_

from myshop.models import db
from configuration import MyShopConfig

STATIC_URL = MyShopConfig.STATIC_URL
DEFAULT_AVATAR = MyShopConfig.DEFAULT_AVATAR


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    username = db.Column(db.String(35), unique=True, nullable=False)
    email = db.Column(db.String(120))
    password = db.Column(db.String(255))

    # gender (m/l)
    gender = db.Column(db.String(1), default="")
    
    fullname = db.Column(db.String(255), default="")

    # day born user
    birthday = db.Column(db.DateTime)

    # user phone number
    phone_number = db.Column(db.String(15), default="0")

    # avatar
    avatar = db.Column(db.String(50), default="")
    avatar_ext = db.Column(db.String(5), default="")

    role = db.Column(db.String(20), default="user")

    created_on = db.Column(db.DateTime)

    ROLE_ADMINISTRATOR = "administrator"
    def __init__(self, username, email=None, password=None, fullname=None, id=None):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.id = id

        # hash password
        if password:
            self.set_password(password)

        self.created_on = pendulum.now()

    
    @property
    def birthday_timestamp(self):
        if self.birthday:
            return self.birthday.timestamp()
        return 0

    @property
    def avatar_url(self):
        if self.avatar == "" or self.avatar == None:
            large = DEFAULT_AVATAR.format(size="large")
            medium = DEFAULT_AVATAR.format(size="medium")
            small = DEFAULT_AVATAR.format(size="small")

        else:
            large = "%s/avatar/%s/%s_large.%s" % (STATIC_URL, self.id, self.avatar, self.avatar_ext)
            medium = "%s/avatar/%s/%s_medium.%s" % (STATIC_URL, self.id, self.avatar, self.avatar_ext)
            small = "%s/avatar/%s/%s_small.%s" % (STATIC_URL, self.id, self.avatar, self.avatar_ext)

        return {
            "large": large,
            "medium": medium,
            "small": small
        }

    def set_password(self, password: str):
        """Set user password

        Args:
            password: new password
        """
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password) -> bool:
        """Verify hash password

        Args:
            password: hash password

        Returns:
            bool (True or False)
        """
        return pwd_context.verify(password, self.password)


def get_by_username_or_email(identifier: str) -> Users:
    """Get user by username or email

    Args:
        identifier: username or email user

    Returns:
        Users object
    """
    return Users.query.filter(
        or_(
            Users.username == identifier,
            Users.email == identifier
        )
    ).first()


def get_by_id(user_id: int) -> Users:
    """Get user by user_id

    Args:
        user_id: id user
    
    Return:
        Users object
    """
    return Users.query.filter_by(id=user_id).first()

def get_by_username(username: str) -> Users:
    """Get user by username or email

    Args:
        username: username user

    Return:
        Users object
    """
    return Users.query.filter_by(username=username).first()

def get_by_email(email: str) -> Users:
    """Get user by email

    Args:
        email: email user

    Return:
        Users object
    """
    return Users.query.filter_by(email=email).first()