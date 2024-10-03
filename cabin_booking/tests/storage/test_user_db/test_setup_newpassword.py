import pytest
from django.contrib.auth.hashers import make_password

from cabin_booking.models import User
from cabin_booking.storage.dtos import ProfileDTO
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestSetupNewPassword:
    def test_setup_new_password(self):
        email = "iphone@gamil.com"
        username = 'null'
        first_name = "Apple"
        last_name = "iphone"
        team_name = "Sales"
        contact_number = "9666910497"
        new_password = "123456789"
        hashed_password = make_password(new_password)
        user = User.objects.create(email=email, username=username, first_name=first_name, last_name=last_name,
                                   team_name=team_name, contact_number=contact_number, password=hashed_password)
        storage = UserDB()
        response = storage.setup_newpassword(user.user_id, new_password)
        expected_dto = ProfileDTO(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            team_name=team_name,
            contact_number=contact_number
        )
        actual_dto = ProfileDTO(
            email=response.email,
            first_name=response.first_name,
            last_name=response.last_name,
            username=response.username,
            team_name=response.team_name,
            contact_number=response.contact_number
        )
        assert expected_dto == actual_dto
