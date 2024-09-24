import json

from django.http import HttpResponse


class UpdatePasswordResponse:
    @staticmethod
    def invalid_user_response():
        return HttpResponse(json.dumps({
            "error_code": "400",
            "error_message": "invalid user"
        }), status=400)

    @staticmethod
    def invalid_password_response():
        return HttpResponse(json.dumps({
            "error_code": "400'",
            "error_message": "Invalid Password"
        }), status=400)

    @staticmethod
    def password_update_successfull_response():
        return HttpResponse(json.dumps({
            "error_code": '200',
            "error_message": "password updated successfully"
        }), status=200)
