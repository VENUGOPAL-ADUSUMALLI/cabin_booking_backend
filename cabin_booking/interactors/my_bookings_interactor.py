from cabin_booking.databases.booking_db import BookingDB
from cabin_booking.exception import InvalidUserException


class MyBookingsInteractor:
    def __init__(self,storage:BookingDB):
        self.storage = storage
    def get_user_my_bookings_interactor(self,user_id):
        try:
            self.storage.validate_user_id(user_id)
        except InvalidUserException:
            raise InvalidUserException()
        user_bookings_details = self.storage.get_user_bookings(user_id)
