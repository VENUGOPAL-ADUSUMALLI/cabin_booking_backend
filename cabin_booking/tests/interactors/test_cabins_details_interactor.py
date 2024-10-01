from unittest import mock

import pytest

from cabin_booking.exception import SomethingWentWrongException
from cabin_booking.interactors.cabins_details_interactor import CabinDetailsInteractor
from cabin_booking.presenter.cabin_details_response import CabinDetailsResponse
from cabin_booking.storage.cabin_db import CabinDB
from cabin_booking.storage.dtos import FloorWiseCabinDetailsDTO, CabinDetailsDTO


class TestCabinDetails:
    @pytest.fixture
    def cabin_db_mock(self):
        return mock.create_autospec(CabinDB)

    @pytest.fixture
    def cabins_details_response_mock(self):
        return mock.create_autospec(CabinDetailsResponse)

    @pytest.fixture
    def interactor(self, cabin_db_mock, cabins_details_response_mock):
        return CabinDetailsInteractor(
            storage=cabin_db_mock,
            response=cabins_details_response_mock
        )

    def test_some_went_wrong_exception(self, interactor, cabin_db_mock, cabins_details_response_mock):
        # Arrange
        cabin_db_mock.get_cabins_details.side_effect = SomethingWentWrongException
        expected_response = "something went wrong"
        cabins_details_response_mock.something_went_wrong_exception.return_value = expected_response
        # Act
        response = interactor.get_floor_wise_cabins_list()
        # Assert
        cabin_db_mock.get_cabins_details.assert_called_once()
        cabins_details_response_mock.something_went_wrong_exception.assert_called_once()
        cabins_details_response_mock.cabin_details_success_response.assert_not_called()
        assert response == expected_response

    def test_get_cabins_details(self, interactor, cabin_db_mock, cabins_details_response_mock):
        # Arrange
        cabin_details_dto = [
            FloorWiseCabinDetailsDTO(
                floor='Ground Floor',
                cabin=[
                    CabinDetailsDTO(
                        cabin_id='c523f744-6f9a-4da2-be0c-a1f9491e7e63',
                        name='Conference Room',
                        cabin_type='CONFERENCE_ROOM',
                        description='Sufficient for 25 People'
                    )
                ]
            ),
            FloorWiseCabinDetailsDTO(
                floor='First Floor',
                cabin=[
                    CabinDetailsDTO(
                        cabin_id='a99183d9-52b4-443a-b30e-9b189702249f',
                        name='Conference Room',
                        cabin_type='CONFERENCE_ROOM',
                        description='Sufficient for 25 people'
                    )
                ]
            ),
            FloorWiseCabinDetailsDTO(
                floor='Fourth Floor',
                cabin=[
                    CabinDetailsDTO(
                        cabin_id='cfbfc0d3-f53d-4499-8ebd-63c059fe6ef2',
                        name='Conference Room',
                        cabin_type='CONFERENCE_ROOM',
                        description='Sufficient for 25 people'
                    ),
                    CabinDetailsDTO(
                        cabin_id='6e7d8a1e-b5fc-4d55-9729-27417a21287d',
                        name='Call pod 3a',
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='2a1fa6fc-83fa-4ed6-b9af-8ce4d0c315d3',
                        name='Call pod 3b',
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='b2ff1c68-5009-4d20-9103-01db46d76342',
                        name='Call pod 3C',
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='11791db9-8d32-431e-b309-c7e6435dd95d',
                        name='Call pod 3d',
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='eb08389d-3400-40d4-b376-5b71e1111bf9',
                        name='Call pod 3e',
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    )
                ]
            )
        ]
        cabin_db_mock.get_cabins_details.return_value = cabin_details_dto
        expected_response = [
            {
                "floor_name": "Ground Floor",
                "cabins": [
                    {
                        "cabin_id": "c523f744-6f9a-4da2-be0c-a1f9491e7e63",
                        "cabin_name": "Conference Room",
                        "cabin_type": "CONFERENCE_ROOM",
                        "description": "Sufficient for 25 People"
                    }
                ]
            },
            {
                "floor_name": "First Floor",
                "cabins": [
                    {
                        "cabin_id": "a99183d9-52b4-443a-b30e-9b189702249f",
                        "cabin_name": "Conference Room",
                        "cabin_type": "CONFERENCE_ROOM",
                        "description": "sufficient for 25 people"
                    }
                ]
            },
            {
                "floor_name": "Fourth Floor",
                "cabins": [
                    {
                        "cabin_id": "cfbfc0d3-f53d-4499-8ebd-63c059fe6ef2",
                        "cabin_name": "Conference Room",
                        "cabin_type": "CONFERENCE_ROOM",
                        "description": "sufficient for 25 people"
                    },
                    {
                        "cabin_id": "6e7d8a1e-b5fc-4d55-9729-27417a21287d",
                        "cabin_name": "Call pod 3a",
                        "cabin_type": "CALL_POD_CABINS",
                        "description": "Sufficient for only 1 person"
                    },
                    {
                        "cabin_id": "2a1fa6fc-83fa-4ed6-b9af-8ce4d0c315d3",
                        "cabin_name": "Call pod 3b",
                        "cabin_type": "CALL_POD_CABINS",
                        "description": "Sufficient for only 1 person"
                    },
                    {
                        "cabin_id": "b2ff1c68-5009-4d20-9103-01db46d76342",
                        "cabin_name": "Call pod 3C",
                        "cabin_type": "CALL_POD_CABINS",
                        "description": "Sufficient for only 1 person"
                    },
                    {
                        "cabin_id": "11791db9-8d32-431e-b309-c7e6435dd95d",
                        "cabin_name": "Call pod 3d",
                        "cabin_type": "CALL_POD_CABINS",
                        "description": "Sufficient for only 1 person"
                    },
                    {
                        "cabin_id": "eb08389d-3400-40d4-b376-5b71e1111bf9",
                        "cabin_name": "Call pod 3e",
                        "cabin_type": "CALL_POD_CABINS",
                        "description": "Sufficient for only 1 person"
                    }
                ]
            }
        ]
        cabins_details_response_mock.cabin_details_success_response.return_value = expected_response
        # Act
        response = interactor.get_floor_wise_cabins_list()
        # Assert
        cabin_db_mock.get_cabins_details.assert_called_once()
        cabins_details_response_mock.cabin_details_success_response.assert_called_once_with(cabin_details_dto)
        assert response == expected_response
