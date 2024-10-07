from datetime import time

from cabin_booking.interactors.dtos import CabinTimeSlotsAvailabilityDTO, TimeSlotsDTO
from cabin_booking.presenter.get_cabins_slots_response import CabinSlotsDetailsResponse


class TestGetCabinSlotsResponse:
    def test_invalid_cabin_id_exception(self, snapshot):
        presenter = CabinSlotsDetailsResponse()
        response = presenter.invalid_cabin_id_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_invalid_date_range_exception(self, snapshot):
        presenter = CabinSlotsDetailsResponse()
        response = presenter.invalid_date_range_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_get_cabin_slot_details_success_response(self, snapshot):
        cabin_availability_dto_from_db = [CabinTimeSlotsAvailabilityDTO(
            cabin_id='b2ff1c68-5009-4d20-9103-01db46d763420',
            time_slots=[
                TimeSlotsDTO(slot=time(9, 0), availability=True),
                TimeSlotsDTO(slot=time(10, 0), availability=True),
                TimeSlotsDTO(slot=time(11, 0), availability=True),
                TimeSlotsDTO(slot=time(12, 0), availability=True),
                TimeSlotsDTO(slot=time(13, 0), availability=True),
                TimeSlotsDTO(slot=time(14, 0), availability=True),
                TimeSlotsDTO(slot=time(15, 0), availability=True),
                TimeSlotsDTO(slot=time(16, 0), availability=True),
                TimeSlotsDTO(slot=time(17, 0), availability=True),
                TimeSlotsDTO(slot=time(18, 0), availability=False),
                TimeSlotsDTO(slot=time(19, 0), availability=True),
                TimeSlotsDTO(slot=time(20, 0), availability=False),
                TimeSlotsDTO(slot=time(21, 0), availability=True),
                TimeSlotsDTO(slot=time(22, 0), availability=True),
                TimeSlotsDTO(slot=time(23, 0), availability=True),

            ]
        )]
        presenter = CabinSlotsDetailsResponse()
        response = presenter.get_cabin_slot_details_success_response(cabin_availability_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')
