from datetime import datetime

import pytest

from cabin_booking.exception import RefreshTokenExpiredException, InvalidRefreshTokenException
from cabin_booking.models import User
from cabin_booking.storage.dtos import AccessTokenDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication
from oauth2_provider.models import RefreshToken


@pytest.mark.django_db
class TestCreateRefreshToken:
    def test_create_refresh_access_token(self):
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
        refresh_token = storage.create_refresh_token(user_id=user.user_id, access_token=access_token_dto)
        response = storage.create_refresh_access_token(refresh_token.refresh_token)
        assert len(response.access_token) == 32

    def test_refresh_token_exception(self):
        refresh_token = "f8028c4da6914db7a387d2bb87c02dba"
        storage = UserAuthentication()
        with pytest.raises(InvalidRefreshTokenException):
            storage.create_refresh_access_token(refresh_token)

    def test_refresh_token_expired_exception(self):
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
        refresh_token_obj = RefreshToken.objects.get(token=refresh_token_dto.refresh_token)
        refresh_token_obj.revoked = datetime.now()
        refresh_token_obj.save()
        with pytest.raises(RefreshTokenExpiredException):
            storage.create_refresh_access_token(refresh_token_obj.token)
