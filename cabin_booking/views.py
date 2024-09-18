from http.client import responses

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse

from cabin_booking.databases.booking_db import BookingDB
from cabin_booking.databases.cabin_db import CabinDB
from cabin_booking.databases.user_authentication_db import UserAuthentication
from cabin_booking.databases.user_db import UserDB
from cabin_booking.interactors.cabin_confirm_slots_interactor import ConfirmSlotInteractor
from cabin_booking.interactors.cabins_details_interactor import CabinDetailsInteractor
from cabin_booking.interactors.get_cabin_wise_slots_interactor import CabinWiseSlotsInteractor
from cabin_booking.interactors.login_interactors import LoginInteractor
from cabin_booking.interactors.profile_interactor import ProfileInteractor
from cabin_booking.interactors.signup_interactor import SignupInteractor
from cabin_booking.interactors.update_password_interactor import UpdatePasswordInteractor
from cabin_booking.interactors.user_booked_slots_interactor import UserBookedSlotsInteractor
from cabin_booking.interactors.user_profile_update_interactor import UserProfileUpdate
from cabin_booking.responses.cabin_confirm_slots_response import ConfirmSlotResponse
from cabin_booking.responses.cabin_details_response import CabinDetailsResponse
from cabin_booking.responses.get_cabins_slots_response import CabinSlotsDetailsResponse
from cabin_booking.responses.update_password_response import UpdatePasswordResponse
from cabin_booking.responses.login_interactor_response import LoginInteractorResponse
from cabin_booking.responses.profile_interactor_response import ProfileInteractorResponse
from cabin_booking.responses.signup_interactor_response import SignupInteractorResponse
from cabin_booking.responses.user_booked_slots_response import UserBookedSlotResponse
from cabin_booking.responses.user_profile_update_response import UserProfileUpdateResponse


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_login_interactor_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    response = LoginInteractor(storage=UserDB(), response=LoginInteractorResponse(),
                               authentication=UserAuthentication()).login_interactor(email, password)
    return response


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_signup_interactor_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    contact_number = request.data.get("contact_number")
    team_name = request.data.get("team_name")

    response = SignupInteractor(storage=UserDB(), response=SignupInteractorResponse()).signup_interactor(
        email=email, password=password,
        username=username, first_name=first_name,
        last_name=last_name,
        contact_number=contact_number,
        team_name=team_name
    )
    return response


@api_view(['GET'])
def get_user_profile_api_view(request):
    user_id = request.data.get('user_id')
    user_profile_dto = ProfileInteractor(storage=UserDB(),
                                         response=ProfileInteractorResponse()).get_user_details_profile_interactor(
        user_id=str(user_id))
    return user_profile_dto


@api_view(['POST'])
def get_update_password_view(request):
    email = request.data.get("email")
    password = request.data.get('password')
    new_password = request.data.get('new_password')
    response = UpdatePasswordInteractor(storage=UserDB(),
                                        response=UpdatePasswordResponse()).update_password_interactor(email=email,
                                                                                                      password=password,
                                                                                                      new_password=new_password)
    return response


@api_view(['GET'])
def get_cabin_details_view(request):
    response = CabinDetailsInteractor(storage=CabinDB(), response=CabinDetailsResponse()).get_floor_wise_cabins_list()
    return response


@api_view(["GET"])
def get_cabin_wise_slots_view(request):
    """
            {
          "cabin_ids": [
            "string"
          ],
          "start_date": "2024-09-12",
          "end_date": "2024-09-12"
        }
    """
    cabin_ids = request.data.get('cabin_ids')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    response = CabinWiseSlotsInteractor(storage=BookingDB(user_db_storage=UserDB()),
                                        response=CabinSlotsDetailsResponse()).get_cabin_slots_interactor(
        cabin_ids=cabin_ids, start_date=start_date,
        end_date=end_date)
    return response


@api_view(["POST"])
def get_cabin_confirm_slot_view(request):
    cabin_id = request.data.get('cabin_id')
    time_slots = request.data.get('time_slots')
    user_id = request.user.user_id
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    purpose = request.data.get('purpose')
    response = ConfirmSlotInteractor(storage=BookingDB(user_db_storage=UserDB()), user_db_storage=UserDB(),
                                     response=ConfirmSlotResponse()).confirm_slot_interactor(
        cabin_id=cabin_id,
        start_date=start_date,
        end_date=end_date, purpose=purpose,
        user_id=user_id, time_slots=time_slots)
    return response


@api_view(["GET"])
def get_user_booked_slots_view(request):
    cabin_id = request.data.get('cabin_id')
    start_date_time = request.data.get('start_date_time')
    end_date_time = request.data.get('end_date_time')
    response = UserBookedSlotsInteractor(storage=BookingDB(user_db_storage=UserDB()),
                                         response=UserBookedSlotResponse()).user_booked_slot(
        cabin_id=cabin_id, start_date_time=start_date_time, end_date_time=end_date_time)
    return response


@api_view(['GET'])
def update_user_profile_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    first_name = request.data.get('firstname')
    last_name = request.data.get('lastname')
    team_name = request.data.get('team_name')
    contact_number = request.data.get('contact_number')
    response = UserProfileUpdate(storage=UserDB(), response=UserProfileUpdateResponse()).update_user_profile_interactor(
        username=username,
        first_name=first_name,
        last_name=last_name, team_name=team_name,
        contact_number=contact_number, email=email)
    return response
