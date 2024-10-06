import datetime
from datetime import date, time

import pytest

from cabin_booking.models import *
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestCheckUserAlreadyBookedSlots:
    @pytest.fixture()
    def user_db_storage(self):
        return UserDB()

    @pytest.fixture()
    def create_cabin_slots(self, user_db_storage):
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
                                                  end_date_time=datetime(2024, 10, 29, 19, 0),
                                                  cabin_booking=cabin_booking)

    def test_check_user_already_booked_slots_returns_true(self, user_db_storage, create_cabin_slots):
        cabin_instance_id = Cabin.objects.get(name="Conference Room")
        converted_start_date = date(2024, 10, 28)
        converted_end_date = date(2024, 10, 29)
        converted_time_slots = [time(18, 0)]
        storage = BookingDB(user_db_storage)
        response = storage.check_user_already_booked_slots(cabin_instance_id.id, converted_start_date,
                                                           converted_end_date,
                                                           converted_time_slots)
        assert response is True

    def test_check_user_already_booked_slots_returns_false(self, user_db_storage, create_cabin_slots):
        cabin_instance_id = Cabin.objects.get(name="Conference Room")
        converted_start_date = date(2024, 10, 30)
        converted_end_date = date(2024, 10, 30)
        converted_time_slots = [time(18, 0)]
        storage = BookingDB(user_db_storage)
        response = storage.check_user_already_booked_slots(cabin_instance_id.id, converted_start_date,
                                                           converted_end_date,
                                                           converted_time_slots)
        assert response is False
