

from cabin_booking.databases.dtos import UserPasswordUpdateDTO, ProfileDTO
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
    def validate_password(email, password):
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
        user_dto = ProfileDTO(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            team_name=user.team_name,
            contact_number=user.contact_number
        )
        return user_dto

    @staticmethod
    def profile(user_id):
        user_details = User.objects.get(user_id=user_id)
        user_dto = ProfileDTO(
            email=user_details.email,
            first_name=user_details.first_name,
            last_name=user_details.last_name,
            username=user_details.username,
            team_name=user_details.team_name,
            contact_number=user_details.contact_number
        )
        return user_dto

    @staticmethod
    def setup_newpassword(user_id, new_password):
        user = User.objects.get(user_id=user_id)
        print(new_password)
        user.set_password(new_password)
        user.save()
        user_dto = ProfileDTO(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            team_name=user.team_name,
            contact_number=user.contact_number
        )
        return user_dto
    @staticmethod
    def validate_user_id(user_id):
        get_user = User.objects.get(user_id=user_id)
        if not get_user:
            raise InvalidUserException()

