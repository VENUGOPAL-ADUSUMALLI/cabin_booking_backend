import json

from django.http import HttpResponse


class ConfirmSlotResponse:
    @staticmethod
    def invalid_cabin_id_response():
        return HttpResponse(json.dumps({
            "error_code":"400",
            "error_message":"Invalid Cabin id"
        }),status=400)
    @staticmethod
    def invalid_user_id_response():
        return HttpResponse(json.dumps({
            "error_code":"400",
            "error_message" : "Invalid Canin Id"
        }),status=400)
    @staticmethod
    def create_confirm_slots_success_response():
        return HttpResponse(json.dumps({
            "error_code" : "200",
            "error_message" : "slot Booked Successfully"
        }),status=200)

    @staticmethod
    def uniques_constraint_response():
        return HttpResponse(json.dumps({
            "error_message": "slot already Booked",
            "status": 400
        }), status=400)