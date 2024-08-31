import logging
from collections import defaultdict
from os import access

from oauth2_provider.models import Application
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from django.utils import timezone
from datetime import timedelta
import uuid
from cabin_booking.models import *
from cabin_booking.databases.user_db import UserDB
from cabin_booking_backend.asgi import application


class user_authentication:
    @staticmethod
    def create_application(user_id):
        app = Application.objects.create(
            name=settings.Application_name,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authrization_grant_type=Application.GRANT_PASSWORD,
            user_id=user_id
        )
        return app

    @staticmethod
    def create_access_token(user_id):
        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        app = Application.objects.get(settings.Application_name)
        access_token = AccessToken.objects.create(
            user=user_id,
            scope='read write',
            expires=expires,
            token=uuid.uuid4().hex,
            application=app
        )
        return access_token
    @staticmethod
    def create_refresh_token(access_token, user_id):
        app = Application.objects.get(settings.Application_name)
        refresh_token = RefreshToken.objects.create(
            user_id=user_id,
            token=uuid.uuid4().hex,
            application=app,
            access_token=access_token
        )
        return refresh_token
