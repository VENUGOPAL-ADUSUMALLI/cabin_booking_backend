import json

from django.http import HttpResponse


class SignupInteractorResponse:
    @staticmethod
    def user_already_exists_response():
        return HttpResponse(json.dumps({
            "error_message": "User Already exist",
            "status": 400
        }), status=400)
    @staticmethod
    def uniques_constraint_response(e):
        return HttpResponse(json.dumps({
            "error_message": str(e),
            "status": 400
        }), status=400)
    @staticmethod
    def user_signup_dto_response(user_signup_dto):
        response_dict = {
            "access_token": str(user_signup_dto.access_token),
            "refresh_token": str(user_signup_dto.refresh_token)
        }
        return HttpResponse(json.dumps(response_dict),
                            status=200)


