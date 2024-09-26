from unittest import mock

import pytest

from cabin_booking.exception import InvalidRefreshTokenException, RefreshTokenExpiredException
from cabin_booking.interactors.create_refresh_access_token_interactor import CreateRefreshAccessToken
from cabin_booking.presenter.create_refresh_access_token_response import CreateRefreshAccessTokensResponse
from cabin_booking.storage.dtos import CreateRefreshTokenDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication


class TestCreateAccessTokenUsingRefreshToken:
    @pytest.fixture()
    def refresh_access_token_response_mock(self):
        return mock.create_autospec(CreateRefreshAccessTokensResponse)

    @pytest.fixture()
    def user_authentication_mock(self):
        return mock.create_autospec(UserAuthentication)

    @pytest.fixture()
    def interactor(self, refresh_access_token_response_mock, user_authentication_mock):
        return CreateRefreshAccessToken(
            response=refresh_access_token_response_mock,
            authentication=user_authentication_mock
        )

    def test_invalid_refresh_token(self, interactor, refresh_access_token_response_mock,
                                   user_authentication_mock):
        # Arrange
        refresh_token = '80263b6143524c10935aa61372601e03'
        user_authentication_mock.create_refresh_access_token.side_effect = InvalidRefreshTokenException
        expected_response = 'Invalid refresh token'
        refresh_access_token_response_mock.invalid_refresh_token_response.return_value = expected_response
        # Act
        response = interactor.refresh_access_token_interactor(refresh_token)
        # Assert
        user_authentication_mock.create_refresh_access_token.assert_called_once_with(refresh_token)
        refresh_access_token_response_mock.invalid_refresh_token_response.assert_called_once_with()
        refresh_access_token_response_mock.token_expired_response.assert_not_called()
        refresh_access_token_response_mock.get_refresh_access_token_success_response.assert_not_called()
        assert response == expected_response

    def test_token_expiry_exception(self, interactor, refresh_access_token_response_mock, user_authentication_mock):
        # Arrange
        refresh_token = '80263b6143524c10935aa61372601e03'
        user_authentication_mock.create_refresh_access_token.side_effect = RefreshTokenExpiredException
        expected_response = 'Token expired please login again'
        refresh_access_token_response_mock.token_expired_response.return_value = expected_response
        # Act
        response = interactor.refresh_access_token_interactor(refresh_token)
        # Assert
        user_authentication_mock.create_refresh_access_token.assert_called_once_with(refresh_token)
        refresh_access_token_response_mock.token_expired_response.assert_called_once_with()
        refresh_access_token_response_mock.get_refresh_access_token_success_response.assert_not_called()
        assert response == expected_response

    def test_create_access_token_using_refresh_token(self, interactor, refresh_access_token_response_mock,
                                                     user_authentication_mock):
        # Arrange
        refresh_token = '80263b6143524c10935aa61372601e03'
        access_token = 'b4b21823c56343c5b9920a2ca1f78ed6'
        access_token_dto = CreateRefreshTokenDTO(
            access_token=access_token
        )
        user_authentication_mock.create_refresh_access_token.return_value = access_token_dto
        expected_response = {
            "access_token": access_token
        }
        refresh_access_token_response_mock.get_refresh_access_token_success_response.return_value = expected_response
        user_authentication_mock.create_access_token.return_value = access_token
        # Act
        response = interactor.refresh_access_token_interactor(refresh_token)
        # Assert
        user_authentication_mock.create_refresh_access_token.assert_called_once_with(refresh_token)
        refresh_access_token_response_mock.get_refresh_access_token_success_response.assert_called_once_with(
            access_token_dto)
        assert response == expected_response
