from unittest import mock

import pytest

from cabin_booking.exception import InvalidCabinIDException, InvalidDetailsException
from cabin_booking.interactors.user_booked_slots_interactor import UserBookedSlotsInteractor
from cabin_booking.presenter.user_booked_slots_response import UserBookedSlotResponse
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.dtos import BookingProfileDTO


class TestUserBookedSlots:
    @pytest.fixture
    def booking_db_mock(self):
        return mock.create_autospec(BookingDB)

    @pytest.fixture
    def user_booking_response_mock(self):
        return mock.create_autospec(UserBookedSlotResponse)

    @pytest.fixture
    def interactor(self, booking_db_mock, user_booking_response_mock):
        return UserBookedSlotsInteractor(
            storage=booking_db_mock,
            response=user_booking_response_mock
        )

    def test_invalid_cabin_id(self, interactor, booking_db_mock, user_booking_response_mock):
        # Arrange
        cabin_id = "2a1fa6fc-83fa-4ed6-b9af-8ce4d0c315d3",
        start_date_time = "2024-09-23 11:00"
        end_date_time = "2024-09-23 12:00"
        booking_db_mock.validate_cabin_id.side_effect = InvalidCabinIDException
        expected_response = "Invalid Cabin id"
        user_booking_response_mock.invalid_cabin_id_response.return_value = expected_response
        # Act
        response = interactor.user_booked_slot_interactor(cabin_id, start_date_time, end_date_time)
        # Assert
        booking_db_mock.validate_cabin_id.assert_called_once_with(cabin_id)
        user_booking_response_mock.invalid_cabin_id_response.assert_called_once()
        booking_db_mock.get_user_booked_slot.assert_not_called()
        user_booking_response_mock.user_booked_slots_response.assert_not_called()
        assert response == expected_response

    def test_invalid_details_exception(self, interactor, booking_db_mock, user_booking_response_mock):
        # Arrange
        cabin_id = "11791db9-8d32-431e-b309-c7e6435dd95d",
        start_date_time = "2024-09-23 11:00"
        end_date_time = "2024-09-23 12:00"
        booking_db_mock.get_user_booked_slot.side_effect = InvalidDetailsException
        expected_response = 'Invalid details'
        user_booking_response_mock.invalid_details_exception.return_value = expected_response
        # Act
        response = interactor.user_booked_slot_interactor(cabin_id, start_date_time, end_date_time)
        # Assert
        booking_db_mock.get_user_booked_slot.assert_called_once_with(cabin_id, start_date_time, end_date_time)
        user_booking_response_mock.invalid_details_exception.assert_called_once()
        user_booking_response_mock.user_booked_slots_response.assert_not_called()
        assert response == expected_response

    def test_user_booked_slots_response(self, interactor, booking_db_mock, user_booking_response_mock):
        # Arrange
        cabin_id = "11791db9-8d32-431e-b309-c7e6435dd95d"
        start_date_time = "2024-09-23 11:00"
        end_date_time = "2024-09-23 12:00"
        user_details_dto = BookingProfileDTO(
            email="ggh@gmail.com",
            first_name="Kiran",
            last_name="chenna",
            username="sahoorey",
            team_name="air operations",
            contact_number="98255652615",
            purpose="Meeting"
        )
        expected_response = {
            "email": "ggh@gmail.com",
            "username": "sahoorey",
            "first_name": "Kiran",
            "last_name": "chenna",
            "team_name": "air operations",
            "contact_number": "98255652615",
            "purpose": "Meeting"
        }
        booking_db_mock.get_user_booked_slot.return_value = user_details_dto
        user_booking_response_mock.user_booked_slots_response.return_value = expected_response
        # Act
        response = interactor.user_booked_slot_interactor(cabin_id, start_date_time, end_date_time)
        # Assert
        booking_db_mock.get_user_booked_slot.assert_called_once_with(cabin_id, start_date_time, end_date_time)
        user_booking_response_mock.user_booked_slots_response.assert_called_once_with(user_details_dto)
        assert response == expected_response
