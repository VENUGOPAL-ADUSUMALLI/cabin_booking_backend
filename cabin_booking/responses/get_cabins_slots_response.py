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
    def get_cabin_slot_details_success_response(cabin_wise_slot_details_dtos):
        cabin_id_wise_slot_details_dict = {}
        for each_time_slot in cabin_wise_slot_details_dtos:
            cabin_id = each_time_slot.cabin_ids
            cabin_id_wise_slot_details_dict[cabin_id] = {
                "cabin_id": cabin_id,
                "time_slots": []
            }
            for time_slots in each_time_slot.time_slots:
                time_slot_dict = {
                    'slots': str(time_slots.slot),
                    "availability": time_slots.availability
                }
                cabin_id_wise_slot_details_dict[cabin_id]['time_slots'].append(time_slot_dict)
        response = list(cabin_id_wise_slot_details_dict.values())
        return HttpResponse(json.dumps(response, indent=4), status=200)





