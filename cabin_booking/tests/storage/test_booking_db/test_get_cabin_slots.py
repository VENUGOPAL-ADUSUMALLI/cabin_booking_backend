import uuid
from datetime import datetime, timedelta

import mock
import pytest

from cabin_booking.interactors.dtos import StartEndDateTimeDTO
from cabin_booking.models import BookingSlot, User, Floor, Cabin
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestGetCabinSlots:
    @pytest.fixture()
    def user_db_storage_mock(self):
        return UserDB()

    def test_get_cabin_slots(self, user_db_storage_mock):
        floor = Floor.objects.create(order=1, name="Ground Floor")
        cabin_id = str(uuid.uuid4())
        cabin = Cabin.objects.create(id=cabin_id, floor=floor, name="Conference Room", type="CONFERENCE_ROOM",
                                     description='Sufficient for 25 People', is_available=True)
        purpose = 'Meeting'
        user_id = str(uuid.uuid4())
        user = User.objects.create(
            user_id=user_id,
            email="sample@gamil.com",
            team_name="Testing",
            contact_number="9666910497",
            first_name='Testing for',
            last_name="Booking"
        )
        list_start_time = [datetime(2024, 10, 28, 18, 0), datetime(2024, 10, 29, 20, 0)]
        list_start_end_date = []
        for start_date_time in list_start_time:
            end_date_time = start_date_time + timedelta(hours=1)
            start_date_time_dto = StartEndDateTimeDTO(
                start_date_time=start_date_time,
                end_date_time=end_date_time
            )
            list_start_end_date.append(start_date_time_dto)
        storage = BookingDB(user_db_storage_mock)

        storage.create_cabin_slots(cabin.id, purpose, user.user_id, list_start_end_date)
        booking_obj = BookingSlot.objects.filter(cabin_booking__cabin__id__in=[cabin.id])
        assert booking_obj.count() == 2
