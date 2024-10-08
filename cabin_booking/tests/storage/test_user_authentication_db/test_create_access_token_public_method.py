import pytest

from cabin_booking.models import User
from cabin_booking.storage.user_authentication_db import UserAuthentication


@pytest.mark.django_db
class TestCreateAccessTokenPublicMethod:
    def test_create_access_token(self):
        user = User.objects.create(
            username="user",
            email="testing@gmail.com",
            team_name="Booking DB test",
            first_name="Testing",
            last_name="Booking Db",
            contact_number="9835576526"
        )
        storage = UserAuthentication()
        response = storage.create_access_token(user.user_id)
        assert str(user.user_id) == str(response.user_id)
        assert 32 == len(response.access_token)
