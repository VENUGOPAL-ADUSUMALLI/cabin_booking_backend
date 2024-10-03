import uuid

import pytest

from cabin_booking.models import User
from cabin_booking.storage.user_db import UserDB


@pytest.mark.django_db
class TestUpdateUserProfile:
    def test_update_user_profile(self):
        user_id = str(uuid.uuid4())
        user_name = "Venu Gopal"
        first_name = "Apple"
        last_name = "iphone"
        team_name = "Sales"
        contact_number = "9666910497"
        user = User.objects.create(
            user_id=user_id,
            username=user_name,
            first_name=first_name,
            last_name=last_name,
            team_name=team_name,
            contact_number=contact_number
        )
        new_user_name = "Apple India"
        new_first_name = "iphone"
        new_last_name = "Apple"
        new_team_name = 'innovation'
        new_contact_number = "9441844128"
        storage = UserDB()
        update_rows = storage.update_user_profile(user_id=user_id, first_name=new_first_name, username=new_user_name,
                                                  last_name=new_last_name, team_name=new_team_name,
                                                  contact_number=new_contact_number)
        assert update_rows == 1
        response = User.objects.get(user_id=user_id)
        assert response.username == new_user_name
        assert response.first_name == new_first_name
        assert response.last_name == new_last_name
        assert response.team_name == new_team_name
        assert response.contact_number == new_contact_number
