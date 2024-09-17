import json
from http.client import responses

from django.http import HttpResponse


class CabinSlotsDetailsResponse:
    @staticmethod
    def invalid_cabin_id_exception():
        return HttpResponse(json.dumps({
            "error_message": " Invalid Cabin Id",
            "error_code":"400"
        }),status=400)

    @staticmethod
    def get_cabin_slot_details_success_response(cabin_id_available_slot_dtos):
        cabins = []
        for each_time_slot in cabin_id_available_slot_dtos:
            cabin_id = each_time_slot.cabin_id
            time_slots = []
            for time_slot_dto in each_time_slot.time_slots:
                time_slot_dict = {
                    'slot': str(time_slot_dto.slot),
                    "availability": time_slot_dto.availability
                }
                time_slots.append(time_slot_dict)
            cabin= {
                "cabin_id": cabin_id,
                "time_slots": time_slots
            }
            cabins.append(cabin)

        return HttpResponse(json.dumps(cabins, indent=4), status=200)





