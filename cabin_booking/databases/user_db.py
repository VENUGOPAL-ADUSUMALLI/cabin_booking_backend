from cabin_booking.exception import InvalidUserException, InvalidPasswordException, UserAlreadyExistsException, \
    UniqueConstraintException
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
    def get_email(email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise InvalidUserException()
        return user

    @staticmethod
    def setup_newpassword(user, new_password):
        user.set_password(new_password)
        user_save_password = user.save()
        return user_save_password
