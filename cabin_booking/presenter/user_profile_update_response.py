import json

from django.http import HttpResponse


class UserProfileUpdateResponse:
    @staticmethod
    def invalid_user_exception():
        return HttpResponse(json.dumps({
            "error_message": "Invalid user",
            "error_code": "400"
        }), status=400)

    @staticmethod
    def update_user_profile_success_response():
        return HttpResponse(json.dumps({
            "error_message": "Profile Updated Successfully",
            "error_code": "200"
        }), status=200)
