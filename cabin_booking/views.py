from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import HttpResponse


from cabin_booking.databases.user_db import UserDB
from cabin_booking.interactors.login_interactors import LoginInteractor
from cabin_booking.interactors.profile_interactor import ProfileInteractor
from cabin_booking.interactors.signup_interactor import SignupInteractor
from cabin_booking.interactors.update_password_interactor import UpdatePasswordInteractor
from cabin_booking.responses.update_password_response import UpdatePasswordResponse
from cabin_booking.responses.login_interactor_response import LoginInteractorResponse
from cabin_booking.responses.profile_interactor_response import ProfileInteractorResponse
from cabin_booking.responses.signup_interactor_response import SignupInteractorResponse


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_login_interactor_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    response = LoginInteractor(storage=UserDB(), response=LoginInteractorResponse()).login_interactor(email, password)
    return response


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def get_signup_interactor_view(request):
    email = request.data.get("email")
    password = request.data.get("Password")
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
    if not user_id:
        return HttpResponse({'error_code': "invalid_user", "error_message": "invalid User"})
    user_profile_dto = ProfileInteractor(storage=UserDB(),
                                         response=ProfileInteractorResponse()).get_user_details_profile_interactor(
        user_id=user_id)
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
