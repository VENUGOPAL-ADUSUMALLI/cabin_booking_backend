from datetime import datetime

import pytest

from cabin_booking.exception import InvalidRefreshTokenException, InvalidAccessTokenException
from cabin_booking.models import User
from cabin_booking.storage.dtos import AccessTokenDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication
from oauth2_provider.models import RefreshToken, AccessToken


@pytest.mark.django_db
class TestExpireAccessTokenRefreshToken:
    def test_expire_access_token_refresh_token(self):
        user = User.objects.create(
            username="user",
            email="testing@gmail.com",
            team_name="Booking DB test",
            first_name="Testing",
            last_name="Booking Db",
            contact_number="9835576526"
        )
        storage = UserAuthentication()
        access_token = storage.create_access_token(user.user_id)
        access_token_dto = AccessTokenDTO(
            user_id=user.user_id,
            access_token=access_token.access_token
        )
        refresh_token_dto = storage.create_refresh_token(user_id=user.user_id, access_token=access_token_dto)
        access_token_obj = AccessToken.objects.get(token=access_token.access_token)
        refresh_token_obj = RefreshToken.objects.get(token=refresh_token_dto.refresh_token)
        access_token_obj.revoked = datetime.now()
        refresh_token_obj.revoked = datetime.now()
        response = storage.expire_access_token_refresh_token(access_token=access_token.access_token,
                                                             refresh_token=refresh_token_dto.refresh_token)
        assert response is None

    def test_invalid_refresh_token(self):
        refresh_token = "f8028c4da6914db7a387d2bb87c02dba",
        access_token = "4ff013910e324889964378690f2bf0b6"
        storage = UserAuthentication()
        with pytest.raises(InvalidRefreshTokenException):
            storage.expire_access_token_refresh_token(refresh_token=refresh_token, access_token=access_token)

    def test_invalid_access_token_exception(self):
        user = User.objects.create(
            username="user",
            email="testing@gmail.com",
            team_name="Booking DB test",
            first_name="Testing",
            last_name="Booking Db",
            contact_number="9835576526"
        )
        storage = UserAuthentication()
        access_token = storage.create_access_token(user.user_id)
        access_token_dto = AccessTokenDTO(
            user_id=user.user_id,
            access_token=access_token.access_token
        )
        refresh_token_dto = storage.create_refresh_token(user_id=user.user_id, access_token=access_token_dto)
        access_token = "4ff013910e324889964378690f2bf0b6"
        storage = UserAuthentication()
        with pytest.raises(InvalidAccessTokenException):
            storage.expire_access_token_refresh_token(refresh_token=refresh_token_dto.refresh_token,
                                                      access_token=access_token)
