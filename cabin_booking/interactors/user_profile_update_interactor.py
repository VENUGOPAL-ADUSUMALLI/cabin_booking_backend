from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidUsernameException, InvalidUserDetailsException
from cabin_booking.responses.user_profile_update_response import UserProfileUpdateResponse


class UserProfileUpdate:
    def __init__(self,storage:UserDB,response:UserProfileUpdateResponse):
        self.storage = storage
        self.response = response
    def update_user_profile_interactor(self,username,first_name,last_name,contact_number,team_name,email):
        try:
            self.storage.validate_user_email(email)
        except InvalidUsernameException:
            return self.response.invalid_email_exception()
        # try:
        #     self.storage.validate_user_first_name(first_name,last_name,contact_number)
        # except InvalidUserDetailsException:
        #     return self.response.invalid_user_details_exception()
        self.storage.update_user_profile(username,first_name, last_name, contact_number,team_name,email)
        return self.response.update_user_profile_success_response()



