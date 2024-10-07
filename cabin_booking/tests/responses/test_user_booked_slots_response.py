from cabin_booking.presenter.user_booked_slots_response import UserBookedSlotResponse
from cabin_booking.storage.dtos import BookingProfileDTO


class TestUserBookedSlotsResponse:
    def test_invalid_cabin_id_response(self, snapshot):
        presenter = UserBookedSlotResponse()
        response = presenter.invalid_cabin_id_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_invalid_details_exception(self, snapshot):
        presenter = UserBookedSlotResponse()
        response = presenter.invalid_details_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_user_booked_slots_response(self, snapshot):
        user_details_dto_from_db = BookingProfileDTO(
            email="ggh@gmail.com",
            username="sahoorey",
            first_name="Kiran",
            last_name="chenna",
            team_name="air operations",
            contact_number="98255652615",
            purpose="Meeting"
        )
        presenter = UserBookedSlotResponse()
        response = presenter.user_booked_slots_response(user_details_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')
