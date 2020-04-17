import os
from pathlib import Path

current_dir = Path(__file__).parent

def getenv(key, default=None, func=None):
    """Get environment variabel return None if not exists
    Args:
        key: key os environment
        default: default value if not exists
        func: apply function in env
    """
    val = os.getenv(key, default)
    if func:
        val = func(val)
    return val


class MyShopConfig(object):
    """MyShop Configuration"""
    # flask debug configuration
    DEBUG = getenv("DEBUG", False, bool)

    # static url for access assets
    STATIC_URL = "http://127.0.0.1:5000/file"
    STORAGE_PATH = getenv("STORAGE_PATH", "/var/www/html/file")

    DEFAULT_AVATAR = STATIC_URL + "/default/avatar_default_{size}.jpg"

    INTERNAL_TOKEN = "bnsultjhbqyydugtjvchrioszozwxmlpcocdmjdv"

    # database config
    MYSQL_HOST = getenv("DB_HOST", "127.0.0.1")
    MYSQL_USER = getenv("DB_USER", "root")
    MYSQL_PASS = getenv("DB_PASS", "")
    MYSQL_DBNAME = getenv("DB_NAME", "myshop")
    MYSQL_PORT = getenv("DB_PORT", 3306, int)

    # sqlalchemy
    # mysql://username:password@server:port/db
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (
        MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False, bool)
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 60
    SQLALCHEMY_MAX_OVERFLOW = 20

    # redis config
    REDIS_HOST = getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = getenv("REDIS_PORT", "6379")

    # max file upload 100mb
    MAX_CONTENT_LENGTH = getenv("MAX_CONTENT_LENGTH", 100 * 1024 * 1024, int)

    # WEB frontend configuration
    WEB_URL = getenv("WEB_URL", "http://localhost:5000")

    # secret key
    SECRET_KEY = getenv("SECRET_KEY", "secretkeymyshopapi")

    # Konfigurasi logging yang menampilkan log level INFO (INFO, ERROR, WARNING)
    # Console :
    # output : "INFO 2020-04-04 15:45:55,126 - myshop.route.v1.error - error.py:12: error authentifikasi"
    LOG_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(levelname)s] %(asctime)s - %(name)s - %(filename)s:%(lineno)d: %(message)s", 
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": getenv("LOG_LEVEL", "INFO"),
                "formatter": "verbose",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "*": {
                "propagate": False,
                "handlers": ["console"]
            }
        },
        "root": {
            "level": getenv("LOG_LEVE", "INFO"),
            "handlers": [
                "console"
            ]
        }
    }