from flask import Blueprint, request, jsonify, send_file

from myshop.exceptions import BadRequest, NotFound
from myshop.libs.ratelimit import ratelimit
from configuration import MyShopConfig


bp = Blueprint(__name__, "files")

@bp.route("/file/<path:path_file>")
def get_files(path_file):
    str_path_file = ""
    for i in path_file.split("/"):
        str_path_file = str_path_file + "/" + i

    filename = path_file.split("/")[-1]

    path_file_send = MyShopConfig.STORAGE_PATH + str_path_file

    return send_file(path_file_send, attachment_filename=filename)