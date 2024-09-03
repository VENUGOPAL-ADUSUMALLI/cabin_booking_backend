import json

from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from cabin_booking.databases.dtos import SignupResponseDTO, LoginResponseDTO, ProfileDTO
from cabin_booking.databases.user_db import UserDB
from cabin_booking.interactors.login_interactors import LoginInteractor
from cabin_booking.interactors.profile_interactor import ProfileInteractor
from cabin_booking.interactors.signup_interactor import SignupInteractor
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_login_interactor_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email:
        return HttpResponse({'error_code': "invalid_user",
                             "error_message": "Invalid email id (don't have an account please signup to continue)"},
                            status=400)

    if not password:
        return HttpResponse(
            {"error_code": "invalid_password", "error_message": "Invalid Password (please check your password)"},
            status=400)

    user_login_dto = LoginInteractor(storage=UserDB()).login_interactor(email, password)
    return HttpResponse(json.dumps(LoginResponseDTO(user_login_dto.access_token, user_login_dto.refresh_token)),
                        status=200)


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
    if not email:
        return HttpResponse(
            {"error_code": "user_already_exist", "error_message": "you have an account please login to continue"},
            status=400)
    user_signup_dto = SignupInteractor(storage=UserDB()).signup_interactor(email=email, password=password,
                                                                           username=username, first_name=first_name,
                                                                           last_name=last_name,
                                                                           contact_number=contact_number,
                                                                           team_name=team_name)
    return HttpResponse(json.dumps(SignupResponseDTO(user_signup_dto.access_token, user_signup_dto.refresh_token)),
                        status=200)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_user_profile_api_view(request):
    user_id = request.data.get('user_id')
    user_profile_dto = ProfileInteractor(storage=UserDB()).get_user_details_profile_interactor(user_id=user_id)
    return HttpResponse(json.dumps(ProfileDTO(user_profile_dto.user_id),status=200))



