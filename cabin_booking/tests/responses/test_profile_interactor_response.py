from cabin_booking.presenter.profile_interactor_response import ProfileInteractorResponse
from cabin_booking.storage.dtos import ProfileDTO


class TestProfileInteractorResponse:
    def test_invalid_user_response(self, snapshot):
        presenter = ProfileInteractorResponse()
        response = presenter.invalid_user_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_user_details_dto_response(self, snapshot):
        user_dto_from_db = ProfileDTO(
            email="iphone@gamil.com",
            username='null',
            first_name="Apple",
            last_name="iphone",
            team_name="Sales",
            contact_number="9666910497"
        )
        presenter = ProfileInteractorResponse()
        response = presenter.user_details_dto_response(user_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')
