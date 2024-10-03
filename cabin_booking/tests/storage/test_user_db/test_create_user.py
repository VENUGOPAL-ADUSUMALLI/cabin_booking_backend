import pytest
from django.contrib.auth.hashers import make_password

from cabin_booking.exception import UserAlreadyExistsException
from cabin_booking.models import User
from cabin_booking.storage.dtos import ProfileDTO
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestCreateUser:
    def test_create_user(self):
        email = "iphone@gamil.com"
        password = "987654321"
        first_name = "Apple"
        last_name = "iphone"
        team_name = "Sales"
        user_name = "Venu Gopal"
        contact_number = "9666910497"
        storage = UserDB()

        expected_response = storage.create_user_for_signup(email, password, user_name, first_name, last_name, team_name,
                                                           contact_number)

        response = User.objects.get(email=email)
        assert response.first_name == first_name
        assert response.last_name == last_name
        assert response.team_name == team_name
        assert response.contact_number == contact_number
        assert response.check_password(password)
        expected_dto = ProfileDTO(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=user_name,
            team_name=team_name,
            contact_number=contact_number
        )
        actual_dto = ProfileDTO(
            email=expected_response.email,
            first_name=expected_response.first_name,
            last_name=expected_response.last_name,
            username=expected_response.username,
            team_name=expected_response.team_name,
            contact_number=expected_response.contact_number
        )
        assert expected_dto == actual_dto

    def test_user_already_exists(self):
        email = "iphone@gamil.com"
        password = "987654321"
        first_name = "Apple"
        last_name = "iphone"
        team_name = "Sales"
        user_name = "Venu Gopal"
        contact_number = "9666910497"
        storage = UserDB()
        storage.create_user_for_signup(email, password, user_name, first_name, last_name, team_name,
                                       contact_number)
        with pytest.raises(UserAlreadyExistsException):
            storage.create_user_for_signup(email, password, user_name, first_name, last_name, team_name,
                                           contact_number)
