from cabin_booking.presenter.update_password_response import UpdatePasswordResponse


class TestUpdatePasswordResponse:
    def test_invalid_user_response(self, snapshot):
        presenter = UpdatePasswordResponse()
        response = presenter.invalid_user_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_invalid_password_response(self, snapshot):
        presenter = UpdatePasswordResponse()
        response = presenter.invalid_password_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_password_update_successfull_response(self, snapshot):
        presenter = UpdatePasswordResponse()
        response = presenter.password_update_successfull_response()
        snapshot.assert_match(response.content, 'response.json')
