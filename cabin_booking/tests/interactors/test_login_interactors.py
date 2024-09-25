from unittest import mock

import pytest

from cabin_booking.exception import InvalidUserException
from cabin_booking.interactors.login_interactors import LoginInteractor
from cabin_booking.presenter.login_interactor_response import LoginInteractorResponse
from cabin_booking.storage.dtos import LoginResponseDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication
from cabin_booking.storage.user_db import UserDB


class TestLoginInteractor:
    @pytest.fixture()
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture()
    def login_response_mock(self):
        return mock.create_autospec(LoginInteractorResponse)

    @pytest.fixture()
    def user_authentication_mock(self):
        return mock.create_autospec(UserAuthentication)

    @pytest.fixture()
    def interactor(self, user_db_mock, login_response_mock, user_authentication_mock):
        return LoginInteractor(
            storage=user_db_mock,
            response=login_response_mock,
            authentication=user_authentication_mock
        )

    def test_validate_password_interactor(self, user_db_mock, login_response_mock, interactor,
                                          user_authentication_mock):
        # Arrange
        email = "sprite@gmail.com"
        password = "123456789"
        user_db_mock.validate_password.side_effect = InvalidUserException
        expected_response = "Invalid email id (don't have an account please signup to continue)"
        login_response_mock.invalid_user_response.return_value = expected_response
        # Act
        response = interactor.login_interactor(email, password)
        # Assert
        user_db_mock.validate_password.assert_called_once_with(email, password)
        login_response_mock.invalid_user_response.assert_called_once()
        user_db_mock.get_user_id.assert_not_called()
        user_authentication_mock.create_access_token.assert_not_called()
        user_authentication_mock.create_refresh_token.assert_not_called()
        assert response == expected_response

    def test_invalid_password(self, user_db_mock, login_response_mock, interactor, user_authentication_mock):
        # Arrange
        email = "sprite@gmail.com"
        password = "87654321"
        user_db_mock.validate_password.return_value = False
        expected_response = "Invalid Password (please check your password)"
        login_response_mock.invalid_password_exception_response.return_value = expected_response
        # Act
        response = interactor.login_interactor(email, password)
        # Assert
        user_db_mock.validate_password.assert_called_once_with(email, password)
        login_response_mock.invalid_password_exception_response.assert_called_once()
        user_db_mock.get_user_id.assert_not_called()
        user_authentication_mock.create_access_token.assert_not_called()
        user_authentication_mock.create_refresh_token.assert_not_called()
        assert response == expected_response

    def test_user_id(self, user_db_mock, login_response_mock, interactor, user_authentication_mock):
        # Arrange
        email = "sprite@gmail.com"
        password = "87654321"
        user_id = "28a9d6c1-29ee-4559-8ad8-add0fa902fe3"
        user_db_mock.validate_password.return_value = True
        expected_user_id = "28a9d6c1-29ee-4559-8ad8-add0fa902fe3"
        user_db_mock.get_user_id.return_value = expected_user_id
        expected_access_token = "29bccbcc56f84595be213a2cf76a6b5a"
        expected_refresh_token = "9daa1b2c89894e4fa0facce0f4ada9ed"
        user_authentication_mock.create_access_token.return_value = expected_access_token
        user_authentication_mock.create_refresh_token.return_value = expected_refresh_token
        excepted_response = {
            "access_token": expected_access_token,
            "refresh_token": expected_refresh_token
        }
        access_refresh_token_dto = LoginResponseDTO(
            access_token=expected_access_token,
            refresh_token=expected_refresh_token
        )
        login_response_mock.user_login_dto_response.return_value = excepted_response
        # Act
        response = interactor.login_interactor(email, password)
        # Assert
        user_db_mock.validate_password.assert_called_once_with(email, password)
        user_db_mock.get_user_id.assert_called_once_with(email)
        user_authentication_mock.create_access_token.assert_called_once_with(user_id)
        user_authentication_mock.create_refresh_token.assert_called_once_with(expected_access_token, user_id)
        login_response_mock.user_login_dto_response.assert_called_once_with(access_refresh_token_dto)
        assert response == excepted_response
