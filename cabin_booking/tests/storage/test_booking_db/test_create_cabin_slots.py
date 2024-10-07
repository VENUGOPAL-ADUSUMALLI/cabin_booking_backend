import pytest

from cabin_booking.interactors.dtos import StartEndDateTimeDTO
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB
from cabin_booking.models import *


@pytest.mark.django_db
class TestCreateCabinSlots:
    @pytest.fixture()
    def user_db_storage_mock(self):
        return UserDB()

    def test_create_cabin_slots(self, user_db_storage_mock):
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
        start_date_time = datetime(2024, 10, 28, 18, 0)
        end_date_time = datetime(2024, 10, 30, 19, 0)
        purpose = "Meeting"
        start_end_date_time_dto = StartEndDateTimeDTO(
            start_date_time=start_date_time,
            end_date_time=end_date_time
        )
        storage = BookingDB(user_db_storage_mock)
        response = storage.create_cabin_slots(cabin_instance.id, purpose=purpose, user_id=user.user_id,
                                              list_start_end_date_time_dto=[start_end_date_time_dto])
        assert response is None
