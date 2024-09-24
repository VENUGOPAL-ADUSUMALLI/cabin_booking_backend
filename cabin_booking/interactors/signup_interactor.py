import json

from django.http import HttpResponse

from cabin_booking.storage.dtos import SignupResponseDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication
from cabin_booking.storage.user_db import UserDB
from cabin_booking.exception import UserAlreadyExistsException, UniqueConstraintException
from cabin_booking.presenter.signup_interactor_response import SignupInteractorResponse


class SignupInteractor:
    def __init__(self, storage: UserDB, response: SignupInteractorResponse):
        self.storage = storage
        self.response = response

    def signup_interactor(self, email, username, password, first_name, last_name, team_name, contact_number):
        try:
            self.storage.create_user_for_signup(email, password, username, first_name, last_name,
                                                team_name, contact_number)
        except UserAlreadyExistsException:
            return self.response.user_already_exists_response()
        user_id = self.storage.get_user_id(email)
        access_token = UserAuthentication().create_access_token(user_id)
        refresh_token = UserAuthentication().create_refresh_token(access_token, user_id)
        user_signup_dto = SignupResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )
        user_sign_up_response = SignupInteractorResponse().user_signup_dto_response(user_signup_dto)
        return user_sign_up_response
