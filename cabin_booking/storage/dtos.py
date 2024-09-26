from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class UserDTO:
    token: str


@dataclass
class LoginResponseDTO:
    access_token: str
    refresh_token: str


@dataclass
class SignupResponseDTO:
    access_token: str
    refresh_token: str


@dataclass
class BookingProfileDTO:
    email: str
    username: str
    first_name: str
    last_name: str
    team_name: str
    contact_number: str
    purpose: str


@dataclass
class ProfileDTO:
    email: str
    username: str
    first_name: str
    last_name: str
    team_name: str
    contact_number: str


@dataclass
class UserPasswordUpdateDTO:
    user_id: str


@dataclass
class CabinDetailsDTO:
    cabin_id: str
    name: str
    cabin_type: str
    description: str


@dataclass
class FloorWiseCabinDetailsDTO:
    floor: str
    cabin: list[CabinDetailsDTO]


@dataclass
class AvailabilityDTO:
    availability: bool


@dataclass
class CabinTimeSlotsDTO:
    cabin_id: str
    time_slots: List[datetime.time]


@dataclass
class TimeDTO:
    start_date: datetime.date
    end_date: datetime.date
    time_slots: List[datetime.time]


@dataclass
class UserBookingDetails:
    floor_name: str
    cabin_name: str
    booking_id: str
    start_date: datetime.date
    end_date: datetime.date
    time_slots: List[datetime.time]


@dataclass
class CreateRefreshTokenDTO:
    access_token: str


@dataclass
class UpdateProfileDTO:
    username: str
    first_name: str
    last_name: str
    contact_number: str

    # def get_user_bookings_interactor(self, user_id):
    #     try:
    #         self.storage.validate_user_id(user_id)
    #     except InvalidUserException:
    #         return self.response.invalid_user_exception()
    #     user_bookings_dto = []
    #     try:
    #         user_bookings_details = self.storage.get_user_bookings(user_id)
    #     except NoBookingsException:
    #         return self.response.no_bookings_exception()
    #     for booking in user_bookings_details:
    #         for cabin_booking in booking.cabinbooking_set.all():
    #             time_slots = set()
    #             start_date_list = []
    #             for booking_slot in cabin_booking.bookingslot_set.all():
    #                 start_date_list.append(booking_slot.start_date_time.date())
    #                 time_slots.add(booking_slot.start_date_time.time())
    #                 unique_time_slots = sorted(set(time_slots))
    #                 cabin_details_dto = UserBookingDetails(
    #                     floor_name=cabin_booking.cabin.floor.name,
    #                     cabin_name=cabin_booking.cabin.name,
    #                     booking_id=booking.id,
    #                     start_date=start_date_list[0],
    #                     end_date=start_date_list[-1],
    #                     time_slots=unique_time_slots
    #                 )
    #                 if not start_date_list:
    #                     raise NoBookingsException()
    #                 user_bookings_dto.append(cabin_details_dto)
    #
    #     return user_bookings_dto