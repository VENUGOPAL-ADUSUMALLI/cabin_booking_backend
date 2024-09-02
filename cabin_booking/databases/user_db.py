from cabin_booking.exception import InvalidUserException, InvalidPasswordException
from cabin_booking.models import *
from cabin_booking.utils import check_user_login, UserDTO


class UserDB:
    def __init__(self):
        pass

    @staticmethod
    def get_user_id(email):
        try:
            user = User.objects.get(email=email)
            return str(user.user_id)
            # print(user.user_id)

        except User.DoesNotExist:
            raise InvalidUserException()

    @staticmethod
    def check_user_login(email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise InvalidUserException()
        return  user.check_password(password)

