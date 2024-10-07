from cabin_booking.presenter.signup_interactor_response import SignupInteractorResponse
from cabin_booking.storage.dtos import SignupResponseDTO


class TestUserSignUpInteractorResponse:
    def test_user_already_exists_response(self, snapshot):
        presenter = SignupInteractorResponse()
        response = presenter.user_already_exists_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_user_signup_dto_response(self, snapshot):
        user_signup_dto_from_db = SignupResponseDTO(
            access_token="e431bd6a2ca34e98b5e5aaa0cdb87bf8",
            refresh_token='e127c58f00c94daca06cb870d0eca3cc'
        )
        presenter = SignupInteractorResponse()
        response = presenter.user_signup_dto_response(user_signup_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')
