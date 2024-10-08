from django.http import HttpResponse

from cabin_booking.exception import InvalidRefreshTokenException, RefreshTokenExpiredException
from cabin_booking.presenter.create_refresh_access_token_response import CreateRefreshAccessTokensResponse
from cabin_booking.storage.dtos import CreateRefreshTokenDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication


class CreateRefreshAccessToken:
    def __init__(self, authentication: UserAuthentication,
                 response: CreateRefreshAccessTokensResponse):
        self.authentication = authentication
        self.response = response

    def refresh_access_token_interactor(self, refresh_token) -> HttpResponse:
        try:
            get_refresh_token = self.authentication.create_refresh_access_token(
                refresh_token)
        except InvalidRefreshTokenException:
            return self.response.invalid_refresh_token_response()
        except RefreshTokenExpiredException:
            return self.response.token_expired_response()
        refresh_access_token_dto = CreateRefreshTokenDTO(
            access_token=get_refresh_token.access_token
        )
        response = self.response.get_refresh_access_token_success_response(refresh_access_token_dto)
        return response
