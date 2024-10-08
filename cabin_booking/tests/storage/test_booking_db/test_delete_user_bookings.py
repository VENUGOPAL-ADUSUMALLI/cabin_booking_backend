import pytest

from cabin_booking.exception import InvalidBookingIDException
from cabin_booking.models import *
from cabin_booking.storage.booking_db import BookingDB
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

    def test_delete_user_bookings(self, create_cabin_slots, user_db_storage_mock):
        user = User.objects.get(email="testing@gmail.com")
        booking = Booking.objects.get(user=user)
        storage = BookingDB(user_db_storage_mock)
        response = storage.delete_user_bookings_db(booking.id)
        assert response is None
    def test_for_invalid_cabin_id(self,create_cabin_slots, user_db_storage_mock):
        booking_id ="95918a43-8f9d-4bad-9efa-0ca9dae7ec9e"
        storage = BookingDB(user_db_storage_mock)
        with pytest.raises(InvalidBookingIDException):
            storage.delete_user_bookings_db(booking_id)
