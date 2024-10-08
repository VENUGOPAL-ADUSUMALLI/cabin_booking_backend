from cabin_booking.exception import InvalidBookingIDException
from cabin_booking.presenter.delete_user_bookings_response import DeleteUserBookingsResponse
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


class DeleteUserBookings:
    def __init__(self, storage: BookingDB, user_db_storage: UserDB, response: DeleteUserBookingsResponse):
        self.storage = storage
        self.user_db_storage = user_db_storage
        self.response = response

    def delete_user_bookings_interactor(self, booking_id):
        try:
            self.storage.delete_user_bookings_db(booking_id)
        except InvalidBookingIDException:
            return self.response.invalid_booking_exception()

        response = self.response.slot_delete_success_response()
        return response
