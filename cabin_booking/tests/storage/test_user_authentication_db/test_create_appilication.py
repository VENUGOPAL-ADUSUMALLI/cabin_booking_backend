import pytest

from cabin_booking.models import User
from cabin_booking.storage.user_authentication_db import UserAuthentication


@pytest.mark.django_db
class TestCreateApplication:
    def test_create_application(self):
        user = User.objects.create(
            username="user",
            email="testing@gmail.com",
            team_name="Booking DB test",
            first_name="Testing",
            last_name="Booking Db",
            contact_number="9835576526"
        )
        storage = UserAuthentication()
        response = storage._create_application(user.user_id)
        assert user.user_id == response.user_id

