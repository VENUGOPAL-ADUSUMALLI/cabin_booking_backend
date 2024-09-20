from cabin_booking.databases.booking_db import BookingDB
from cabin_booking.databases.dtos import UserBookingDetails
from cabin_booking.exception import InvalidUserException
from cabin_booking.responses.my_bookings_response import MyBookingsResponse


class MyBookingsInteractor:
    def __init__(self, storage: BookingDB, response: MyBookingsResponse):
        self.storage = storage
        self.response = response

    def get_user_my_bookings_interactor(self, user_id, ):
        try:
            self.storage.validate_user_id(user_id)
        except InvalidUserException:
            raise InvalidUserException()
        user_bookings_dto = []
        user_bookings_details = self.storage.get_user_bookings(user_id)
        for each in user_bookings_details:
            user_details_dto = UserBookingDetails(
                floor_name=each.floor_name,
                cabin_name=each.cabin_name,
                booking_id=each.booking_id,
                start_date=each.start_date,
                end_date=each.end_date,
                time_slots=each.time_slots
            )
            user_bookings_dto.append(user_details_dto)
        return self.response.my_bookings_success_response(user_bookings_dto)