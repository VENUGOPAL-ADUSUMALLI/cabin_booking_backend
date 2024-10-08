from datetime import datetime
from typing import List

from django.db.models import Q

from cabin_booking.exception import InvalidCabinIDException, NoBookingsException, InvalidDateRangeException, \
    InvalidBookingIDException
from cabin_booking.models import BookingSlot, Cabin, Booking, CabinBooking
from cabin_booking.storage.dtos import CabinTimeSlotsDTO, UserBookingDetailsDTO, BookingProfileDTO
from cabin_booking.storage.user_db import UserDB


class BookingDB:
    def __init__(self, user_db_storage: UserDB):
        self.user_db_storage = user_db_storage

    @staticmethod
    def get_cabin_slots(cabin_ids, start_date, end_date) -> List[CabinTimeSlotsDTO]:
        cabin_slots = BookingSlot.objects.filter(start_date_time__date__gte=start_date,
                                                 start_date_time__date__lte=end_date,
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
    def validate_start_and_end_dates(start_date, end_date) -> None:
        if start_date > end_date:
            raise InvalidDateRangeException()

    @staticmethod
    def create_cabin_slots(cabin_id, purpose, user_id, list_start_end_date_time_dto) -> None:

        create_user_booking = Booking.objects.create(user_id=user_id, purpose=purpose)
        create_cabin_bookings = CabinBooking.objects.create(cabin_id=cabin_id, booking=create_user_booking)
        for dto in list_start_end_date_time_dto:
            BookingSlot.objects.create(start_date_time=dto.start_date_time,
                                       end_date_time=dto.end_date_time,
                                       cabin_booking=create_cabin_bookings)

    @staticmethod
    def validate_cabin_id_for_cabin_slots(cabin_ids) -> None:
        all_cabins = []
        cabins = Cabin.objects.all()
        for each_cabin in cabins:
            all_cabins.append(str(each_cabin.id))
        for each_cabin in cabin_ids:
            if each_cabin not in all_cabins:
                raise InvalidCabinIDException()

    @staticmethod
    def validate_cabin_id(cabin_id) -> None:
        try:
            Cabin.objects.get(id=cabin_id)
        except Cabin.DoesNotExist:
            raise InvalidCabinIDException()

    @staticmethod
    def check_user_already_booked_slots(cabin_id, convert_start_date, convert_end_date, converted_time_slots) -> bool:
        check_slots = BookingSlot.objects.filter(start_date_time__date__gte=convert_start_date,
                                                 end_date_time__date__lte=convert_end_date,
                                                 start_date_time__time__in=converted_time_slots,
                                                 cabin_booking__cabin_id=cabin_id)
        return check_slots.exists()

    @staticmethod
    def get_user_booked_slot(cabin_id, start_date_time, end_date_time) -> BookingProfileDTO:
        start_date_time = datetime.strptime(start_date_time, "%Y-%m-%d %H:%M")
        end_date_time = datetime.strptime(end_date_time, "%Y-%m-%d %H:%M")
        cabin_slot_details = BookingSlot.objects.filter(
            Q(start_date_time=start_date_time) | Q(end_date_time=end_date_time),
            cabin_booking__cabin_id=cabin_id)
        for each_details in cabin_slot_details:
            user_details_dto = BookingProfileDTO(
                email=each_details.cabin_booking.booking.user.email,
                first_name=each_details.cabin_booking.booking.user.first_name,
                last_name=each_details.cabin_booking.booking.user.last_name,
                username=each_details.cabin_booking.booking.user.username,
                team_name=each_details.cabin_booking.booking.user.team_name,
                contact_number=each_details.cabin_booking.booking.user.contact_number,
                purpose=each_details.cabin_booking.booking.purpose
            )
            return user_details_dto

    @staticmethod
    def get_user_bookings(user_id) -> List[UserBookingDetailsDTO]:
        bookings_details_dto = []
        user_booking_details = Booking.objects.filter(user_id=user_id).prefetch_related(
            "cabinbooking_set__bookingslot_set", "cabinbooking_set__cabin__floor"
        )
        if not user_booking_details.exists():
            raise NoBookingsException()
        for booking in user_booking_details:
            for cabin_booking in booking.cabinbooking_set.all():
                time_slots = set()
                start_date_list = []
                end_date_list = []
                for booking_slot in cabin_booking.bookingslot_set.all():
                    start_date_list.append(booking_slot.start_date_time.date())
                    end_date_list.append(booking_slot.end_date_time.date())
                    time_slots.add(booking_slot.start_date_time.time())
                unique_time_slots = sorted(set(time_slots))
                if not start_date_list:
                    raise NoBookingsException()
                cabin_details_dto = UserBookingDetailsDTO(
                    floor_name=cabin_booking.cabin.floor.name,
                    cabin_name=cabin_booking.cabin.name,
                    booking_id=booking.id,
                    start_date=start_date_list[0],
                    end_date=end_date_list[-1],
                    time_slots=unique_time_slots
                )
                bookings_details_dto.append(cabin_details_dto)

        return bookings_details_dto

    @staticmethod
    def delete_user_bookings_db(booking_id) -> None:
        try:
            booking_obj = Booking.objects.get(id=booking_id)
            booking_obj.delete()
        except Booking.DoesNotExist:
            raise InvalidBookingIDException()
