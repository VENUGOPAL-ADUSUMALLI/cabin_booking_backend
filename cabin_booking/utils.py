from datetime import time

from cabin_booking.constants.config import order_types
from cabin_booking.constants.time_slots_constant import SLOT_BOOKING_START_TIME, SLOT_BOOKING_END_TIME
from cabin_booking.storage.cabin_db import CabinDB
# from cabin_booking.storage.user_authentication_db import
from cabin_booking.exception import InvalidPasswordException, \
    InvalidEmailException, InvalidCabinIDException, InvalidUserException
from cabin_booking.models import *
from django.contrib.auth.hashers import make_password


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
        print(each.start_date_time, each.end_date_time)


def validate_cabin_id_foe_cabin_slots(cabin_ids):
    all_cabins = []
    cabins = Cabin.objects.all()
    for each_cabin in cabins:
        all_cabins.append(str(each_cabin.id))
    for each_cabin in cabin_ids:
        if each_cabin not in all_cabins:
            raise InvalidCabinIDException()


def validate_cabins(user_id):
    booking_id = []
    user_booking_details = Booking.objects.filter(user_id=user_id).prefetch_related("cabins__floor")
    for each in user_booking_details:
        for cabin in each.cabins.all():
            print(cabin.floor.name)
            print(cabin.name)
            booking_id.append(each.id)
    print(booking_id)
    booking_time_details = BookingSlot.objects.filter(cabin_booking__booking_id__in=booking_id)
    for each in booking_time_details:
        print(each.start_date_time)
        print(each.end_date_time)
        # print(each.cabins.floor.name)
        # print(each.cabins.name)


# dc927863-3890-422e-b8d6-038a1e0eab00
def create_user_for_signup(email, password, user_name, first_name, last_name, team_name, contact_number):
    hashed_password = make_password(password)
    create_user_signup = User.objects.create(email=email, password=hashed_password, first_name=first_name,
                                             last_name=last_name, team_name=team_name, contact_number=contact_number,
                                             username=user_name)
    print(create_user_signup)


# def update_password(email,old_password,new_password):
def check_password(email, password):
    get_user_obj = User.objects.get(email=email)
    if not get_user:
        raise InvalidUserException()
    check_user_password = get_user_obj.check_password(password)
    return check_user_password


def update_password(email, old_password, new_password):
    user = User.objects.get(email=email)
    validate_old_password = check_password(email, old_password)
    if validate_old_password:
        new_password = make_password(new_password)
        user.password = new_password
        user.save()
        print("password updated successfully")
# This is the expected final response in dictionary format
        final_response = [
            {
                "cabin_id": "b2ff1c68-5009-4d20-9103-01db46d76342",
                "time_slots": [
                    {"slot": "09:00:00", "availability": True},
                    {"slot": "10:00:00", "availability": True},
                    {"slot": "11:00:00", "availability": True},
                    {"slot": "12:00:00", "availability": True},
                    {"slot": "13:00:00", "availability": True},
                    {"slot": "14:00:00", "availability": True},
                    {"slot": "15:00:00", "availability": True},
                    {"slot": "16:00:00", "availability": True},
                    {"slot": "17:00:00", "availability": True},
                    {"slot": "18:00:00", "availability": False},
                    {"slot": "19:00:00", "availability": True},
                    {"slot": "20:00:00", "availability": False},
                    {"slot": "21:00:00", "availability": True},
                    {"slot": "22:00:00", "availability": True},
                    {"slot": "23:00:00", "availability": True},
                ]
            }
        ]

        cabin_id_available_dtos = [
            CabinTimeSlotsAvailabilityDTO(
                cabin_id='b2ff1c68-5009-4d20-9103-01db46d76342',
                time_slots=[
                    TimeSlotsDTO(slot=time(9, 0), availability=True),
                    TimeSlotsDTO(slot=time(10, 0), availability=True),
                    TimeSlotsDTO(slot=time(11, 0), availability=True),
                    TimeSlotsDTO(slot=time(12, 0), availability=True),
                    TimeSlotsDTO(slot=time(13, 0), availability=True),
                    TimeSlotsDTO(slot=time(14, 0), availability=True),
                    TimeSlotsDTO(slot=time(15, 0), availability=True),
                    TimeSlotsDTO(slot=time(16, 0), availability=True),
                    TimeSlotsDTO(slot=time(17, 0), availability=True),
                    TimeSlotsDTO(slot=time(18, 0), availability=False),
                    TimeSlotsDTO(slot=time(19, 0), availability=True),
                    TimeSlotsDTO(slot=time(20, 0), availability=False),
                    TimeSlotsDTO(slot=time(21, 0), availability=True),
                    TimeSlotsDTO(slot=time(22, 0), availability=True),
                    TimeSlotsDTO(slot=time(23, 0), availability=True),
                ]
            )
        ]

        # Mock the database response and response handler
        booking_db_mock.get_cabin_slots.return_value = cabin_id_available_dtos
        cabin_slots_response_mock.get_cabin_slot_details_success_response.return_value = final_response

        # Act
        response = interactor.get_cabin_slots_interactor(cabin_ids, start_date, end_date)

        # Assert
        booking_db_mock.get_cabin_slots.assert_called_once_with(cabin_ids, start_date, end_date)
        cabin_slots_response_mock.get_cabin_slot_details_success_response.assert_called_once_with(
            cabin_id_available_dtos)
        assert response == final_response  # Now comparing two dictionaries