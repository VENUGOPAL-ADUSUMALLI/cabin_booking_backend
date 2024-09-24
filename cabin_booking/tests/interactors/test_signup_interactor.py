from unittest import mock

import pytest

from cabin_booking.exception import UserAlreadyExistsException
from cabin_booking.interactors.signup_interactor import SignupInteractor
from cabin_booking.presenter.signup_interactor_response import SignupInteractorResponse
from cabin_booking.storage.dtos import ProfileDTO
from cabin_booking.storage.user_authentication_db import UserAuthentication
from cabin_booking.storage.user_db import UserDB


class TestSignupInteractor:
    @pytest.fixture()
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture()
    def signup_interactor_response_mock(self):
        return mock.create_autospec(SignupInteractorResponse)

    @pytest.fixture()
    def user_authentication_mock(self):
        return mock.create_autospec(UserAuthentication)

    @pytest.fixture()
    def interactor(self, user_db_mock, signup_interactor_response_mock, user_authentication_mock):
        return SignupInteractor(
            storage=user_db_mock,
            response=signup_interactor_response_mock,
            authentication=user_authentication_mock
        )

    def test_user_already_exception(self, interactor, user_db_mock, signup_interactor_response_mock):
        email = "sprite@gmail.com"
        password = "87654321"
        username = "sprite"
        first_name = "Coco cola"
        last_name = "Pepsi"
        team_name = "waste drinks"
        contact_number = "8441844128"
        user_db_mock.create_user_for_signup.side_effect = UserAlreadyExistsException
        expected_response = "User Already exist"
        signup_interactor_response_mock.user_already_exists_response.return_value = expected_response
        response = interactor.signup_interactor(email, username, password, first_name, last_name, team_name,
                                                contact_number)
        user_db_mock.create_user_for_signup.assert_called_once_with(email, password, username, first_name, last_name,
                                                                    team_name, contact_number)
        signup_interactor_response_mock.user_already_exists_response.assert_called_once_with()
        assert response == expected_response

    def test_create_user_success(self, interactor, user_db_mock, signup_interactor_response_mock,
                                 user_authentication_mock):
        email = "maaza@gmail.com"
        password = "87654321"
        username = "Maaza"
        first_name = "Coco cola"
        last_name = "Maaza"
        team_name = "waste drinks"
        contact_number = "8441844128"
        user_id = 'a10a2749-74a8-4a34-82f0-54a9c40de498'
        user_account_dto_response = ProfileDTO(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            team_name=team_name,
            contact_number=contact_number

        )
        user_db_mock.create_user_for_signup.return_value = user_account_dto_response
        expected_user_id = 'a10a2749-74a8-4a34-82f0-54a9c40de498'
        user_db_mock.get_user_id.return_value = expected_user_id
        expected_access_token = "133319343d9946bb8f15d6833e4eab90"
        expected_refresh_token = "71ca7c8528e24b3eaf689cc597064179"
        user_authentication_mock.create_access_token.return_value = expected_access_token
        user_authentication_mock.create_refresh_token.return_value = expected_refresh_token
        expected_response = {
            "access_token": expected_access_token,
            "refresh_token": expected_refresh_token
        }
        signup_interactor_response_mock.user_signup_dto_response.return_value = expected_response
        response = interactor.signup_interactor(email, password, username, first_name, last_name, team_name,
                                                contact_number)
        user_db_mock.create_user_for_signup.assert_called_once_with(email, username, password, first_name, username,
                                                                    team_name, contact_number)
        user_db_mock.get_user_id.assert_called_once_with(email)
        user_authentication_mock.create_access_token.assert_called_once_with(user_id)
        user_authentication_mock.create_refresh_token.assert_called_once_with(expected_access_token, user_id)
        assert response == expected_response
