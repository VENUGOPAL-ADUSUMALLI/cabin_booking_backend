from cabin_booking.presenter.cabin_details_response import CabinDetailsResponse


class TestCabinDetailsResponse:
    def test_something_went_wrong_exception(self, snapshot):
        presenter = CabinDetailsResponse()
        response = presenter.something_went_wrong_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_cabin_details_success_response(self, snapshot):
        pass