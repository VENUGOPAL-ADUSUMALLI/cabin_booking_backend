import json

from django.http import HttpResponse


class ProfileInteractorResponse:
    @staticmethod
    def invalid_user_response()-> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": 400,
            "error_message": "Invalid User"
        }, indent=4), status=400)

    @staticmethod
    def user_details_dto_response(user_dto)-> HttpResponse:
        user_profile_dict = {
            "email": user_dto.email,
            "username": user_dto.username,
            "first_name": user_dto.first_name,
            "last_name": user_dto.last_name,
            "team_name": user_dto.team_name,
            "contact_number": user_dto.contact_number

        }
        return HttpResponse(json.dumps(user_profile_dict,indent=4), status=200)
