import mock

import pytest
from django.template.defaultfilters import first

from cabin_booking.exception import InvalidUserException
from cabin_booking.interactors.update_password_interactor import UpdatePasswordInteractor
from cabin_booking.presenter.update_password_response import UpdatePasswordResponse
from cabin_booking.storage.dtos import ProfileDTO
from cabin_booking.storage.user_db import UserDB


class TestUpdatePasswordInteractor:
    @pytest.fixture()
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture()
    def update_password_response_mock(self):
        return mock.create_autospec(UpdatePasswordResponse)

    @pytest.fixture()
    def interactor(self, user_db_mock, update_password_response_mock):
        return UpdatePasswordInteractor(
            storage=user_db_mock,
            response=update_password_response_mock
        )

    def test_validate_password_invalid_user_exception(self, interactor, user_db_mock, update_password_response_mock):
        # Arrange
        email = "maaza23@gmail.com"
        old_password = "123456789"
        new_password = "87654321"
        user_db_mock.validate_password.side_effect = InvalidUserException
        expected_response = 'invalid email id'
        update_password_response_mock.invalid_user_response.return_value = expected_response
        # Act
        response = interactor.update_password_interactor(email, old_password, new_password)
        # Assert
        user_db_mock.validate_password.assert_called_once_with(email, old_password)
        update_password_response_mock.invalid_user_response.assert_called_once()
        user_db_mock.get_user_id.assert_not_called()
        user_db_mock.setup_newpassword.assert_not_called()
        assert response == expected_response

    def test_invalid_user_password(self, interactor, user_db_mock, update_password_response_mock):
        # Arrange
        email = "maaza23@gmail.com"
        old_password = "123456789"
        new_password = "87654321"
        user_db_mock.validate_password.return_value = False
        expected_response = 'Invalid Password'
        update_password_response_mock.invalid_password_response.return_value = expected_response
        # Act
        response = interactor.update_password_interactor(email, old_password, new_password)
        # Assert
        user_db_mock.validate_password.assert_called_once_with(email, old_password)
        update_password_response_mock.invalid_password_response.assert_called_once()
        user_db_mock.get_user_id.assert_not_called()
        user_db_mock.setup_newpassword.assert_not_called()
        assert response == expected_response

    def test_update_password_success(self, interactor, user_db_mock, update_password_response_mock):
        # Arrange
        email = "maaza23@gmail.com"
        old_password = "123456789"
        new_password = "87654321"
        username = "Maaza"
        first_name = "Coco cola"
        last_name = "Maaza"
        team_name = "waste drinks"
        contact_number = "8441844128"
        user_id = 'a10a2749-74a8-4a34-82f0-54a9c40de498'
        user_db_mock.validate_password.return_value = True
        expected_user_id = 'a10a2749-74a8-4a34-82f0-54a9c40de498'
        user_db_mock.get_user_id.return_value = expected_user_id
        user_profile_dto = ProfileDTO(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            team_name=team_name,
            contact_number=contact_number
        )
        user_db_mock.setup_newpassword.return_value = user_profile_dto
        expected_response = "password updated successfully"
        update_password_response_mock.password_update_successfull_response.return_value = expected_response
        # Act
        response = interactor.update_password_interactor(email, old_password, new_password)
        # Assert
        user_db_mock.get_user_id.assert_called_once_with(email)
        user_db_mock.setup_newpassword.assert_called_once_with(user_id, new_password)
        update_password_response_mock.password_update_successfull_response.assert_called_once()
        assert response == expected_response
