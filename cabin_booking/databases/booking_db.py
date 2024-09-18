from datetime import datetime, timedelta
from typing import List

from django.db import transaction
from django.utils import timezone

from cabin_booking.databases.dtos import CabinTimeSlotsDTO, ProfileDTO
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidCabinIDException, UniqueConstraintException
from cabin_booking.models import BookingSlot, Cabin, Booking, CabinBooking


class BookingDB:
    def __init__(self, user_db_storage: UserDB):
        self.user_db_storage = user_db_storage

    @staticmethod
    def get_cabin_slots(cabin_ids, start_date, end_date) -> List[CabinTimeSlotsDTO]:
        cabin_slots = BookingSlot.objects.filter(start_date_time__gte=start_date, end_date_time__lte=end_date,
                                                 cabin_booking__cabin_id__in=cabin_ids)

        cabin_id_wise_slots_dict = {}
        for each_cabin_slot in cabin_slots:
            cabin_id = each_cabin_slot.cabin_booking.cabin.id
            if cabin_id not in cabin_id_wise_slots_dict:
                cabin_id_wise_slots_dict[cabin_id] = CabinTimeSlotsDTO(
                    cabin_id=cabin_id,
                    time_slots=[]
                )
            cabin_id_wise_slots_dict[cabin_id].time_slots.append(each_cabin_slot.start_date_time.time())
        return list(cabin_id_wise_slots_dict.values())

    @staticmethod
    def create_cabin_slots(cabin_id,purpose, user_id,list_start_end_date_time_dto):
        try:
            with transaction.atomic():
                create_user_booking = Booking.objects.create(user_id=user_id, purpose=purpose)
                create_cabin_bookings = CabinBooking.objects.create(cabin_id=cabin_id, booking=create_user_booking)
                for dto in list_start_end_date_time_dto:
                    BookingSlot.objects.create(start_date_time=dto.start_date_time,
                                                                      end_date_time=dto.end_date_time,
                                                                      cabin_booking=create_cabin_bookings)
        except Exception as e:
            raise UniqueConstraintException(e)

    @staticmethod
    def validate_cabin_id_for_cabin_slots(cabin_ids):
        all_cabins = []
        cabins = Cabin.objects.all()
        for each_cabin in cabins:
            all_cabins.append(str(each_cabin.id))
        for each_cabin in cabin_ids:
            if each_cabin not in all_cabins:
                raise InvalidCabinIDException()

    @staticmethod
    def validate_cabin_id(cabin_id):
        try:
            Cabin.objects.get(id=cabin_id)
        except Cabin.DoesNotExist:
            raise InvalidCabinIDException()

    def validate_user_id(self, user_id):
        self.storage.validate_user_id(user_id)

    @staticmethod
    def get_user_booked_slot(cabin_id, start_date_time, end_date_time):
        start_date_time = timezone.make_aware(datetime.strptime(start_date_time, "%Y-%m-%d %H:%M"))
        end_date_time = timezone.make_aware(datetime.strptime(end_date_time, "%Y-%m-%d %H:%M"))
        cabin_slot_details = BookingSlot.objects.filter(start_date_time=start_date_time, end_date_time=end_date_time,
                                                        cabin_booking__cabin_id=cabin_id)
        user_slot_details = []
        for each_details in cabin_slot_details:
            user_details_dto = ProfileDTO(
                email=each_details.cabin_booking.booking.user.email,
                first_name=each_details.cabin_booking.booking.user.first_name,
                last_name=each_details.cabin_booking.booking.user.last_name,
                username=each_details.cabin_booking.booking.user.username,
                team_name=each_details.cabin_booking.booking.user.team_name,
                contact_number=each_details.cabin_booking.booking.user.contact_number,
                purpose=each_details.cabin_booking.booking.purpose
            )
            user_slot_details.append(user_details_dto)
        return user_slot_details
