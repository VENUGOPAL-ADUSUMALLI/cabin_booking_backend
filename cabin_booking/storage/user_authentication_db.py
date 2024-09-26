from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from oauth2_provider.models import Application
from oauth2_provider.models import RefreshToken, AccessToken
from oauth2_provider.settings import oauth2_settings
from pycparser.ply.yacc import token

from cabin_booking.constants.time_slots_constant import REFRESH_TOKEN_EXPIRE_TIME
from cabin_booking.exception import RefreshTokenExpiredException, InvalidRefreshTokenException, \
    InvalidAccessTokenException
from cabin_booking.models import *
from cabin_booking.storage.dtos import CreateRefreshTokenDTO


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
        app = Application.objects.filter(name=settings.APPLICATION_NAME, user_id=user_id).first()
        if not app:
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
        app = Application.objects.filter(name=settings.APPLICATION_NAME, user_id=user_id).first()
        if not app:
            app = self.create_application(user_id)
        expire_date = timezone.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_TIME)
        refresh_token = RefreshToken.objects.create(
            user_id=user_id,
            token=uuid.uuid4().hex,
            application=app,
            access_token=access_token
        )
        refresh_token.revoked = expire_date
        refresh_token.save()
        return refresh_token

    def create_refresh_access_token(self, refresh_token):
        try:
            refresh_token_obj = RefreshToken.objects.get(token=refresh_token)
            if refresh_token_obj.revoked < timezone.now():
                raise RefreshTokenExpiredException()
            new_access_token = self.create_access_token(refresh_token_obj.user_id)
            refresh_token_obj.access_token = new_access_token
            refresh_token_obj.save()
            access_token_dto = CreateRefreshTokenDTO(
                access_token=refresh_token_obj.access_token
            )
            return access_token_dto
        except RefreshToken.DoesNotExist:
            raise InvalidRefreshTokenException()

    def expire_access_token_refresh_token(self, access_token, refresh_token):
        try:
            with transaction.atomic():
                refresh_token_obj = RefreshToken.objects.get(token=refresh_token)
                refresh_token_obj.revoked = timezone.now()
                refresh_token_obj.save()
                access_token_obj = AccessToken.objects.get(token=access_token)
                access_token_obj.expires = timezone.now()
                access_token_obj.save()
        except RefreshToken.DoesNotExist:
            raise InvalidRefreshTokenException()
        except AccessToken.DoesNotExist:
            raise InvalidAccessTokenException()
