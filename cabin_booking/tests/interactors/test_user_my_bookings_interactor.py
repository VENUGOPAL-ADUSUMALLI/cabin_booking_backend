from unittest import mock

import pytest

from cabin_booking.exception import InvalidUserException, NoBookingsException
from cabin_booking.interactors.my_bookings_interactor import MyBookingsInteractor
from cabin_booking.presenter.my_bookings_response import MyBookingsResponse
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.dtos import UserBookingDetailsDTO
from cabin_booking.storage.user_db import UserDB


class TestUserMyBookingsInteractor:
    @pytest.fixture
    def bookings_db_mock(self):
        return mock.create_autospec(BookingDB)

    @pytest.fixture
    def my_bookings_response_mock(self):
        return mock.create_autospec(MyBookingsResponse)

    @pytest.fixture
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture
    def interactor(self, bookings_db_mock, my_bookings_response_mock, user_db_mock):
        bookings_db_mock.user_db_storage = user_db_mock
        return MyBookingsInteractor(
            storage=bookings_db_mock,
            response=my_bookings_response_mock
        )

    def test_invalid_user_exception(self, interactor, bookings_db_mock, my_bookings_response_mock):
        # Arrange
        user_id = "cf408174-f8d8-4ca9-ad5d-e2bd2fb68617"
        bookings_db_mock.validate_user_id.side_effect = InvalidUserException
        expected_response = "Invalid User"
        my_bookings_response_mock.invalid_user_exception.return_value = expected_response
        # Act
        response = interactor.get_user_my_bookings_interactor(user_id)
        # Assert
        bookings_db_mock.validate_user_id.assert_called_once_with(user_id)
        my_bookings_response_mock.invalid_user_exception.assert_called_once()
        bookings_db_mock.get_user_bookings.assert_not_called()
        my_bookings_response_mock.no_bookings_exception.assert_not_called()
        my_bookings_response_mock.my_bookings_success_response.assert_not_called()
        assert response == expected_response

    def test_no_bookings_exception(self, interactor, bookings_db_mock, my_bookings_response_mock):
        # Arrange
        user_id = "cf408174-f8d8-4ca9-ad5d-e2bd2fb68617"
        bookings_db_mock.get_user_bookings.side_effect = NoBookingsException
        expected_response = 'No Bookings'
        my_bookings_response_mock.no_bookings_exception.return_value = expected_response
        # Act
        response = interactor.get_user_my_bookings_interactor(user_id)
        # Assert
        bookings_db_mock.get_user_bookings.assert_called_once_with(user_id)
        my_bookings_response_mock.no_bookings_exception.assert_called_once()
        my_bookings_response_mock.my_bookings_success_response.assert_not_called()
        assert response == expected_response

    def test_user_bookings_success_response(self, interactor, bookings_db_mock, my_bookings_response_mock):
        # Arrange
        user_id = "cf408174-f8d8-4ca9-ad5d-e2bd2fb68617"
        booking_db_dto = [UserBookingDetailsDTO(
            floor_name='Fourth Floor',
            cabin_name='Call pod 3b',
            booking_id='215e37da-b01c-4fae-b262-faa986984056',
            start_date="2024-09-23",
            end_date="2024-09-25",
            time_slots=[
                "11:00",
                "13:00"
            ]
        )
        ]
        bookings_db_mock.get_user_bookings.return_value = booking_db_dto
        expected_response = [
            {
                "Floor_name": "Fourth Floor",
                "cabin_name": "Call pod 3b",
                "Booking_id": "215e37da-b01c-4fae-b262-faa986984056",
                "start_date": "2024-09-23",
                "end_date": "2024-09-25",
                "time_slots": [
                    "11:00",
                    "13:00"
                ]
            },
            {
                "Floor_name": "Fourth Floor",
                "cabin_name": "Call pod 3e",
                "Booking_id": "6b47d1f4-b95e-4891-8ad2-06f96bec0711",
                "start_date": "2024-09-01",
                "end_date": "2024-09-03",
                "time_slots": [
                    "18:00",
                    "20:00"
                ]
            }
        ]
        my_bookings_response_mock.my_bookings_success_response.return_value = expected_response
        # Act
        response = interactor.get_user_my_bookings_interactor(user_id)
        # Assert
        bookings_db_mock.get_user_bookings.assert_called_once_with(user_id)
        my_bookings_response_mock.my_bookings_success_response.assert_called_once()
        assert response == expected_response
