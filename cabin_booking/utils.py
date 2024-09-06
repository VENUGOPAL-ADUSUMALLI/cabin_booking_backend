import logging
from collections import defaultdict
from dataclasses import dataclass

from oauth2_provider.models import Application

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

# from cabin_booking.databases.user_authentication_db import
from cabin_booking.exception import InvalidUserException, UserAlreadyExistsException, InvalidPasswordException, \
    InvalidEmailException
from cabin_booking.models import *
from django.conf import settings






def get_user_id():
    a = User.objects.all().count()
    print(a)
    # print(a.user_id)
    # a.set_password(password)
    # a.save()
    # print(a.check_password(password))


def get_cabin_details():
    cabin_details = Cabin.objects.all().select_related("floor").order_by('floor__order')
    print(cabin_details)
    floor_wise_cabins_list = []
    floor_id_wise_cabins_list = defaultdict(list)
    floor_id_wise_name = {}
    for each_cabins in cabin_details:
        cabin_dict = {
            "cabin_id": str(each_cabins.id),
            "name": each_cabins.name,
            "description": each_cabins.description
        }
        floor_id_wise_cabins_list[str(each_cabins.floor_id)].append(cabin_dict)
        floor_id_wise_name[str(each_cabins.floor_id)] = each_cabins.floor_name

    for floor_id, cabin_list in floor_id_wise_cabins_list:
        cabin_dict = {
            "floor": floor_id_wise_name[floor_id],
            'cabins': cabin_list
        }
        floor_wise_cabins_list.append(cabin_dict)
    return floor_wise_cabins_list
