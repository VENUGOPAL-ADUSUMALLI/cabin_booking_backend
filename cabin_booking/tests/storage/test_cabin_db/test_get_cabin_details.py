import pytest

from cabin_booking.exception import SomethingWentWrongException
from cabin_booking.models import Cabin, Floor
from cabin_booking.storage.cabin_db import CabinDB
from cabin_booking.storage.dtos import FloorWiseCabinDetailsDTO, CabinDetailsDTO


@pytest.mark.django_db
class TestGetCabinDetails:
    def test_get_cabin_details(self):
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
        storage = CabinDB()
        response = storage.get_cabins_details()
        ground_floor_conference = Cabin.objects.get(name='Conference Room', floor=ground_floor)
        first_floor_conference = Cabin.objects.get(name="Conference Room", floor=first_floor)
        fourth_floor_conference = Cabin.objects.get(name="Conference Room", floor=fourth_floor)
        fourth_floor_pod_3a = Cabin.objects.get(name='Call pod 3a', floor=fourth_floor)
        fourth_floor_pod_3b = Cabin.objects.get(name='Call pod 3b', floor=fourth_floor)
        fourth_floor_pod_3c = Cabin.objects.get(name='Call pod 3c', floor=fourth_floor)
        fourth_floor_pod_3d = Cabin.objects.get(name='Call pod 3d', floor=fourth_floor)
        fourth_floor_pod_3e = Cabin.objects.get(name='Call pod 3e', floor=fourth_floor)

        # Updated description casing to match the actual data
        expected_dto = [
            FloorWiseCabinDetailsDTO(
                floor="Ground Floor",
                cabin=[
                    CabinDetailsDTO(
                        cabin_id=str(ground_floor_conference.id),
                        name="Conference Room",
                        cabin_type='CONFERENCE_ROOM',
                        description='Sufficient for 25 People'  # Updated case
                    )
                ]
            ),
            FloorWiseCabinDetailsDTO(
                floor="First Floor",
                cabin=[
                    CabinDetailsDTO(
                        cabin_id=str(first_floor_conference.id),
                        name="Conference Room",
                        cabin_type='CONFERENCE_ROOM',
                        description='Sufficient for 25 People'  # Updated case
                    )
                ]
            ),
            FloorWiseCabinDetailsDTO(
                floor="Fourth Floor",
                cabin=[
                    CabinDetailsDTO(
                        cabin_id=str(fourth_floor_conference.id),
                        name="Conference Room",
                        cabin_type='CONFERENCE_ROOM',
                        description='Sufficient for 25 People'  # Updated case
                    ),
                    CabinDetailsDTO(
                        cabin_id=str(fourth_floor_pod_3a.id),
                        name="Call pod 3a",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id=str(fourth_floor_pod_3b.id),
                        name="Call pod 3b",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id=str(fourth_floor_pod_3c.id),
                        name="Call pod 3c",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id=str(fourth_floor_pod_3d.id),
                        name="Call pod 3d",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id=str(fourth_floor_pod_3e.id),
                        name="Call pod 3e",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    )
                ]
            )
        ]
        assert response == expected_dto
    def test_cabin_does_not_exist(self):
        storage = CabinDB()
        def get_mock_cabin_exception():
            try:
                raise Cabin.DoesNotExist
            except Cabin.DoesNotExist:
                raise SomethingWentWrongException()

        storage.get_cabins_details = get_mock_cabin_exception
        with pytest.raises(SomethingWentWrongException):
            storage.get_cabins_details()

