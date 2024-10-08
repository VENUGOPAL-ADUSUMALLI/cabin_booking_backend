from cabin_booking.presenter.delete_user_bookings_response import DeleteUserBookingsResponse


class TestDeleteUserBookingsResponse:
    def test_invalid_booking_exception(self,snapshot):
        presenter = DeleteUserBookingsResponse()
        response = presenter.invalid_booking_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_slot_delete_success_response(self, snapshot):
        presenter = DeleteUserBookingsResponse()
        response = presenter.slot_delete_success_response()
        snapshot.assert_match(response.content, 'response.json')