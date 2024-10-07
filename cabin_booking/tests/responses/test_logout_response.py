from cabin_booking.presenter.logout_responses import LogoutResponse


class TestLogoutResponse:
    def test_invalid_refresh_token_response(self, snapshot):
        presenter = LogoutResponse()
        response = presenter.invalid_refresh_token_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_invalid_access_token_response(self, snapshot):
        presenter = LogoutResponse()
        response = presenter.invalid_access_token_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_logout_success_response(self, snapshot):
        presenter = LogoutResponse()
        response = presenter.logout_success_response()
        snapshot.assert_match(response.content, 'response.json')
