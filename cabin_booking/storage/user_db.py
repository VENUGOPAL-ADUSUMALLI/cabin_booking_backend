from django.contrib.auth.hashers import make_password

from cabin_booking.exception import InvalidUserException, UserAlreadyExistsException, \
    InvalidUserDetailsException, InvalidEmailException
from cabin_booking.models import *
from cabin_booking.storage.dtos import ProfileDTO


class UserDB:
    def __init__(self):
        pass

    @staticmethod
    def get_user_id(email):
        user = User.objects.get(email=email)
        return str(user.user_id)

    @staticmethod
    def validate_password(email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise InvalidUserException
        return user.check_password(password)

    @staticmethod
    def create_user_for_signup(email, password, username, first_name, last_name, team_name, contact_number):
        if User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException()

        hashed_password = make_password(password)
        user = User.objects.create(email=email, password=hashed_password, username=username, first_name=first_name,
                                   last_name=last_name, team_name=team_name, contact_number=contact_number)

        user_profile_dto = ProfileDTO(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            team_name=user.team_name,
            contact_number=user.contact_number
        )
        return user_profile_dto

    @staticmethod
    def profile(user_id):
        user_details = User.objects.get(user_id=user_id)
        if not user_details:
            raise InvalidUserException()
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
        hashed_password = make_password(new_password)
        user.password = hashed_password
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

    @staticmethod
    def validate_user_email(email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise InvalidEmailException()

    @staticmethod
    def validate_user_first_name(first_name, last_name, contact_number):
        try:
            User.objects.get(first_name=first_name, last_name=last_name, contact_number=contact_number)
        except User.DoesNotExist:
            raise InvalidUserDetailsException()

    @staticmethod
    def update_user_profile(username, first_name, last_name, contact_number, team_name, user_id):
        user_profile_update = User.objects.filter(user_id=user_id).update(
            username=username,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number, team_name=team_name)
        # it returns the number of rows that updated
        return user_profile_update
