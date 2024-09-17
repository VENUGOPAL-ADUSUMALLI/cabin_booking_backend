from datetime import time

from cabin_booking.constants.time_slots_constant import SLOT_BOOKING_START_TIME, SLOT_BOOKING_END_TIME
from cabin_booking.databases.booking_db import BookingDB
from cabin_booking.databases.dtos import CabinTimeSlotsDTO, TimeSlotsDTO
from cabin_booking.exception import SomethingWentWrongException
from cabin_booking.responses.get_cabins_slots_response import CabinSlotsDetailsResponse


class CabinWiseSlotsInteractor:
    def __init__(self, storage: BookingDB, response: CabinSlotsDetailsResponse):
        self.storage = storage
        self.response = response

    def get_cabin_slots_interactor(self, cabin_ids, start_date, end_date):
        # cabin_id_validation = self.storage.validate_cabin_id(cabin_ids)
        # if not cabin_id_validation:
        #     return self.response.invalid_cabin_id_exception()
        cabin_slot_details_dtos = self.storage.get_cabin_slots(cabin_ids, start_date, end_date)
        fixed_time_slots = []
        for each_hour in range(SLOT_BOOKING_START_TIME, SLOT_BOOKING_END_TIME):
            fixed_time_slots.append(time(each_hour, 0))
        for each_time_slot in cabin_slot_details_dtos:
            for time_slots in each_time_slot.time_slots:
                time_slots.availability = True
                if time_slots.slot in fixed_time_slots:
                    time_slots.availability = False
        if not cabin_slot_details_dtos:
            for i in cabin_ids:
                cabin_slot_details_dtos.append(
                    CabinTimeSlotsDTO(
                        cabin_ids=i,
                        time_slots=[TimeSlotsDTO(
                            slot=j,
                            availability=True
                        )for j in fixed_time_slots]
                    )
                )
        return self.response.get_cabin_slot_details_success_response(cabin_slot_details_dtos)
