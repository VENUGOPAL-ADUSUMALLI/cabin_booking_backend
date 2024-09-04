import json

from django.http import HttpResponse

from cabin_booking.databases.dtos import ProfileDTO
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidUserException
from cabin_booking.responses.profile_interactor_response import ProfileInteractorResponse


class ProfileInteractor:
    def __init__(self, storage: UserDB,response:ProfileInteractorResponse):
        self.storage = storage
        self.response = response

    def get_user_details_profile_interactor(self, user_id):
        try:
            user_details = self.storage.profile(user_id)
            if not user_details:
                raise InvalidUserException()
        except InvalidUserException:
            self.response.invalid_user_response()
        user_dto = ProfileDTO(
            email=user_details.email,
            password=user_details.password,
            first_name=user_details.first_name,
            last_name=user_details.last_name,
            username= user_details.username,
            team_name= user_details.team_name,
            contact_number=user_details.contact_number
        )
        user_details_response = ProfileInteractorResponse().user_details_dto_response(user_dto)
        return user_details_response
