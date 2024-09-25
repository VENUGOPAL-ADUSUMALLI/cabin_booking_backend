from unittest import mock

import pytest

from cabin_booking.exception import InvalidUserException
from cabin_booking.interactors.profile_interactor import ProfileInteractor
from cabin_booking.presenter.profile_interactor_response import ProfileInteractorResponse
from cabin_booking.storage.dtos import ProfileDTO
from cabin_booking.storage.user_db import UserDB


class TestProfileInteractor:
    @pytest.fixture()
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture()
    def profile_interactor_response_mock(self):
        return mock.create_autospec(ProfileInteractorResponse)

    @pytest.fixture()
    def interactor(self, user_db_mock, profile_interactor_response_mock):
        return ProfileInteractor(
            storage=user_db_mock,
            response=profile_interactor_response_mock
        )

    def test_invalid_user_exception(self, interactor, user_db_mock, profile_interactor_response_mock):
        user_id = 'a10a2749-74a8-4a34-82f0-54a9c40de498'
        user_db_mock.profile.side_effect = InvalidUserException
        expected_response = 'Invalid User'
        profile_interactor_response_mock.invalid_user_response.return_value = expected_response
        response = interactor.get_user_details_profile_interactor(user_id)
        user_db_mock.profile.assert_called_once_with(user_id)
        profile_interactor_response_mock.invalid_user_response.assert_called_once_with()
        profile_interactor_response_mock.user_details_dto_response.assert_not_called()
        assert response == expected_response

    def test_get_user_details_success(self, interactor, user_db_mock, profile_interactor_response_mock):
        user_id = 'a10a2749-74a8-4a34-82f0-54a9c40de498'
        email = "maaza@gmail.com"
        username = "Maaza"
        first_name = "Coco cola"
        last_name = "Maaza"
        team_name = "waste drinks"
        contact_number = "8441844128"
        user_profile_dto = ProfileDTO(
            email=email,
            first_name=first_name,
            last_name=last_name,
            team_name=team_name,
            contact_number=contact_number,
            username=username
        )
        user_db_mock.profile.return_value = user_profile_dto
        expected_response = ProfileDTO(
            email=email,
            first_name=first_name,
            last_name=last_name,
            team_name=team_name,
            contact_number=contact_number,
            username=username
        )
        profile_interactor_response_mock.user_details_dto_response.return_value = expected_response
        response = interactor.get_user_details_profile_interactor(user_id)
        user_db_mock.profile.assert_called_once_with(user_id)
        profile_interactor_response_mock.user_details_dto_response.assert_called_once_with(user_profile_dto)
        assert response == expected_response
