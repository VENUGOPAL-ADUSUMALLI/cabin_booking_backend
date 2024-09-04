from django.http import HttpResponse

from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidPasswordException, InvalidUserException
from cabin_booking.interactors.update_password_response import UpdatePasswordResponse


class UpdatePasswordInteractor:
    def __init__(self, storage: UserDB, response: UpdatePasswordResponse):
        self.storage = storage
        self.response = response

    def update_password_interactor(self, email, password, new_password):
        try:
            user = self.storage.get_email(email)
        except InvalidUserException:
            return self.response.invalid_user_response()
        if new_password != password:
            return self.response.invalid_password_response()
        self.storage.setup_newpassword(user,new_password)
        return self.response.password_update_successfull_response()
