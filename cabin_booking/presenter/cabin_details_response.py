import json

from django.http import HttpResponse


class CabinDetailsResponse:
    @staticmethod
    def something_went_wrong_exception()->HttpResponse:
        return HttpResponse(json.dumps({
            "error_code": "400",
            "error_message": "something went wrong"
        }, indent=4), status=400)

    @staticmethod
    def cabin_details_success_response(floor_wise_cabins_details_dtos)->HttpResponse:
        get_floor_wise_cabins_dict = {}
        for each in floor_wise_cabins_details_dtos:
            floor_name = each.floor
            if floor_name not in get_floor_wise_cabins_dict:
                get_floor_wise_cabins_dict[floor_name] = {
                    "floor_name": floor_name,
                    "cabins": []
                }
            for cabin in each.cabin:
                cabin_dict = {
                    "cabin_id": str(cabin.cabin_id),
                    "cabin_name": cabin.name,
                    "cabin_type": cabin.cabin_type,
                    "description": cabin.description
                }
                get_floor_wise_cabins_dict[floor_name]["cabins"].append(cabin_dict)
        response = list(get_floor_wise_cabins_dict.values())
        return HttpResponse(json.dumps(response, indent=4), status=200)
