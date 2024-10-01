from datetime import time
from unittest import mock

import pytest

from cabin_booking.exception import InvalidCabinIDException, InvalidDateRangeException
from cabin_booking.interactors.dtos import CabinTimeSlotsAvailabilityDTO, TimeSlotsDTO
from cabin_booking.interactors.get_cabin_wise_slots_interactor import CabinWiseSlotsInteractor
from cabin_booking.presenter.get_cabins_slots_response import CabinSlotsDetailsResponse
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.dtos import CabinTimeSlotsDTO


class TestCabinSlots:
    @pytest.fixture
    def booking_db_mock(self):
        return mock.create_autospec(BookingDB)

    @pytest.fixture
    def cabin_slots_response_mock(self):
        return mock.create_autospec(CabinSlotsDetailsResponse)

    @pytest.fixture
    def interactor(self, booking_db_mock, cabin_slots_response_mock):
        return CabinWiseSlotsInteractor(
            storage=booking_db_mock,
            response=cabin_slots_response_mock
        )

    def test_invalid_cabin_id_exception(self, interactor, booking_db_mock, cabin_slots_response_mock):
        # Arrange
        cabin_ids = ["b2ff1c68-5009-4d20-9103-01db46d76342888"]
        start_date = "2024-10-28"
        end_date = "2024-10-28"
        booking_db_mock.validate_cabin_id_for_cabin_slots.side_effect = InvalidCabinIDException
        expected_response = 'Invalid Cabin Id'
        cabin_slots_response_mock.invalid_cabin_id_exception.return_value = expected_response
        # Act
        response = interactor.get_cabin_slots_interactor(cabin_ids, start_date, end_date)
        # assert
        booking_db_mock.validate_cabin_id_for_cabin_slots.assert_called_once_with(cabin_ids)
        cabin_slots_response_mock.invalid_cabin_id_exception.assert_called_once()
        booking_db_mock.validate_start_and_end_dates.assert_not_called()
        cabin_slots_response_mock.invalid_date_range_exception.assert_not_called()
        booking_db_mock.get_cabin_slots.assert_not_called()
        cabin_slots_response_mock.get_cabin_slot_details_success_response.assert_not_called()
        assert response == expected_response

    def test_invalid_date_exception(self, interactor, booking_db_mock, cabin_slots_response_mock):
        # Arrange
        cabin_ids = ["b2ff1c68-5009-4d20-9103-01db46d76342"]
        start_date = "2024-10-28"
        end_date = "2024-10-27"
        booking_db_mock.validate_start_and_end_dates.side_effect = InvalidDateRangeException
        expected_response = 'Invalid Date'
        cabin_slots_response_mock.invalid_date_range_exception.return_value = expected_response
        # Act
        response = interactor.get_cabin_slots_interactor(cabin_ids, start_date, end_date)
        # Assert
        booking_db_mock.validate_start_and_end_dates.assert_called_once_with(start_date, end_date)
        cabin_slots_response_mock.invalid_date_range_exception.assert_called_once()
        booking_db_mock.get_cabin_slots.assert_not_called()
        cabin_slots_response_mock.get_cabin_slot_details_success_response.assert_not_called()
        assert response == expected_response

    def test_cabin_slots(self, interactor, booking_db_mock, cabin_slots_response_mock):
        # Arrange
        cabin_ids = ["b2ff1c68-5009-4d20-9103-01db46d76342"]
        start_date = "2024-10-28"
        end_date = "2024-10-29"
        cabin_slots_response = [CabinTimeSlotsDTO(
            cabin_id='b2ff1c68-5009-4d20-9103-01db46d76342',
            time_slots=[
                time(18, 0),
                time(20, 0)
            ]
        )]
        booking_db_mock.get_cabin_slots.return_value = cabin_slots_response
        cabin_availability_dto = [CabinTimeSlotsAvailabilityDTO(
            cabin_id='b2ff1c68-5009-4d20-9103-01db46d763420',
            time_slots=[
                TimeSlotsDTO(slot=time(9, 0), availability=True),
                TimeSlotsDTO(slot=time(10, 0), availability=True),
                TimeSlotsDTO(slot=time(11, 0), availability=True),
                TimeSlotsDTO(slot=time(12, 0), availability=True),
                TimeSlotsDTO(slot=time(13, 0), availability=True),
                TimeSlotsDTO(slot=time(14, 0), availability=True),
                TimeSlotsDTO(slot=time(15, 0), availability=True),
                TimeSlotsDTO(slot=time(16, 0), availability=True),
                TimeSlotsDTO(slot=time(17, 0), availability=True),
                TimeSlotsDTO(slot=time(18, 0), availability=False),
                TimeSlotsDTO(slot=time(19, 0), availability=True),
                TimeSlotsDTO(slot=time(20, 0), availability=False),
                TimeSlotsDTO(slot=time(21, 0), availability=True),
                TimeSlotsDTO(slot=time(22, 0), availability=True),
                TimeSlotsDTO(slot=time(23, 0), availability=True),

            ]
        )]
        expected_response = {
            "cabin_id": "b2ff1c68-5009-4d20-9103-01db46d76342",
            "time_slots": [
                {
                    "slot": "09:00:00",
                    "availability": True
                },
                {
                    "slot": "10:00:00",
                    "availability": True
                },
                {
                    "slot": "11:00:00",
                    "availability": True
                },
                {
                    "slot": "12:00:00",
                    "availability": True
                },
                {
                    "slot": "13:00:00",
                    "availability": True
                },
                {
                    "slot": "14:00:00",
                    "availability": True
                },
                {
                    "slot": "15:00:00",
                    "availability": True
                },
                {
                    "slot": "16:00:00",
                    "availability": True
                },
                {
                    "slot": "17:00:00",
                    "availability": True
                },
                {
                    "slot": "18:00:00",
                    "availability": False
                },
                {
                    "slot": "19:00:00",
                    "availability": True
                },
                {
                    "slot": "20:00:00",
                    "availability": False
                },
                {
                    "slot": "21:00:00",
                    "availability": True
                },
                {
                    "slot": "22:00:00",
                    "availability": True
                },
                {
                    "slot": "23:00:00",
                    "availability": True
                }
            ]
        }
        cabin_slots_response_mock.get_cabin_slot_details_success_response.return_value = expected_response
        # Act
        response = interactor.get_cabin_slots_interactor(cabin_ids, start_date, end_date)
        # Assert
        booking_db_mock.get_cabin_slots.assert_called_once_with(cabin_ids, start_date, end_date)
        cabin_slots_response_mock.get_cabin_slot_details_success_response.assert_called_once()
        assert response == expected_response
