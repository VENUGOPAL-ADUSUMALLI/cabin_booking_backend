from cabin_booking.presenter.cabin_details_response import CabinDetailsResponse
from cabin_booking.storage.dtos import FloorWiseCabinDetailsDTO, CabinDetailsDTO


class TestCabinDetailsResponse:
    def test_something_went_wrong_exception(self, snapshot):
        presenter = CabinDetailsResponse()
        response = presenter.something_went_wrong_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_cabin_details_success_response(self, snapshot):
        expected_dto_from_db = [
            FloorWiseCabinDetailsDTO(
                floor="Ground Floor",
                cabin=[
                    CabinDetailsDTO(
                        cabin_id='c523f744-6f9a-4da2-be0c-a1f9491e7e63',
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
                        cabin_id='a99183d9-52b4-443a-b30e-9b189702249f',
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
                        cabin_id='4fae901f-3980-47ea-a74e-abb1c3cd35a1',
                        name="Conference Room",
                        cabin_type='CONFERENCE_ROOM',
                        description='Sufficient for 25 People'  # Updated case
                    ),
                    CabinDetailsDTO(
                        cabin_id='6e7d8a1e-b5fc-4d55-9729-27417a21287d',
                        name="Call pod 3a",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='2a1fa6fc-83fa-4ed6-b9af-8ce4d0c315d3',
                        name="Call pod 3b",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='b2ff1c68-5009-4d20-9103-01db46d76342',
                        name="Call pod 3c",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='11791db9-8d32-431e-b309-c7e6435dd95d',
                        name="Call pod 3d",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    ),
                    CabinDetailsDTO(
                        cabin_id='eb08389d-3400-40d4-b376-5b71e1111bf9',
                        name="Call pod 3e",
                        cabin_type='CALL_POD_CABINS',
                        description='Sufficient for only 1 person'
                    )
                ]
            )
        ]
        presenter = CabinDetailsResponse()
        response = presenter.cabin_details_success_response(expected_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')
