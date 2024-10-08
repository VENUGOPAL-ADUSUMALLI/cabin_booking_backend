from django.http import HttpResponse

from cabin_booking.exception import InvalidUserException
from cabin_booking.presenter.user_profile_update_response import UserProfileUpdateResponse
from cabin_booking.storage.user_db import UserDB


class UserProfileUpdate:
    def __init__(self, storage: UserDB, response: UserProfileUpdateResponse):
        self.storage = storage
        self.response = response

    def update_user_profile_interactor(self, username, first_name, last_name, contact_number, team_name,
                                       user_id) -> HttpResponse:
        try:
            self.storage.validate_user_id(user_id)
        except InvalidUserException:
            return self.response.invalid_user_exception()
        self.storage.update_user_profile(username, first_name, last_name, contact_number, team_name, user_id)
        return self.response.update_user_profile_success_response()
