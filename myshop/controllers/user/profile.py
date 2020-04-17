import os

from datetime import datetime, date
from PIL import Image, ImageOps

from flask_sqlalchemy import Pagination
from werkzeug.datastructures import FileStorage

from myshop.exceptions import BadRequest, NotFound
from myshop.models import db, Users
from myshop.models import user as user_mdl
from myshop.libs import file

from configuration import MyShopConfig

STORAGE_PATH = MyShopConfig.STORAGE_PATH


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


def update_profile(user_id: int, username: str = None, fullname: str = None, gender: str = None, 
                   phone_number: str = None, email: str = None, birthday: date = None, avatar: FileStorage = None):
    # get user object
    user = user_mdl.get_by_id(user_id)
    if not user:
        raise NotFound("user %i not exist" % user_id)

    # update avatar
    if avatar:
        update_avatar(user, avatar)

    # update username
    if username:
        update_username(user, username)

    # update email
    if email:
        update_email(user, email)

    # update fullname
    if fullname:
        update_fullname(user, fullname)
    
    # update phone_number
    if phone_number:
        update_phone_number(user, phone_number)

    # update gender
    if gender:
        update_gender(user, gender)

    # update birthday
    if birthday:
        update_birthday(user, birthday)

    db.session.add(user)
    db.session.flush()

    return user


def update_avatar(user, avatar):
    """Update avatar user"""
    filename = file.safe_filename(filename=avatar.filename)
    name, ext = os.path.splitext(filename)
    img = Image.open(avatar)
    subdir = "%s/%s" % ("avatar", str(user.id))

    size_large = (1024, 1024)
    im_large = ImageOps.fit(img, size_large, Image.ANTIALIAS)
    filename_large = STORAGE_PATH + "/" + subdir + "/" + name + "_large." + ext
    im_large.save(filename_large)

    size_medium = (520, 520)
    im_medium = ImageOps.fit(img, size_medium, Image.ANTIALIAS)
    filename_medium = STORAGE_PATH + "/" + subdir + "/" + name + "_medium." + ext
    im_medium.save(filename_medium)

    size_small = (180, 180)
    im_small = ImageOps.fit(img, size_small, Image.ANTIALIAS)
    filename_small = STORAGE_PATH + "/" + subdir + "/" + name + "_small." + ext
    im_small.save(filename_small)

    user.avatar = name
    user.avatar_ext = ext

    return user


def update_username(user, username):
    """Update username user"""
    # check username sudah digunakan user lain
    another_user = user_mdl.get_by_username(username)
    if another_user:
        raise BadRequest("username sudah digunakan")

    user.username = username


def update_email(user, email):
    """Update email user"""
    # check email sudah digunakan user lain
    another_user = user_mdl.get_by_email(email=email)
    if another_user:
        raise BadRequest("email sudah digunakan")

    user.email = email


def update_fullname(user, fullname):
    """Update fullname user"""
    user.fullname = fullname


def update_phone_number(user, phone_number):
    """Update phone_number user"""
    user.phone_number = phone_number


def update_gender(user, gender):
    """Update gender user"""
    user.gender = gender


def update_birthday(user, birthday):
    """Update user birthday"""
    user.birthday = birthday