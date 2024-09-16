from datetime import datetime
from typing import List
from django.utils import timezone
from cabin_booking.databases.cabin_db import CabinDB
from cabin_booking.databases.dtos import CabinTimeSlotsDTO, TimeSlotsDTO
from cabin_booking.databases.user_db import UserDB
from cabin_booking.exception import InvalidCabinIDException
from cabin_booking.models import BookingSlot, Cabin, Booking, CabinBooking, User
from cabin_booking.responses.cabin_confirm_slots_response import ConfirmSlotResponse


class BookingDB:
    def __init__(self, user_db_storage: UserDB):
        self.user_db_storage = user_db_storage

    @staticmethod
    def get_cabin_slots(cabin_ids, start_date, end_date) -> List[CabinTimeSlotsDTO]:
        # cabin_id = Cabin.objects.filter(id__in=cabin_ids)
        # if  cabin_id:
        #     raise InvalidCabinIDException()
        cabin_slots = BookingSlot.objects.filter(start_date_time__gte=start_date, end_date_time__lte=end_date,
                                                 cabin_booking__cabin_id__in=cabin_ids)
        cabin_id_wise_slots_dict = {}
        for each_cabin_slot in cabin_slots:
            cabin_id = each_cabin_slot.cabin_booking.cabin.id
            if cabin_id not in cabin_id_wise_slots_dict:
                cabin_id_wise_slots_dict[cabin_id] = CabinTimeSlotsDTO(
                    cabin_ids=cabin_id,
                    time_slots=[]
                )
            time_slots_dict = TimeSlotsDTO(
                slot=each_cabin_slot.start_date.time()
            )
            cabin_id_wise_slots_dict[cabin_id].time_slots.append(time_slots_dict)
        return list(cabin_id_wise_slots_dict.values())

    def create_cabin_slots(self, cabin_id, start_date, end_date, purpose, user_id):
        start_date = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d %H:%M"))
        end_date = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d %H:%M"))
        create_user_booking = Booking.objects.create(user_id=user_id, purpose=purpose)
        create_cabin_bookings = CabinBooking.objects.create(cabin_id=cabin_id, booking=create_user_booking)
        create_time_slot = BookingSlot.objects.create(start_date_time=start_date, end_date_time=end_date,
                                                      cabin_booking=create_cabin_bookings)

    @staticmethod
    def validate_cabin_id(cabin_id):
        try:
            Cabin.objects.get(id=cabin_id)
        except Cabin.DoesNotExist:
            raise InvalidCabinIDException()

    def validate_user_id(self, user_id):
        self.storage.validate_user_id(user_id)
