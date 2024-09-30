from datetime import datetime
from unittest import mock

import pytest

from cabin_booking.exception import InvalidCabinIDException, InvalidUserException
from cabin_booking.interactors.cabin_confirm_slots_interactor import ConfirmSlotInteractor
from cabin_booking.interactors.dtos import StartEndDateTimeDTO
from cabin_booking.presenter.cabin_confirm_slots_response import ConfirmSlotResponse
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


class TestCabinConfirmSlot:
    @pytest.fixture
    def booking_db_mock(self):
        return mock.create_autospec(BookingDB)

    @pytest.fixture
    def cabin_confirm_response_mock(self):
        return mock.create_autospec(ConfirmSlotResponse)

    @pytest.fixture
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture
    def interactor(self, booking_db_mock, cabin_confirm_response_mock, user_db_mock):
        return ConfirmSlotInteractor(
            storage=booking_db_mock,
            response=cabin_confirm_response_mock,
            user_db_storage=user_db_mock
        )

    def test_invalid_cabin_id(self, interactor, booking_db_mock, cabin_confirm_response_mock, user_db_mock):
        # Arrange
        cabin_id = 'b2ff1c68-5009-4d20-9103-01db46d7634288'
        start_date = "2024-10-28"
        end_date = "2024-10-29"
        purpose = "Meeting"
        user_id = " cf408174-f8d8-4ca9-ad5d-e2bd2fb68617"
        time_slots = ["18:00", "20:00"]
        booking_db_mock.validate_cabin_id.side_effect = InvalidCabinIDException
        expected_response = "Invalid Cabin id"
        cabin_confirm_response_mock.invalid_cabin_id_response.return_value = expected_response
        # Act
        response = interactor.confirm_slot_interactor(cabin_id, start_date, end_date, purpose, user_id, time_slots)
        # Assert
        booking_db_mock.validate_cabin_id.assert_called_once_with(cabin_id)
        cabin_confirm_response_mock.invalid_cabin_id_response.assert_called_once()
        user_db_mock.validate_user_id.assert_not_called()
        cabin_confirm_response_mock.invalid_user_id_response.assert_not_called()
        booking_db_mock.check_user_already_booked_slots.assert_not_called()
        cabin_confirm_response_mock.uniques_constraint_response.assert_not_called()
        booking_db_mock.create_cabin_slots.assert_not_called()
        cabin_confirm_response_mock.create_confirm_slots_success_response.assert_not_called()
        assert response == expected_response

    def test_invalid_user_exception(self, interactor, booking_db_mock, cabin_confirm_response_mock, user_db_mock):
        # Arrange
        cabin_id = 'b2ff1c68-5009-4d20-9103-01db46d76342'
        start_date = "2024-10-28"
        end_date = "2024-10-29"
        purpose = "Meeting"
        user_id = " cf408174-f8d8-4ca9-ad5d-e2bd2fb6861788"
        time_slots = ["18:00", "20:00"]
        user_db_mock.validate_user_id.side_effect = InvalidUserException
        expected_response = "Invalid User Id"
        cabin_confirm_response_mock.invalid_user_id_response.return_value = expected_response
        # Act
        response = interactor.confirm_slot_interactor(cabin_id, start_date, end_date, purpose, user_id, time_slots)
        # Assert
        user_db_mock.validate_user_id.assert_called_once_with(user_id)
        cabin_confirm_response_mock.invalid_user_id_response.assert_called_once()
        booking_db_mock.check_user_already_booked_slots.assert_not_called()
        cabin_confirm_response_mock.uniques_constraint_response.assert_not_called()
        booking_db_mock.create_cabin_slots.assert_not_called()
        cabin_confirm_response_mock.create_confirm_slots_success_response.assert_not_called()
        assert response == expected_response

    def test_already_booked_slots(self, interactor, booking_db_mock, cabin_confirm_response_mock, user_db_mock):
        # Arrange
        cabin_id = 'b2ff1c68-5009-4d20-9103-01db46d76342'
        start_date = "2024-10-28"
        end_date = "2024-10-29"
        purpose = "Meeting"
        user_id = " cf408174-f8d8-4ca9-ad5d-e2bd2fb6861788"
        time_slots = ["18:00", "20:00"]
        converted_start_date = datetime(2024, 10, 28)
        converted_end_date = datetime(2024, 10, 29)
        converted_time_slots = [datetime.strptime("18:00", "%H:%M"), datetime.strptime("20:00", "%H:%M"), ]
        booking_db_mock.check_user_already_booked_slots.return_value = True
        expected_response = 'slot already Booked'
        cabin_confirm_response_mock.uniques_constraint_response.return_value = expected_response
        # Act
        response = interactor.confirm_slot_interactor(cabin_id, start_date, end_date, purpose, user_id, time_slots)
        # Assert
        booking_db_mock.check_user_already_booked_slots.assert_called_once_with(cabin_id, converted_start_date,
                                                                                converted_end_date,
                                                                                converted_time_slots)
        cabin_confirm_response_mock.uniques_constraint_response.assert_called_once()
        booking_db_mock.create_cabin_slots.assert_not_called()
        cabin_confirm_response_mock.create_confirm_slots_success_response.assert_not_called()
        assert response == expected_response

    def test_create_cabin_slots(self, interactor, booking_db_mock, cabin_confirm_response_mock, user_db_mock):
        # Arrange
        cabin_id = 'b2ff1c68-5009-4d20-9103-01db46d76342'
        start_date = "2024-10-28"
        end_date = "2024-10-29"
        purpose = "Meeting"
        user_id = " cf408174-f8d8-4ca9-ad5d-e2bd2fb68617"
        time_slots = ["18:00", "20:00"]
        list_start_end_date_time_dto = [
            StartEndDateTimeDTO(
                start_date_time=datetime(2024, 10, 28, 18, 0),
                end_date_time=datetime(2024, 10, 28, 19, 0),
            ),
            StartEndDateTimeDTO(
                start_date_time=datetime(2024, 10, 28, 20, 0),
                end_date_time=datetime(2024, 10, 28, 21, 0),
            ),
            StartEndDateTimeDTO(
                start_date_time=datetime(2024, 10, 29, 18, 0),
                end_date_time=datetime(2024, 10, 29, 19, 0),
            ),
            StartEndDateTimeDTO(
                start_date_time=datetime(2024, 10, 29, 20, 0),
                end_date_time=datetime(2024, 10, 29, 21, 0),
            ),
        ]
        booking_db_mock.check_user_already_booked_slots.return_value = False
        expected_response = "slot Booked Successfully"
        cabin_confirm_response_mock.create_confirm_slots_success_response.return_value = expected_response
        # Act
        response = interactor.confirm_slot_interactor(cabin_id, start_date, end_date, purpose, user_id, time_slots)
        # Assert
        booking_db_mock.create_cabin_slots.assert_called_once_with(cabin_id, purpose, user_id,
                                                                   list_start_end_date_time_dto)
        cabin_confirm_response_mock.create_confirm_slots_success_response.assert_called_once()
        assert response == expected_response
