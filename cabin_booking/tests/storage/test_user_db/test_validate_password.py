import pytest
from django.contrib.auth.hashers import make_password

from cabin_booking.exception import InvalidUserException
from cabin_booking.models import User
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestValidatePassword:
    def test_validate_password_return_true(self):
        email = "iphone@gamil.com"
        password = "123456789"
        user = User.objects.create(
            email=email
        )
        hashed_password = make_password(password)
        user.password = hashed_password
        user.save()
        storage = UserDB()
        response = storage.validate_password(email, password)
        assert response is True

    def test_validate_password_return_false(self):
        email = "iphone@gamil.com"
        password = "123456789"
        wrong_password = "125878"
        user = User.objects.create(
            email=email
        )
        hashed_password = make_password(password)
        user.password = hashed_password
        user.save()
        storage = UserDB()
        response = storage.validate_password(email, wrong_password)
        assert response is False

    def test_invalid_user_exception(self):
        email = "somerandom@gmail.com"
        password = "8966563698"
        storage = UserDB()
        with pytest.raises(InvalidUserException):
            storage.validate_password(email, password)