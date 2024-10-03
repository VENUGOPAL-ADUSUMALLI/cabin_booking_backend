import uuid

import pytest

from cabin_booking.exception import InvalidUserException
from cabin_booking.models import User
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestValidateUserId:
    def test_validate_user_id(self):
        user_id = str(uuid.uuid4())
        User.objects.create(user_id=user_id)
        storage = UserDB()
        response = storage.validate_user_id(user_id)
        assert response is None

    def test_invalid_user_exception(self):
        user_id = uuid.UUID("1a919ad7-17e5-4ea6-b072-846e1988fbc0")
        storage = UserDB()
        with pytest.raises(InvalidUserException):
            storage.validate_user_id(user_id)
