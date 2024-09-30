from datetime import datetime, timedelta

from django.utils import timezone

from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB
from cabin_booking.exception import InvalidCabinIDException, InvalidUserException, UniqueConstraintException
from cabin_booking.interactors.dtos import StartEndDateTimeDTO
from cabin_booking.presenter.cabin_confirm_slots_response import ConfirmSlotResponse


class ConfirmSlotInteractor:
    def __init__(self, storage: BookingDB, response: ConfirmSlotResponse, user_db_storage: UserDB):
        self.storage = storage
        self.response = response
        self.user_db_storage = user_db_storage

    def confirm_slot_interactor(self, cabin_id, start_date, end_date, purpose, user_id, time_slots):
        try:
            self.storage.validate_cabin_id(cabin_id)
        except InvalidCabinIDException:
            return self.response.invalid_cabin_id_response()
        try:
            self.user_db_storage.validate_user_id(user_id)
        except InvalidUserException:
            return self.response.invalid_user_id_response()
        convert_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        convert_end_date = datetime.strptime(end_date, "%Y-%m-%d")
        converted_time_slots = []
        for each_slot in time_slots:
            converted_time_slots.append(datetime.strptime(each_slot, "%H:%M"))
        user_already_booked_slots = self.storage.check_user_already_booked_slots(cabin_id, convert_start_date, convert_end_date,
                                                                         converted_time_slots)
        if user_already_booked_slots:
            return self.response.uniques_constraint_response()

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date_day = start_date.date()
        end_date_day = end_date.date()
        list_start_end_date_time_dto = []
        for date in range((end_date_day - start_date_day).days + 1):
            current_day = start_date + timedelta(days=date)
            for each_slot in time_slots:
                time = datetime.strptime(each_slot, "%H:%M").time()
                start_date_time = datetime.combine(current_day, time)
                end_date_time = start_date_time + timedelta(hours=1)
                start_end_date_time_dto = StartEndDateTimeDTO(
                    start_date_time=start_date_time,
                    end_date_time=end_date_time
                )
                list_start_end_date_time_dto.append(start_end_date_time_dto)

        self.storage.create_cabin_slots(cabin_id, purpose, user_id, list_start_end_date_time_dto)

        return self.response.create_confirm_slots_success_response()
