import json

from django.http import HttpResponse


class UpdatePasswordResponse:
    @staticmethod
    def invalid_user_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": "400",
            "error_message": "invalid email id"
        }, indent=4), status=400)

    @staticmethod
    def invalid_password_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": "400'",
            "error_message": "Invalid Password"
        }, indent=4), status=400)

    @staticmethod
    def password_update_successfull_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": '200',
            "error_message": "password updated successfully"
        }, indent=4), status=200)
