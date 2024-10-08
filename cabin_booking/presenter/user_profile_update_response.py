import json

from django.http import HttpResponse


class UserProfileUpdateResponse:
    @staticmethod
    def invalid_user_exception() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_message": "Invalid user",
            "error_code": "400"
        }, indent=4), status=400)

    @staticmethod
    def update_user_profile_success_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_message": "Profile Updated Successfully",
            "error_code": "200"
        }, indent=4), status=200)
