from datetime import time

from cabin_booking.constants.config import order_types
from cabin_booking.constants.time_slots_constant import SLOT_BOOKING_START_TIME, SLOT_BOOKING_END_TIME
from cabin_booking.databases.cabin_db import CabinDB
# from cabin_booking.databases.user_authentication_db import
from cabin_booking.exception import InvalidPasswordException, \
    InvalidEmailException, InvalidCabinIDException
from cabin_booking.models import *


def get_user_id():
    a = User.objects.get(email="yaswanthramreddy@gmail.com")
    print(a.__dict__)
    print(a.user_id)


def get_user(password):
    a = User.objects.get(email="xyz@gmail.com")
    b = a.check_password(password)
    print(b)


def create_user(email, password, first_name, last_name, username, team_name):
    user = User.objects.create(email=email, first_name=first_name, last_name=last_name,
                               team_name=team_name, username=username)
    user.set_password(password)
    user.save()
    return f"{user.username} , password ={user.password},email={user.email},first_name={user.first_name},last_name = {user.last_name}"


def check_password_for_user(email, password):
    user = User.objects.get(email=email)
    print(
        f"{user.username} , password ={user.password},email={user.email},first_name={user.first_name},last_name = {user.last_name}")
    return user.check_password(password)


# user_sign_up_password =pbkdf2_sha256$870000$nbGXpvVF8ltxsTeFwfEIix$kJfLGEtB6dQXaS0lmwmrhoNWb8AAqmB53w85yett2N0=
# user_login_password =pbkdf2_sha256$870000$nbGXpvVF8ltxsTeFwfEIix$kJfLGEtB6dQXaS0lmwmrhoNWb8AAqmB53w85yett2N0=
# upadated_password = pbkdf2_sha256$870000$HGLfi7pmXC206iOdy0Tw3j$2ll5XPkJLTFGoJsRJYGd1WalE5RL3ab5NeGfeqdMpCc
# password_after_updated_password = pbkdf2_sha256$870000$HGLfi7pmXC206iOdy0Tw3j$2ll5XPkJLTFGoJsRJYGd1WalE5RL3ab5NeGfeqdMpCc

def update_password_for_user(email, password, new_password):
    user_email_verification = User.objects.get(email=email)
    if not user_email_verification:
        raise InvalidEmailException()
    valid_password_for_user = user_email_verification.check_password(password)
    if not valid_password_for_user:
        raise InvalidPasswordException
    user_email_verification.set_password(new_password)
    user_email_verification.save()
    user_details = User.objects.get(email=email)
    return f"{user_details.username} , password ={user_details.password},email={user_details.email},first_name={user_details.first_name},last_name = {user_details.last_name}"


# def get_cabin_details():
#     cabin_details = Cabin.objects.all().select_related("floor").order_by('floor__order')
#     print(cabin_details)
#     floor_wise_cabins_list = []
#     floor_id_wise_cabins_list = defaultdict(list)
#     floor_id_wise_name = {}
#     cabins_list = []
#     for each_cabins in cabin_details:
#         cabin_dict = {
#             "cabin_id": str(each_cabins.id),
#             "name": each_cabins.name,
#             "description": each_cabins.description
#         }
#         cabins_list.append(cabin_dict)
#     print(json.dumps(cabins_list,indent=4))
# def get_floor_wise_cabins_list():
#     cabin_details = Cabin.objects.all().select_related("floor").order_by("floor__order")
#     floor_cabins_list = {}
#     cabins_list = []
#
#     for each in cabin_details:
#         floor_name = each.floor.name
#         if floor_name not in floor_cabins_list:
#             floor_cabins_list[floor_name]={
#                 "floor_name":floor_name,
#                 "cabins" : []
#             }
#
#         cabin_dict = {
#             "cabins_id": str(each.id),
#             "name": each.name,
#             "description": each.description
#         }
#         floor_cabins_list[floor_name]["cabins"].append(cabin_dict)
#     output = list(floor_cabins_list.values())
#
#
#
#     return json.dumps(output, indent=4)
def get_floor_wise_cabins_list():
    cabins = Cabin.objects.all().select_related("floor").order_by("floor__order")
    get_floor_wise_cabins_dict = {}
    for each in cabins:
        floor_name = each.floor.name
        if floor_name not in get_floor_wise_cabins_dict:
            get_floor_wise_cabins_dict[floor_name] = {
                "floor_name": floor_name,
                'cabins': []
            }
        cabin_dict = {
            "cabin_id": str(each.id),
            "cabin_name": each.name,
            "cabin_type": each.type,
            "description": each.description
        }
        get_floor_wise_cabins_dict[floor_name]["cabins"].append(cabin_dict)
    response = list(get_floor_wise_cabins_dict.values())
    return response


def get_floor_wise_cabins_list_utils():
    floor_wise_cabins_details_dto = CabinDB().get_cabins_details()
    for each_dto in floor_wise_cabins_details_dto:
        cabin_details_dto = each_dto.cabin
        sorted_cabin_details_dto = sorted(cabin_details_dto, key=lambda x: order_types.index(x.cabin_type))
        each_dto.cabin = sorted_cabin_details_dto
        # print(each_dto)


def get_cabin_details(cabin_id):
    cabins = Cabin.objects.filter(id=cabin_id).select_related("floor")
    for i in cabins:
        return f"name ={i.name},floor = {i.floor.name}"


fixed_time_slots = []
for each_hour in range(SLOT_BOOKING_START_TIME, SLOT_BOOKING_END_TIME):
    fixed_time_slots.append(time(each_hour, 0))


def get_cabin():
    cabin = Cabin.objects.get(id="a99183d9-52b4-443a-b30e-9b189702249f")
    print(cabin.name, cabin.floor)


def create_cabin_slots(cabin_id, start_date, end_date, purpose, user_id):
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
    create_user_booking = Booking.objects.create(user_id=user_id, purpose=purpose)
    create_cabin_bookings = CabinBooking.objects.create(cabin_id=cabin_id, booking=create_user_booking)
    create_time_slot = BookingSlot.objects.create(start_date_time=start_date, end_date_time=end_date,
                                                  cabin_booking=create_cabin_bookings)
    print(create_time_slot)


def user_details(cabin_id, start_date_time, end_date_time):
    cabin_slots = BookingSlot.objects.filter(start_date_time=start_date_time, end_date_time=end_date_time,
                                             cabin_booking__cabin_id=cabin_id)
    print(cabin_slots)
    for each in cabin_slots:
        print(each.cabin_booking.booking.user.first_name)
        print(each.cabin_booking.booking.purpose)
        print(each.start_date_time,each.end_date_time)



def validate_cabin_id_foe_cabin_slots(cabin_ids):
    all_cabins = []
    cabins = Cabin.objects.all()
    for each_cabin in cabins:
        all_cabins.append(str(each_cabin.id))
    for each_cabin in cabin_ids:
        if each_cabin not in all_cabins:
            raise InvalidCabinIDException()