import pytest

from cabin_booking.models import User
from cabin_booking.storage.dtos import AccessTokenDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication


@pytest.mark.django_db
class TestCreateRefreshToken:
    def test_create_refresh_token(self):
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
        response = storage.create_refresh_token(user_id=user.user_id, access_token=access_token_dto)
        assert str(user.user_id) == str(response.user_id)
        assert 32 == len(response.refresh_token)
