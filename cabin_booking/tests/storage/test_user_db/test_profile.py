import uuid

import pytest

from cabin_booking.exception import InvalidUserException
from cabin_booking.models import User
from cabin_booking.storage.dtos import ProfileDTO
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestProfile:
    def test_user_profile(self):
        email = "iphone@gamil.com"
        username = 'null'
        first_name = "Apple"
        last_name = "iphone"
        team_name = "Sales"
        contact_number = "9666910497"
        user = User.objects.create(email=email, username=username, first_name=first_name, last_name=last_name,
                                   team_name=team_name, contact_number=contact_number)
        storage = UserDB()
        response = storage.profile(user.user_id)
        expected_dto = ProfileDTO(
            email=response.email,
            first_name=response.first_name,
            last_name=response.last_name,
            username=response.username,
            team_name=response.team_name,
            contact_number=response.contact_number
        )
        actual_dto = ProfileDTO(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            team_name=team_name,
            contact_number=contact_number
        )
        assert actual_dto == expected_dto

    def test_invalid_user_exception(self):
        user_id = uuid.UUID("1a919ad7-17e5-4ea6-b072-846e1988fbc0")
        storage = UserDB()
        with pytest.raises(InvalidUserException):
            storage.profile(user_id)
