from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidUserException
from cabin_booking.responses.update_password_response import UpdatePasswordResponse
from cabin_booking.models import User


class UpdatePasswordInteractor:
    def __init__(self, storage: UserDB, response: UpdatePasswordResponse):
        self.storage = storage
        self.response = response

    def update_password_interactor(self, email, old_password, new_password):
        try:
            is_correct_password = self.storage.validate_password(email, old_password)
            if is_correct_password is False:
                return self.response.invalid_password_response()
        except InvalidUserException:
            return self.response.invalid_user_response()
        user_id = self.storage.get_user_id(email)
        self.storage.setup_newpassword(user_id, new_password)
        return self.response.password_update_successfull_response()

