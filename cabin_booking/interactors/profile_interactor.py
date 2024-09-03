from cabin_booking.databases.dtos import ProfileDTO
from cabin_booking.databases.user_db import UserDB


class ProfileInteractor:
    def __init__(self, storage: UserDB):
        self.storage = storage

    def get_user_details_profile_interactor(self, user_id):
        user_details = self.storage.profile(user_id)
        user_dto = ProfileDTO(
            email=user_details.email,
            password=user_details.password,
            first_name=user_details.first_name,
            last_name=user_details.last_name,
            username= user_details.username,
            team_name= user_details.team_name,
            contact_number=user_details.contact_number
        )
        return user_dto
