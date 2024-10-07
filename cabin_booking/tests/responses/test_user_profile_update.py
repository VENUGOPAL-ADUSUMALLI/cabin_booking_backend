from cabin_booking.presenter.user_profile_update_response import UserProfileUpdateResponse


class TestUserProfileUpdate:
    def test_invalid_user_exception(self, snapshot):
        presenter = UserProfileUpdateResponse()
        response = presenter.invalid_user_exception()
        snapshot.assert_match(response.content, 'response.json')

    def test_update_user_profile_success_response(self, snapshot):
        presenter = UserProfileUpdateResponse()
        response = presenter.update_user_profile_success_response()
        snapshot.assert_match(response.content, 'response.json')
