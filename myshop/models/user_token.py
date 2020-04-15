import time
import pendulum
import uuid

import jwt

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from myshop.exceptions import NotFound, LogoutError
from myshop.models import db
from configuration import MyShopConfig

__author__ = "isndmz@gmail.com"


class UserTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Access token for request
    token = db.Column(db.String(255), unique=True)

    # user who grant access
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)

    is_deleted = db.Column(db.Boolean, default=0)

    created_on = db.Column(db.DateTime)

    user = relationship("Users", backref="user_tokens")

    def __init__(self, user_id):
        self.user_id = user_id
        self.token = self.gen_token(user_id)
        

        self.created_on = pendulum.now()

    def gen_token(self, user_id):
        """Generate token for access credential information

        Args:
            role: user role
            user_id: user id
        
        Returns:
            str token
        """
        token = Serializer(MyShopConfig.SECRET_KEY)
        return token.dumps({'user': self.user_id, 'nonce': uuid.uuid4().hex}).decode('utf-8')

    @staticmethod
    def validate(token):
        """Validate user token

        Args:
            token: token will be validate

        Returns:
            Users object
        
        Raises:
            NotFound: if user token not found
        """
        # check token secret in database
        user_token = UserTokens.query.filter_by(token=token).first()
        if not user_token:
            raise NotFound("Token not found in dabatase")

        if user_token.is_deleted:
            raise LogoutError("Please login again")

        return user_token.user


def generate_token(user_id: int) -> str:
    """Generate token"""
    user_token = UserTokens(user_id)
    db.session.add(user_token)
    db.session.flush()

    return user_token.token


def get_by_id(user_id: int) -> str:
    """Get token by id"""
    user_token = UserTokens.query.filter(
        UserTokens.user_id == user_id,
        UserTokens.is_deleted == 0,
    ).order_by(
        UserTokens.id.desc()
    ).first()

    return user_token.token