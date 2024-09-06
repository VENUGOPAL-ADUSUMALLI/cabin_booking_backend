from django.contrib.auth.hashers import check_password

from cabin_booking.databases.dtos import UserPasswordUpdateDTo
from cabin_booking.exception import InvalidUserException, InvalidPasswordException, UserAlreadyExistsException, \
    UniqueConstraintException
from cabin_booking.models import *


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
        return user.check_password(password)

    @staticmethod
    def create_user_for_signup(email, password, username, first_name, last_name, team_name, contact_number):
        if User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException()
        try:
            user = User.objects.create_user(email=email, password=password, username=username, first_name=first_name,
                                            last_name=last_name, team_name=team_name, contact_number=contact_number)

        except Exception as e:
            raise UniqueConstraintException(message=e)
        return user

    @staticmethod
    def profile(user_id):
        user_details = User.objects.get(user_id=user_id)
        return user_details

    @staticmethod
    def check_password_user(email,password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise InvalidUserException()
        return user.check_password(password)

    @staticmethod
    def setup_newpassword(user_id, new_password):
        user = User.objects.get(user_id = user_id)
        user.set_password(new_password)
        user.save()
