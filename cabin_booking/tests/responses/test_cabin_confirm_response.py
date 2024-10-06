from cabin_booking.presenter.cabin_confirm_slots_response import ConfirmSlotResponse


class TestCabinConfirmSlot:
    def test_cabin_confirm_slot(self, snapshot):
        presenter = ConfirmSlotResponse()
        response = presenter.invalid_cabin_id_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_invalid_user_id_response(self, snapshot):
        presenter = ConfirmSlotResponse()
        response = presenter.invalid_user_id_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_create_confirm_slots_success_response(self, snapshot):
        presenter = ConfirmSlotResponse()
        response = presenter.create_confirm_slots_success_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_uniques_constraint_response(self, snapshot):
        presenter = ConfirmSlotResponse()
        response = presenter.uniques_constraint_response()
        snapshot.assert_match(response.content, 'response.json')
