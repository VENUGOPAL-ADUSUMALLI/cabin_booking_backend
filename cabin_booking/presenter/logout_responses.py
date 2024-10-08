import json

from django.http import HttpResponse


class LogoutResponse:
    @staticmethod
    def invalid_refresh_token_response() -> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Invalid refresh token"
            }
            , indent=4), status=400)

    @staticmethod
    def invalid_access_token_response() -> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Invalid Access token"
            }
            , indent=4), status=400)

    @staticmethod
    def logout_success_response() -> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": "200",
                "error_message": "logged out successfully"
            }
            , indent=4), status=200)
