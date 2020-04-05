__author__ = "isndmz@gmail.com"


class MyShopException(Exception):
    """Indicates that the request could not be processed because of request in client is invalid"""
    
    message = __doc__.strip()
    status_code = 400
    payload = None

    def __init__(self, message=None, status_code=None, payload=None):

        if message is not None:
            self.message = message

        if status_code is not None:
            self.status_code = status_code

        if payload is not None:
            self.payload = payload

        super(MyShopException, self).__init__(self.message)

    def to_dict(self):
        res = {
            "message": self.message
        }

        if self.payload:
            for key, value in self.payload.items():
                res[key] = value
        
        return res


class BadRequest(MyShopException):
    """Indicates that the query was invalid.
    E.g. some parameter missing."""

    message = __doc__.strip()
    status_code = 400