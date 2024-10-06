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
