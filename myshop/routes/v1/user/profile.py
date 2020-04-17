from flask import Blueprint, request, jsonify

from myshop.controllers.user import profile as profile_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs import auth


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
    }

    return jsonify(response)