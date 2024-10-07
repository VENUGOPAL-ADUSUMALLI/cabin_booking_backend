from cabin_booking.presenter.create_refresh_access_token_response import CreateRefreshAccessTokensResponse
from cabin_booking.storage.dtos import CreateRefreshTokenDTO


class TestCreateRefreshTokenAccessTokenResponse:
    def test_invalid_refresh_token_response(self, snapshot):
        presenter = CreateRefreshAccessTokensResponse()
        response = presenter.invalid_refresh_token_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_token_expired_response(self, snapshot):
        presenter = CreateRefreshAccessTokensResponse()
        response = presenter.token_expired_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_get_refresh_access_token_success_response(self, snapshot):
        expected_dto_from_db = CreateRefreshTokenDTO(
            access_token="1f8c77a1c4eb4b24a55ccf65f7828def"
        )
        presenter = CreateRefreshAccessTokensResponse()
        response = presenter.get_refresh_access_token_success_response(expected_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')

