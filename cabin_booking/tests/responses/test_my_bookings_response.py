from datetime import date, time

from cabin_booking.presenter.my_bookings_response import MyBookingsResponse
from cabin_booking.storage.dtos import UserBookingDetailsDTO


class TestMyBookingsResponse:
    def test_invalid_user_exception(self, snapshot):
        presenter = MyBookingsResponse()
        response = presenter.invalid_user_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_no_bookings_exception(self, snapshot):
        presenter = MyBookingsResponse()
        response = presenter.no_bookings_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_my_bookings_success_response(self, snapshot):
        booking_db_dto_from_db = [UserBookingDetailsDTO(
            floor_name='Fourth Floor',
            cabin_name='Call pod 3b',
            booking_id='215e37da-b01c-4fae-b262-faa986984056',
            start_date=date(2024, 9, 23),
            end_date=date(2024, 9, 25),
            time_slots=[
                time(11, 0),
                time(13, 0)
            ]
        )
        ]
        presenter = MyBookingsResponse()
        response = presenter.my_bookings_success_response(booking_db_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')
