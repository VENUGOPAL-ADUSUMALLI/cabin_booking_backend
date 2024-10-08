import json
from textwrap import indent

from django.http import HttpResponse


class LoginInteractorResponse:
    @staticmethod
    def invalid_user_response()-> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": '400',
                "error_message": "Invalid email id (don't have an account please signup to continue)"
            }, indent=4), status=400)

    @staticmethod
    def invalid_password_exception_response()-> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": '400',
            "error_message": "Invalid Password (please check your password)"
        }, indent=4), status=400)

    @staticmethod
    def user_login_dto_response(user_login_dto)-> HttpResponse:
        user_login_dict = {
            "access_token": str(user_login_dto.access_token),
            "refresh_token": str(user_login_dto.refresh_token)
        }
        return HttpResponse(json.dumps(user_login_dict, indent=4), status=200)
