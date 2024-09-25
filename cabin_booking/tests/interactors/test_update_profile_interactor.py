from http.client import responses
from unittest import mock

import pytest

from cabin_booking.exception import InvalidUserException
from cabin_booking.interactors.user_profile_update_interactor import UserProfileUpdate
from cabin_booking.presenter.user_profile_update_response import UserProfileUpdateResponse
from cabin_booking.storage.dtos import UpdateProfileDTO
from cabin_booking.storage.user_db import UserDB


class TestUpdateProfileInteractor:
    @pytest.fixture()
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture()
    def update_user_profile_response_mock(self):
        return mock.create_autospec(UserProfileUpdateResponse)

    @pytest.fixture()
    def interactor(self, user_db_mock, update_user_profile_response_mock):
        return UserProfileUpdate(
            storage=user_db_mock,
            response=update_user_profile_response_mock
        )

    def test_invalid_user_exception(self, user_db_mock, update_user_profile_response_mock, interactor):
        # Arrange
        username = "Maaza"
        first_name = "Coco cola"
        last_name = "Maaza"
        team_name = "waste drinks"
        contact_number = "8441844128",
        user_id = "a10a2749-74a8-4a34-82f0-54a9c40de498"
        user_db_mock.validate_user_id.side_effect = InvalidUserException
        expected_response = 'Invalid user'
        update_user_profile_response_mock.invalid_user_exception.return_value = expected_response
        # Act
        response = interactor.update_user_profile_interactor(username, first_name, last_name, contact_number, team_name,
                                                             user_id)
        # Assert
        user_db_mock.validate_user_id.assert_called_once_with(user_id)
        update_user_profile_response_mock.invalid_user_exception.assert_called_once()
        user_db_mock.update_user_profile.assert_not_called()
        update_user_profile_response_mock.update_user_profile_success_response.assert_not_called()
        assert response == expected_response

    def test_update_profile_success(self, interactor, user_db_mock, update_user_profile_response_mock):
        # Assert
        username = "Maaza"
        first_name = "Coco cola"
        last_name = "Maaza"
        team_name = "waste drinks"
        contact_number = "8441844128",
        user_id = "a10a2749-74a8-4a34-82f0-54a9c40de498"
        user_db_mock.validate_user_id.return_value = user_id
        expected_rows_updated = 1
        user_db_mock.update_user_profile.return_value = expected_rows_updated
        expected_response = 'Profile Updated Successfully'
        update_user_profile_response_mock.update_user_profile_success_response.return_value = expected_response
        # Act
        response = interactor.update_user_profile_interactor(username, first_name, last_name, contact_number, team_name,
                                                             user_id)
        # Assert
        user_db_mock.validate_user_id.assert_called_once_with(user_id)
        user_db_mock.update_user_profile.assert_called_once_with(username, first_name, last_name, contact_number,
                                                                 team_name, user_id)
        update_user_profile_response_mock.update_user_profile_success_response.assert_called_once_with()
        assert response == expected_response
