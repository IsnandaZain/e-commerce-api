from flask import Blueprint, request, jsonify

from datetime import datetime

from myshop.controllers.user import profile as profile_ctrl
from myshop.exceptions import BadRequest, NotFound
from myshop.libs import auth, validation


bp = Blueprint(__name__, "dashboard_user_profile")


@bp.route("/dashboard/user/profile", methods=["GET"])
def user_profile_list():
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")
    sort = request.args.get("sort", "-username")

    # type conversion
    page = int(page)
    count = int(count)

    user_profiles = profile_ctrl.list_profile(
        page=page,
        count=count,
        sort=sort,
    )

    result = []
    for user_profile in user_profiles.items:
        result.append({
            "id": user_profile.id,
            "username": user_profile.username,
            "fullname": user_profile.fullname,
            "email": user_profile.email,
            "phone_number": user_profile.phone_number,
            "avatar": user_profile.avatar_url,
        })

    response = {
        "status": 200,
        "has_next": user_profiles.has_next,
        "has_prev": user_profiles.has_prev,
        "profile": result,
        "total": user_profiles.total,
    }

    return jsonify(response)