from django.http import HttpResponse

from cabin_booking.constants.config import order_types
from cabin_booking.presenter.cabin_details_response import CabinDetailsResponse
from cabin_booking.storage.cabin_db import CabinDB


class CabinDetailsInteractor:
    def __init__(self, storage: CabinDB, response: CabinDetailsResponse):
        self.storage = storage
        self.response = response

    def get_floor_wise_cabins_list(self) ->HttpResponse:
        floor_wise_cabins_details_dtos = self.storage.get_cabins_details()
        if not floor_wise_cabins_details_dtos:
            return self.response.something_went_wrong_exception()
        for each_dto in floor_wise_cabins_details_dtos:
            cabin_details_dto = each_dto.cabin
            sorted_cabin_details_dto = sorted(cabin_details_dto, key=lambda x: order_types.index(x.cabin_type))
            each_dto.cabin = sorted_cabin_details_dto
        response = self.response.cabin_details_success_response(floor_wise_cabins_details_dtos)
        return response
