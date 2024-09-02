import logging
from collections import defaultdict
from os import access

from django.core.exceptions import MultipleObjectsReturned
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


class UserAuthentication:
    @staticmethod
    def create_application(user_id):
        app = Application.objects.create(
            name=settings.APPLICATION_NAME,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user_id=user_id
        )
        return app

    def create_access_token(self, user_id):
        try:
            app = Application.objects.get(name=settings.APPLICATION_NAME,user_id=user_id)
        except MultipleObjectsReturned:
            app = self.create_application(user_id)
        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        access_token = AccessToken.objects.create(
            user_id=user_id,
            scope='read write',
            expires=expires,
            token=uuid.uuid4().hex,
            application=app
        )
        return access_token

    def create_refresh_token(self, access_token, user_id):
        try:
            app = Application.objects.get(name=settings.APPLICATION_NAME, user_id=user_id)
        except MultipleObjectsReturned:
            app = self.create_application(user_id)
        refresh_token = RefreshToken.objects.create(
            user_id=user_id,
            token=uuid.uuid4().hex,
            application=app,
            access_token=access_token
        )
        return refresh_token
