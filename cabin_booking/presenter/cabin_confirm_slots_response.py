import json

from django.http import HttpResponse


class ConfirmSlotResponse:
    @staticmethod
    def invalid_cabin_id_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": "400",
            "error_message": "Invalid Cabin id"
        }, indent=4), status=400)

    @staticmethod
    def invalid_user_id_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": "400",
            "error_message": "Invalid User Id"
        }, indent=4), status=400)

    @staticmethod
    def create_confirm_slots_success_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": "200",
            "error_message": "slot Booked Successfully"
        }, indent=4), status=200)

    @staticmethod
    def uniques_constraint_response() -> HttpResponse:
        return HttpResponse(json.dumps({
            "error_message": "slot already Booked",
            "status": 400
        }, indent=4), status=400)
