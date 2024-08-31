import logging
from collections import defaultdict
from dataclasses import dataclass

from oauth2_provider.models import Application

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from cabin_booking.databases.user_authentication_db import
from cabin_booking.exception import InvalidUserException, UserAlreadyExistsException, InvalidPasswordException, \
    InvalidEmailExceptiom
from cabin_booking.models import *
from django.conf import settings

logger = logging.getLogger(__name__)



@dataclass
class UserDTO:
    name: str
    email: str
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


def get_user_object(email):
    user = User.objects.get(email=email)
    app = Application.objects.create(
        name = settings.Application_name,
        client_type = Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type = Application.GRANT_PASSWORD,
        user = user
    )


def check_user_login(email: str, password: str) -> UserDTO:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        logger.warning(f"Failed login attempt: Invalid email {email}")
        raise InvalidUserException("Invalid email id (don't have an account please signup to continue)")
    if not user.check_password(password):
        logger.warning(f"Failed login attempt:Invalid password for email {email}")
        raise InvalidPasswordException("Invalid Password (please check your password)")
    return UserDTO(
        name=user.first_name,
        email=user.email
    )
    # user_dict = {
    #     "first_name": user.first_name,
    #     "last_name": user.last_name,
    #     "team_name": user.team_name,
    #     "contact_number": user.contact_number,
    #     "email": user.email,
    #     "tokens": get_tokens_for_user(user)
    # }
    # return user_dict


def create_user_for_signup(email, username, password, first_name, last_name, team_name, contact_number):
    if User.objects.filter(email=email).exists():
        raise UserAlreadyExistsException("you have an account please login to continue")

    user = User.objects.create_user(email=email, password=password, username=username, first_name=first_name,
                                    last_name=last_name, team_name=team_name, contact_number=contact_number)
    return get_tokens_for_user(user)


def update_user_password(email, new_password, confirm_password):
    try:
        user = User.objects.get(email=email)
        if new_password != confirm_password:
            raise InvalidPasswordException("password Doesn't match")
        user.set_password(new_password)
        user.save()
        return Response({"message": "password Updated Successfully"}, status=status.HTTP_200_OK)
    except:
        raise InvalidEmailExceptiom("Invalid Email id")

# user = check_user_login(1, 2)
# name = user.name
# email = user.email
