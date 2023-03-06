from flask_restx._http import HTTPStatus
from flask_restx import marshal
from .models import error_response_model


def handle_exception(error, status_code: HTTPStatus):

    return marshal({
        "success": False,
        "data": [{
            "type": type(error).__name__,
            "message": str(error)
        }]
    }, error_response_model), status_code

