from cabin_booking.exception import InvalidUserException
from cabin_booking.models import *


class UserDB():
    def __init__(self):
        pass

    @staticmethod
    def get_user_id(email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            raise InvalidUserException()
