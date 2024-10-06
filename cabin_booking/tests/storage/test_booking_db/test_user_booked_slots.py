import pytest

from cabin_booking.models import *
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.dtos import BookingProfileDTO
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestCheckUserBookedSlots:
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

    def test_user_booked_slot(self, user_db_storage_mock, create_cabin_slots):
        cabin_instance_id = Cabin.objects.get(name="Conference Room")
        start_date_time = "2024-10-28 18:00"
        end_date_time = "2024-10-29 19:00"
        storage = BookingDB(user_db_storage_mock)
        response = storage.get_user_booked_slot(cabin_instance_id.id, start_date_time, end_date_time)
        actual_dto = BookingProfileDTO(
            email=response.email,
            first_name=response.first_name,
            last_name=response.last_name,
            username=response.username,
            team_name=response.team_name,
            contact_number=response.contact_number,
            purpose=response.purpose
        )
        expected_dto_from_db = BookingProfileDTO(
            email="testing@gmail.com",
            first_name="Testing",
            last_name="Booking Db",
            username="user",
            team_name="Booking DB test",
            contact_number="9835576526",
            purpose="Meeting"
        )
        assert actual_dto == expected_dto_from_db
