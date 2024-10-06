import mock
import pytest

from cabin_booking.exception import InvalidCabinIDException
from cabin_booking.models import Floor, Cabin
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestValidateCabinId:
    @pytest.fixture()
    def user_db_storage_mock(self):
        return UserDB()

    @pytest.fixture()
    def create_cabins_and_floors(self):
        floor = [
            Floor(order=1, name="Ground Floor"),
            Floor(order=2, name="First Floor"),
            Floor(order=3, name="Fourth Floor"),
        ]
        Floor.objects.bulk_create(floor)
        ground_floor = Floor.objects.get(name="Ground Floor")
        first_floor = Floor.objects.get(name="First Floor")
        fourth_floor = Floor.objects.get(name="Fourth Floor")
        cabins = [
            Cabin(floor=ground_floor, name="Conference Room", type='CONFERENCE_ROOM',
                  description="Sufficient for 25 People", is_available=True),
            Cabin(floor=first_floor, name="Conference Room", type='CONFERENCE_ROOM',
                  description="Sufficient for 25 People", is_available=True),
            Cabin(floor=fourth_floor, name="Conference Room", type='CONFERENCE_ROOM',
                  description="Sufficient for 25 People", is_available=True),
            Cabin(floor=fourth_floor, name="Call pod 3a", type='CALL_POD_CABINS',
                  description="Sufficient for only 1 person", is_available=True),
            Cabin(floor=fourth_floor, name="Call pod 3b", type='CALL_POD_CABINS',
                  description="Sufficient for only 1 person", is_available=True),
            Cabin(floor=fourth_floor, name="Call pod 3c", type='CALL_POD_CABINS',
                  description="Sufficient for only 1 person", is_available=True),
            Cabin(floor=fourth_floor, name="Call pod 3d", type='CALL_POD_CABINS',
                  description="Sufficient for only 1 person", is_available=True),
            Cabin(floor=fourth_floor, name="Call pod 3e", type='CALL_POD_CABINS',
                  description="Sufficient for only 1 person", is_available=True),
        ]
        Cabin.objects.bulk_create(cabins)

    def test_validate_cabin_id_invalid_cabin_id_exception(self, user_db_storage_mock, create_cabins_and_floors):
        cabin_id = "5d62d552-1889-49ca-bd1d-b7b862c77bfc"
        storage = BookingDB(user_db_storage_mock)
        with pytest.raises(InvalidCabinIDException):
            storage.validate_cabin_id(cabin_id)

    def test_validate_cabin_id_valid_cabin_id_return_none(self, user_db_storage_mock, create_cabins_and_floors):
        cabin_id = "c560fd6f-bd0f-47fe-9fb2-63ebd1624211"
        floor = Floor.objects.create(order=1, name="Ground Floor")
        cabins = Cabin.objects.create(id=cabin_id, floor=floor)
        storage = BookingDB(user_db_storage_mock)
        response = storage.validate_cabin_id(cabins.id)
        assert response is None
