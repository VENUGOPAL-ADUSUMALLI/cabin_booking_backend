import pytest
from unittest import mock

from cabin_booking.databases.user_authentication_db import UserAuthentication
from cabin_booking.databases.user_db import UserDB
from cabin_booking.responses.login_interactor_response import LoginInteractorResponse
from cabin_booking.interactors.login_interactors import LoginInteractor


class TestLoginInteractor:
    @pytest.fixture()
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture()
    def login_interactor_response_mock(self):
        return mock.create_autospec(LoginInteractorResponse)

    @pytest.fixture()
    def user_authentication_mock(self):
        return mock.create_autospec(UserAuthentication)

    @pytest.fixture()
    def interactor(self, user_db_mock, login_interactor_response_mock, user_authentication_mock):
        return LoginInteractor(
            storage=user_db_mock,
            response=login_interactor_response_mock,
            authentication=user_authentication_mock
        )
