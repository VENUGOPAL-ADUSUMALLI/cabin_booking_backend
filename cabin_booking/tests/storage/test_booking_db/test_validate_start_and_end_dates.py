from datetime import datetime

import mock
import pytest

from cabin_booking.exception import InvalidDateRangeException
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestValidateStartEndDates:
    @pytest.fixture()
    def user_db_storage_mock(self):
        return UserDB()

    def test_validate_start_end_date_invalid_date_exception(self, user_db_storage_mock):
        start_date = datetime(2024, 10, 27)
        end_date = datetime(2024, 10, 25)
        storage = BookingDB(user_db_storage_mock)
        with pytest.raises(InvalidDateRangeException):
            storage.validate_start_and_end_dates(start_date, end_date)

    def test_validate_start_end_date(self, user_db_storage_mock):
        start_date = datetime(2024, 10, 27)
        end_date = datetime(2024, 10, 28)
        storage = BookingDB(user_db_storage_mock)
        response = storage.validate_start_and_end_dates(start_date, end_date)
        assert response is None
