import mock
import pytest

from cabin_booking.exception import InvalidBookingIDException
from cabin_booking.interactors.delete_user_bookings_interactor import DeleteUserBookings
from cabin_booking.presenter.delete_user_bookings_response import DeleteUserBookingsResponse
from cabin_booking.storage.booking_db import BookingDB
from cabin_booking.storage.user_db import UserDB


class TestDeleteUserBookings:
    @pytest.fixture()
    def user_db_mock(self):
        return mock.create_autospec(UserDB)

    @pytest.fixture()
    def user_booking_db_mock(self):
        return mock.create_autospec(BookingDB)

    @pytest.fixture()
    def delete_user_bookings_response_mock(self):
        return mock.create_autospec(DeleteUserBookingsResponse)

    @pytest.fixture()
    def interactor(self, user_db_mock, user_booking_db_mock, delete_user_bookings_response_mock):
        return DeleteUserBookings(
            storage=user_booking_db_mock,
            user_db_storage=user_booking_db_mock,
            response=delete_user_bookings_response_mock
        )

    def test_invalid_booking_exception(self, interactor, user_db_mock, user_booking_db_mock,
                                       delete_user_bookings_response_mock):
        # Arrange
        booking_id = "95918a43-8f9d-4bad-9efa-0ca9dae7ec9e"
        user_booking_db_mock.delete_user_bookings_db.side_effect = InvalidBookingIDException
        expected_response = "Invalid Booking ID"
        delete_user_bookings_response_mock.invalid_booking_exception.return_value = expected_response
        #Act
        response = interactor.delete_user_bookings_interactor(booking_id)
        #Assert
        user_booking_db_mock.delete_user_bookings_db.assert_called_once_with(booking_id)
        delete_user_bookings_response_mock.invalid_booking_exception.assert_called_once()
        delete_user_bookings_response_mock.slot_delete_success_response.assert_not_called()

    def test_slot_delete_success_response(self, interactor, user_db_mock, user_booking_db_mock,
                                       delete_user_bookings_response_mock):
        # Arrange
        booking_id = "95918a43-8f9d-4bad-9efa-0ca9dae7ec9e"
        expected_response =  "Your slot has been deleted"
        delete_user_bookings_response_mock.slot_delete_success_response.return_value = expected_response
        # Act
        response = interactor.delete_user_bookings_interactor(booking_id)
        # Assert
        delete_user_bookings_response_mock.slot_delete_success_response.assert_called_once()

