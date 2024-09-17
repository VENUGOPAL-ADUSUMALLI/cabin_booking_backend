import json

from django.http import HttpResponse


class UserProfileUpdateResponse:
    @staticmethod
    def invalid_email_exception():
        return HttpResponse(json.dumps({
            "error_message": "Invalid email ",
            "error_code": "400"
        }), status=400)
    #
    # @staticmethod
    # def invalid_user_details_exception():
    #     return HttpResponse(json.dumps({
    #         "error_message": "Invalid User Details",
    #         "error_code": "400"
    #     }), status=400)
    @staticmethod
    def update_user_profile_success_response():
        return HttpResponse(json.dumps({
            "error_message" : "Profile Updated Successfully",
            "error_code" : "200"
        }),status=200)

