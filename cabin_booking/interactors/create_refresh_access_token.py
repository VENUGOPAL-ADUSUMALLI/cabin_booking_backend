from cabin_booking.databases.dtos import CreateRefreshTokenDTO
from cabin_booking.databases.user_authentication_db import UserAuthentication
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidUserException, InvalidRefreshTokenException, RefreshTokenExpiredException
from cabin_booking.responses.create_refresh_access_token_response import CreateRefreshAccessTokensResponse


class CreateRefreshAccessToken:
    def __init__(self, storage: UserDB, authentication: UserAuthentication,
                 response: CreateRefreshAccessTokensResponse):
        self.storage = storage
        self.authentication = authentication
        self.response = response

    def refresh_access_token_interactor(self, refresh_token):
        try:
            get_refresh_token = self.authentication.create_refresh_access_token(
                refresh_token)
        except InvalidRefreshTokenException:
            return self.response.invalid_refresh_token_response()
        except RefreshTokenExpiredException:
            return self.response.token_expired_response()
        refresh_access_token_dto = CreateRefreshTokenDTO(
            access_token=get_refresh_token
        )
        response = self.response.get_refresh_access_token_success_response(refresh_access_token_dto)
        return response
