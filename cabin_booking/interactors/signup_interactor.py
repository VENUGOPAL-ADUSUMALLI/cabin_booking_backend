from os import access

from cabin_booking.databases.dtos import SignupResponseDTO
from cabin_booking.databases.user_authentication_db import UserAuthentication
from cabin_booking.databases.user_db import UserDB


class SignupInteractor:
    def __init__(self, storage: UserDB):
        self.storage = storage

    def signup_interactor(self, email, username, password, first_name, last_name, team_name, contact_number):
        create_account_for_user = self.storage.create_user_for_signup(email, password, username, first_name, last_name,
                                                                      team_name, contact_number)
        user_id = self.storage.get_user_id(email)
        access_token = UserAuthentication().create_access_token(user_id)
        refresh_token = UserAuthentication().create_refresh_token(access_token, user_id)
        return SignupResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )
