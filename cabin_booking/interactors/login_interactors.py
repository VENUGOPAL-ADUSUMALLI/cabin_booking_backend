import json
from http.client import responses

from django.contrib.auth.handlers.modwsgi import check_password
from django.http import HttpResponse

from cabin_booking.databases.dtos import LoginResponseDTO
from cabin_booking.databases.user_authentication_db import UserAuthentication
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidPasswordException, InvalidUserException
from cabin_booking.responses.login_interactor_response import LoginInteractorResponse


class LoginInteractor:
    def __init__(self, storage:UserDB,response:LoginInteractorResponse):
        self.storage = storage
        self.response = response

    def login_interactor(self, email, password):
        try:
            user_login = self.storage.check_user_login(email, password)
            if not user_login:
                return  self.response.invalid_password_exception_response()

        except InvalidUserException:
           return self.response.invalid_user_response()
        user_id = self.storage.get_user_id(email)
        access_token = UserAuthentication().create_access_token(user_id)
        refresh_token = UserAuthentication().create_refresh_token(access_token, user_id)
        user_login_dto = LoginResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )
        user_response = LoginInteractorResponse().user_login_dto_response(user_login_dto)
        return user_response
