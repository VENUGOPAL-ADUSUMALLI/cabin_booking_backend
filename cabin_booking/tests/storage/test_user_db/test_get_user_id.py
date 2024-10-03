import uuid


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