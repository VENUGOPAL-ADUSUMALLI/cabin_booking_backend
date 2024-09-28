import uuid
from http.client import responses

import pytest
from cabin_booking.models import User
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestGetUserId:
    def test_get_user_id(self):
        user_id = str(uuid.uuid4())
        email = "venu@gmail.com"
        User.objects.create(
            user_id=user_id,
            email=email,
        )
        storage = UserDB()
        response = storage.get_user_id(email)
        assert response == user_id

    def test_create_user(self):
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
        response = User.objects.get(email=email)
        assert response.first_name == first_name
        assert response.last_name == last_name
        assert response.team_name == team_name
        assert response.contact_number == contact_number
