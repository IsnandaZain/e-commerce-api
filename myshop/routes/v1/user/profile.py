from flask import Blueprint, request, jsonify

from datetime import datetime

from myshop.controllers.user import profile as profile_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs import auth, validation


bp = Blueprint(__name__, "user_profile")

@bp.route("/user/profile/<username>", methods=["GET"])
@bp.route("/user/profile/<int:user_id>", methods=["GET"])
@bp.route("/user/profile")
def user_profile(user_id=None, username=None):
    """Get user profile

    """
    if auth.user:
        user_id = auth.user.id

    if not user_id and not username:
        raise BadRequest("Missing user_id or username")

    user = profile_ctrl.get_profile(user_id, username, auth.user)

    response = {
        "status": 200,
        "id": user.id,
        "username": user.username,
        "fullname": user.fullname,
        "email": user.email,
        "phone_number": user.phone_number,
        "avatar": user.avatar_url
    }

    return jsonify(response)


@bp.route("/user/profile", methods=["PUT"])
def user_profile_update():
    """Update user profile

    """
    email = request.form.get("email")
    username = request.form.get("username")
    gender = request.form.get("gender")
    fullname = request.form.get("fullname")
    birthday = request.form.get("birthday")
    phone_number = request.form.get("phone_number")
    avatar = request.files.get("avatar")
    
    if all(a is None for a in [email, gender, fullname, birthday, avatar]):
        raise BadRequest("Tidak ada komponen yang di isi")

    user_id = auth.user.id

    if username and not validation.username.match(username):
        raise BadRequest("username harus diantara 3 - 35 karakter")

    if fullname and not 3 <= len(fullname) <= 35:
        raise BadRequest("Panjang nama lengkap diantar 3 - 35 karakter")

    if email and not validation.email.match(email):
        raise BadRequest("email tidak valid")

    if gender:
        if gender not in ("m", "f"):
            raise BadRequest("Gender harus diantara m / f")
        else:
            gender = gender.lower()

    if birthday:
        try:
            birthday = int(birthday)
        except ValueError:
            raise BadRequest("Birthday menggunakan format epoch")

        birthday = datetime.fromtimestamp(birthday)

    profile_ctrl.update_profile(
        user_id=auth.user.id,
        username=username,
        fullname=fullname,
        email=email,
        gender=gender,
        birthday=birthday,
        phone_number=phone_number,
        avatar=avatar,
    )

    response = {
        "status": 200,
        "message": "Berhasil memperbarui profil"
    }

    return jsonify(response)