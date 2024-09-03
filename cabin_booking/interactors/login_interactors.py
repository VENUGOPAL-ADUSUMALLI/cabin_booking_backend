from django.contrib.auth.handlers.modwsgi import check_password

from cabin_booking.databases.dtos import LoginResponseDTO
from cabin_booking.databases.user_authentication_db import UserAuthentication
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidPasswordException


class LoginInteractor:
    def __init__(self, storage: UserDB):
        self.storage = storage

    def login_interactor(self, email, password):
        check_password_for_user = self.storage.check_user_login(email, password)
        if not check_password_for_user:
            raise InvalidPasswordException()
        user_id = self.storage.get_user_id(email)
        access_token = UserAuthentication().create_access_token(user_id)
        refresh_token = UserAuthentication().create_refresh_token(access_token,user_id)
        return LoginResponseDTO(
           access_token= access_token,
           refresh_token= refresh_token
       )
