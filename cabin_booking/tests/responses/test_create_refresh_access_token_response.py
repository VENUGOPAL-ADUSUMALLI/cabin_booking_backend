from cabin_booking.presenter.create_refresh_access_token_response import CreateRefreshAccessTokensResponse


class TestCreateRefreshTokenAccessTokenResponse:
    def test_invalid_refresh_token_response(self, snapshot):
        presenter = CreateRefreshAccessTokensResponse()
        response = presenter.invalid_refresh_token_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_token_expired_response(self, snapshot):
        presenter = CreateRefreshAccessTokensResponse()
        response = presenter.token_expired_response()
        snapshot.assert_match(response.content, 'response.json')
