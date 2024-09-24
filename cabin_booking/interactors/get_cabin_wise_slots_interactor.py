from datetime import time

from cabin_booking.constants.time_slots_constant import SLOT_BOOKING_START_TIME, SLOT_BOOKING_END_TIME
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.exception import InvalidCabinIDException
from cabin_booking.interactors.dtos import CabinTimeSlotsAvailabilityDTO, TimeSlotsDTO
from cabin_booking.presenter.get_cabins_slots_response import CabinSlotsDetailsResponse


class CabinWiseSlotsInteractor:
    def __init__(self, storage: BookingDB, response: CabinSlotsDetailsResponse):
        self.storage = storage
        self.response = response

    def get_cabin_slots_interactor(self, cabin_ids, start_date, end_date):
        try:
            self.storage.validate_cabin_id_for_cabin_slots(cabin_ids)
        except InvalidCabinIDException:
            return self.response.invalid_cabin_id_exception()
        cabin_slot_details_dtos = self.storage.get_cabin_slots(cabin_ids, start_date, end_date)

        cabin_id_wise_booked_slots = {}
        for dto in cabin_slot_details_dtos:
            cabin_id_wise_booked_slots[str(dto.cabin_id)] = dto.time_slots
        fixed_time_slots = []
        for each_hour in range(SLOT_BOOKING_START_TIME, SLOT_BOOKING_END_TIME):
            fixed_time_slots.append(time(each_hour, 0))

        cabin_id_available_slot_dtos = []
        for cabin_id in cabin_ids:
            time_slot_dtos = []
            for slot in fixed_time_slots:
                if slot in cabin_id_wise_booked_slots.get(cabin_id, []):
                    available = False
                else:
                    available = True

                time_slot_dtos.append(
                    TimeSlotsDTO(
                        slot=slot,
                        availability=available
                    )
                )
            cabin_id_available_slot_dtos.append(
                CabinTimeSlotsAvailabilityDTO(
                    cabin_id=cabin_id,
                    time_slots=time_slot_dtos
                )
            )

        return self.response.get_cabin_slot_details_success_response(cabin_id_available_slot_dtos)
