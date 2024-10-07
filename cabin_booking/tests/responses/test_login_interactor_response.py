from cabin_booking.presenter.login_interactor_response import LoginInteractorResponse
from cabin_booking.storage.dtos import LoginResponseDTO


class TestLoginInteractorResponse:
    def test_invalid_user_response(self, snapshot):
        presenter = LoginInteractorResponse()
        response = presenter.invalid_user_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_invalid_password_exception_response(self, snapshot):
        presenter = LoginInteractorResponse()
        response = presenter.invalid_password_exception_response()
        snapshot.assert_match(response.content, 'response.json')

    def test_user_login_dto_response(self, snapshot):
        expected_dto_from_db = LoginResponseDTO(
            access_token='40d64f9fabc8443cb6792c1cf98dfa59',
            refresh_token='625cd56d495f44658036722ff53a07c0'
        )
        presenter = LoginInteractorResponse()
        response = presenter.user_login_dto_response(expected_dto_from_db)
        snapshot.assert_match(response.content, 'response.json')
