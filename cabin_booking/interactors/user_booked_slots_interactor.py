from cabin_booking.exception import InvalidCabinIDException, InvalidUserException, InvalidDateRangeException, \
    SomethingWentWrongException, InvalidDetailsException
from cabin_booking.presenter.user_booked_slots_response import UserBookedSlotResponse
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.dtos import BookingProfileDTO


class UserBookedSlotsInteractor:
    def __init__(self, storage: BookingDB, response: UserBookedSlotResponse):
        self.storage = storage
        self.response = response

    def user_booked_slot_interactor(self, cabin_id, start_date_time, end_date_time):
        try:
            self.storage.validate_cabin_id(cabin_id)
        except InvalidCabinIDException:
            return self.response.invalid_cabin_id_response()
        try:
            profile_details_dto = self.storage.get_user_booked_slot(cabin_id, start_date_time, end_date_time)
        except InvalidDetailsException:
            return self.response.invalid_details_exception()
        user_details_dto = BookingProfileDTO(
            email=profile_details_dto.email,
            username=profile_details_dto.username,
            first_name=profile_details_dto.first_name,
            last_name=profile_details_dto.last_name,
            team_name=profile_details_dto.team_name,
            contact_number=profile_details_dto.contact_number,
            purpose=profile_details_dto.purpose
        )
        response = self.response.user_booked_slots_response(user_details_dto)
        return response
