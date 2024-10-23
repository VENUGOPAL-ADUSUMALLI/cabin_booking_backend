from django.http import HttpResponse

from cabin_booking.exception import InvalidUserException
from cabin_booking.presenter.login_interactor_response import LoginInteractorResponse
from cabin_booking.storage.dtos import LoginResponseDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication
from cabin_booking.storage.user_db import UserDB


class LoginInteractor:
    def __init__(self, storage: UserDB, response: LoginInteractorResponse, authentication: UserAuthentication):
        self.storage = storage
        self.response = response
        self.authentication = authentication

    def login_interactor(self, email, password) -> HttpResponse:
        try:
            user_login = self.storage.validate_password(email, password)
            if user_login is False:
                return self.response.invalid_password_exception_response()
        except InvalidUserException:
            return self.response.invalid_user_response()
        user_id = self.storage.get_user_id(email)
        access_token = self.authentication.create_access_token(user_id)
        refresh_token = self.authentication.create_refresh_token(access_token, user_id)
        user_login_dto = LoginResponseDTO(
            access_token=access_token.access_token,
            refresh_token=refresh_token.refresh_token
        )
        user_response = self.response.user_login_dto_response(user_login_dto)
        return user_response
