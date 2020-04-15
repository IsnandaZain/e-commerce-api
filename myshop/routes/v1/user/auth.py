from flask import Blueprint, request, jsonify

from myshop.controllers.user import auth as auth_ctrl
from myshop.exceptions import BadRequest
from myshop.libs import auth, validation
from myshop.libs.ratelimit import ratelimit

bp = Blueprint(__name__, "user_auth")


@bp.route("/user/register", methods=["POST"])
@ratelimit(300)
def user_register():
    """Register user baru

    **endpoint**

    .. sourcecode:: http

        POST /user/register

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-type: text/javascript

        {
            "status": 200,
            "user_token": "uytbchdhsuyroqjeoajosd",
            "user" : {
                "id": 1,
                "username": "isnanda",
                "avatar": {
                    "large": "",
                    "medium": "",
                    "small": "",
                },
                "is_admin": false,
            }
        }

    :form email: user email
    :form username: username register (3-35 karater, alfanumerik dan _ )
    :form password: password user (min 8 karakter)
    """
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role", "user")

    # raise exception if mandatory variabel is None
    if None in (email, username, password):
        raise BadRequest("email, username atau password kosong")

    # check email pattern
    if not validation.email.match(email):
        raise BadRequest("email tidak valid")

    # validation username (3-35 char, alfanumerik dan _ )
    if not validation.username.match(username):
        raise BadRequest("Username harus diantara 3 - 35 karakter, alfanumerik atau _ ")

    # validate password (min 8 char)
    if len(password) < 8:
        raise BadRequest("Kata sandi minimal 8 karakter")

    user = auth_ctrl.register(
        email=email,
        username=username,
        password=password,
        role=role,
    )

    response = {
        "status": 200,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }
    }

    return jsonify(response)


@bp.route("/user/login", methods=["POST"])
@ratelimit(300)
def user_login():
    """Login user untuk mendapatkan user token

    **endpoint**

    .. sourcecode:: http

        POST /user/login

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "user": {
                "id": 1,
                "username": "isnanda",
                "role": "user",
            }
        }

    :form username: username atau email user
    :form password: password user
    """
    username = request.form.get("username")
    password = request.form.get("password")

    # check mandatory
    if None in (username, password):
        raise BadRequest("Username atau password kosong")

    user = auth_ctrl.login(identifier=username, password=password)

    response = {
        "status": 200,
        "user_token": user.token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }
    }

    return jsonify(response)