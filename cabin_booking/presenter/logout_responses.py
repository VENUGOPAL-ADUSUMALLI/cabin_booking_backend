import json

from django.http import HttpResponse


class LogoutResponse:
    @staticmethod
    def invalid_refresh_token_response():
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Invalid refresh token"
            }
        ), status=400)

    @staticmethod
    def invalid_access_token_response():
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Invalid Access token"
            }
        ), status=400)

    @staticmethod
    def logout_success_response():
        return HttpResponse(json.dumps(
            {
                "error_code": "200",
                "error_message": "logged out successfully"
            }
        ), status=200)
