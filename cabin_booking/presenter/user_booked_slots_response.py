import json

from django.http import HttpResponse

from cabin_booking.utils import user_details


class UserBookedSlotResponse:
    @staticmethod
    def invalid_cabin_id_response():
        return HttpResponse(json.dumps({
            "error_code": "400",
            "error_message": "Invalid Cabin id"
        }), status=400)

    @staticmethod
    def user_booked_slots_response(user_details_dto):
        user_details_dict = {
            "email": user_details_dto.email,
            "username": user_details_dto.username,
            "first_name": user_details_dto.first_name,
            "last_name": user_details_dto.last_name,
            "team_name": user_details_dto.team_name,
            "contact_number": user_details_dto.contact_number
        }
        return HttpResponse(json.dumps(user_details_dict), status=200)
