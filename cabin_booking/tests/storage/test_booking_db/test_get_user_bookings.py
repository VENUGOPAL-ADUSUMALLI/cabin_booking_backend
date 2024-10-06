from datetime import date, time

import pytest

from cabin_booking.models import *
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.dtos import UserBookingDetailsDTO
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestGetUserBookings:
    @pytest.fixture()
    def user_db_storage_mock(self):
        return UserDB()

    @pytest.fixture()
    def create_cabin_slots(self, user_db_storage_mock):
        user = User.objects.create(
            username="user",
            email="testing@gmail.com",
            team_name="Booking DB test",
            first_name="Testing",
            last_name="Booking Db",
            contact_number="9835576526"
        )
        floor = [
            Floor(order=1, name="Ground Floor"),
        ]
        Floor.objects.bulk_create(floor)
        ground_floor = Floor.objects.get(name="Ground Floor")
        cabins = [
            Cabin(floor=ground_floor, name="Conference Room", type='CONFERENCE_ROOM',
                  description="Sufficient for 25 People", is_available=True),
        ]
        Cabin.objects.bulk_create(cabins)
        cabin_instance = Cabin.objects.get(name="Conference Room", floor=ground_floor)
        booking = Booking.objects.create(user=user, purpose="Meeting")
        cabin_booking = CabinBooking.objects.create(cabin=cabin_instance, booking=booking)
        booking_slot = BookingSlot.objects.create(start_date_time=datetime(2024, 10, 28, 18, 0),
                                                  end_date_time=datetime(2024, 10, 30, 19, 0),
                                                  cabin_booking=cabin_booking)

    def test_get_user_bookings(self, user_db_storage_mock, create_cabin_slots):
        user = User.objects.get(email="testing@gmail.com")
        booking = Booking.objects.get(user=user)
        storage = BookingDB(user_db_storage_mock)
        response = storage.get_user_bookings(user.user_id)
        for each in response:
            actual_dto = UserBookingDetailsDTO(
                floor_name=each.floor_name,
                cabin_name=each.cabin_name,
                booking_id=each.booking_id,
                start_date=each.start_date,
                end_date=each.end_date,
                time_slots=each.time_slots
            )
        expected_dto_from_db = UserBookingDetailsDTO(
            floor_name='Ground Floor',
            cabin_name='Conference Room',
            booking_id=booking.id,
            start_date=date(2024, 10, 28),
            end_date=date(2024, 10, 30),
            time_slots=[time(18, 0)]
        )
        assert actual_dto == expected_dto_from_db
