from IPython import embed

from cabin_booking.databases.booking_db import BookingDB
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidCabinIDException, InvalidUserException
from cabin_booking.responses.cabin_confirm_slots_response import ConfirmSlotResponse


class ConfirmSlotInteractor:
    def __init__(self, storage: BookingDB, response: ConfirmSlotResponse, user_db_storage: UserDB):
        self.storage = storage
        self.response = response
        self.user_db_storage = user_db_storage

    def confirm_slot_interactor(self, cabin_id, start_date, end_date, purpose, user_id):
        try:
            self.storage.validate_cabin_id(cabin_id)
        except InvalidCabinIDException:
            return self.response.invalid_cabin_id_response()
        try:
            self.user_db_storage.validate_user_id(user_id)
        except InvalidUserException:
            return self.response.invalid_user_id_response()
        self.storage.create_cabin_slots(cabin_id, start_date, end_date, purpose, user_id)

        return self.response.create_confirm_slots_success_response()
