from unittest import mock

import pytest

from cabin_booking.exception import InvalidRefreshTokenException, InvalidAccessTokenException
from cabin_booking.interactors.logout_interactor import LogoutInteractor
from cabin_booking.presenter.logout_responses import LogoutResponse
from cabin_booking.storage.user_authentication_db import UserAuthentication


class TestLogoutInteractor:
    @pytest.fixture
    def user_authentication_db_mock(self):
        return mock.create_autospec(UserAuthentication)

    @pytest.fixture
    def logout_interactor_response_mock(self):
        return mock.create_autospec(LogoutResponse)

    @pytest.fixture
    def interactor(self, user_authentication_db_mock, logout_interactor_response_mock):
        return LogoutInteractor(
            authentication=user_authentication_db_mock,
            response=logout_interactor_response_mock
        )

    def test_invalid_refresh_token_exception(self, interactor, user_authentication_db_mock,
                                             logout_interactor_response_mock):
        # Arrange
        access_token = "03b0948b8e3c49f4a172160357bb595e"
        refresh_token = "b4b21823c56343c5b9920a2ca1f78ed6"
        user_authentication_db_mock.expire_access_token_refresh_token.side_effect = InvalidRefreshTokenException
        expected_response = "Invalid refresh token"
        logout_interactor_response_mock.invalid_refresh_token_response.return_value = expected_response
        # Act
        response = interactor.logout_interactor(access_token, refresh_token)
        # Assert
        user_authentication_db_mock.expire_access_token_refresh_token.assert_called_once_with(access_token,
                                                                                              refresh_token)
        logout_interactor_response_mock.invalid_refresh_token_response.assert_called_once()
        logout_interactor_response_mock.invalid_access_token_response.assert_not_called()
        logout_interactor_response_mock.logout_success_response.assert_not_called()
        assert response == expected_response

    def test_invalid_access_token_exception(self, interactor, user_authentication_db_mock,
                                            logout_interactor_response_mock):
        # Arrange
        access_token = "03b0948b8e3c49f4a172160357bb595e"
        refresh_token = "b4b21823c56343c5b9920a2ca1f78ed6"
        user_authentication_db_mock.expire_access_token_refresh_token.side_effect = InvalidAccessTokenException
        expected_response = "Invalid Access token"
        logout_interactor_response_mock.invalid_access_token_response.return_value = expected_response
        # Act
        response = interactor.logout_interactor(access_token, refresh_token)
        # Assert
        user_authentication_db_mock.expire_access_token_refresh_token.assert_called_once_with(access_token,
                                                                                              refresh_token)
        logout_interactor_response_mock.invalid_access_token_response.assert_called_once()
        logout_interactor_response_mock.logout_success_response.assert_not_called()
        assert response == expected_response

    def test_logout_success_response(self, interactor, user_authentication_db_mock, logout_interactor_response_mock):
        # Arrange
        access_token = "03b0948b8e3c49f4a172160357bb595e"
        refresh_token = "b4b21823c56343c5b9920a2ca1f78ed6"
        expected_response = 'logged out successfully'
        logout_interactor_response_mock.logout_success_response.return_value = expected_response
        # Act
        response = interactor.logout_interactor(access_token, refresh_token)
        # Assert
        user_authentication_db_mock.expire_access_token_refresh_token.assert_called_once_with(access_token,
                                                                                              refresh_token)
        logout_interactor_response_mock.logout_success_response.assert_called_once()
        assert response == expected_response
