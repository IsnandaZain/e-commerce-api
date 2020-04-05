import random
import string
from typing import List

import pendulum
from passlib.hash import md5_crypt as pwd_context

from myshop.models import db
from configuration import MyShopConfig

STATIC_URL = MyShopConfig.STATIC_URL


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

    is_admin = db.Column(db.Boolean, default=False)

    role = db.Column(db.String, default="user")

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
