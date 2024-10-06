import mock
import pytest

from cabin_booking.exception import InvalidCabinIDException
from cabin_booking.models import Floor, Cabin
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestValidateCabinIdForCabinSlots:
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

    def test_validate_cabin_id_for_cabin_slots(self, user_db_storage_mock, create_cabins_and_floors):
        cabin_ids_in_db = []
        cabins_id = Cabin.objects.all()
        for each_id in cabins_id:
            cabin_ids_in_db.append(str(each_id.id))
        invalid_cabin_id = "1ffkbfb-kvffkjfkjb-bf555"
        cabin_ids_in_db.append(invalid_cabin_id)
        storage = BookingDB(user_db_storage_mock)
        with pytest.raises(InvalidCabinIDException):
            storage.validate_cabin_id_for_cabin_slots(cabin_ids_in_db)

    def test_validate_response_none(self, user_db_storage_mock, create_cabins_and_floors):
        cabin_ids_in_db = []
        cabins_id = Cabin.objects.all()
        for each_id in cabins_id:
            cabin_ids_in_db.append(str(each_id.id))
        storage = BookingDB(user_db_storage_mock)
        response = storage.validate_cabin_id_for_cabin_slots(cabin_ids_in_db)
        assert response is None
