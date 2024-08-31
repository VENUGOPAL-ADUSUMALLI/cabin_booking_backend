from django.contrib.auth.handlers.modwsgi import check_password

from cabin_booking.databases.user_authentication_db import user_authentication
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidPasswordException


class Interactor:
    @staticmethod
    def login_interactor(email, password):
        check_password_for_user = UserDB.check_user_login(email,password)
        if not check_password_for_user:
            raise InvalidPasswordException()
        user_id = UserDB.get_user_id(email)
        return user_authentication.create_access_token(user_id)

