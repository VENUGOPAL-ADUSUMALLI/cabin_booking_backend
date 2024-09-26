import json
from dataclasses import dataclass
from http.client import HTTPResponse

from django.http import HttpResponse


class CreateRefreshAccessTokensResponse:
    @staticmethod
    def invalid_refresh_token_response():
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Invalid refresh token"
            }
        ), status=400)

    @staticmethod
    def token_expired_response():
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Token expired please login again"
            }
        ), status=400)

    @staticmethod
    def get_refresh_access_token_success_response(refresh_access_token_dto):
        refresh_access_token_dict = {
            "access_token": str(refresh_access_token_dto.access_token)
        }
        return HttpResponse(json.dumps(refresh_access_token_dict), status=200)
