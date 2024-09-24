from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.dtos import ProfileDTO
from cabin_booking.exception import InvalidCabinIDException
from cabin_booking.presenter.user_booked_slots_response import UserBookedSlotResponse
from cabin_booking.utils import user_details


class UserBookedSlotsInteractor:
    def __init__(self, storage: BookingDB,response:UserBookedSlotResponse):
        self.storage = storage
        self.response = response

    def user_booked_slot(self, cabin_id, start_date_time, end_date_time):
        try:
            self.storage.validate_cabin_id(cabin_id)
        except InvalidCabinIDException:
            return self.response.invalid_cabin_id_response()
        profile_details_dto = self.storage.get_user_booked_slot(cabin_id,start_date_time,end_date_time)
        for each_details  in profile_details_dto:
            user_details_dto = ProfileDTO(
                email= each_details.email,
                first_name= each_details.first_name,
                last_name= each_details.last_name,
                username=each_details.username,
                team_name=each_details.team_name,
                contact_number=each_details.contact_number,
                purpose= each_details.purpose

            )
            response= UserBookedSlotResponse().user_booked_slots_response(user_details_dto)
            return response
