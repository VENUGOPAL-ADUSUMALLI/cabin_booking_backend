import json

from django.http import HttpResponse


class MyBookingsResponse:
    @staticmethod
    def my_bookings_success_response(user_bookings_dto):
        bookings_list = []
        for each in user_bookings_dto:
            time_slots = []
            for each_time_slot in each.time_slots:
                time_slots.append(each_time_slot.strftime("%H:%M"))
            user_bookings = {
                "Floor_name": each.floor_name,
                "cabin_name": each.cabin_name,
                "Booking_id": str(each.booking_id),
                "start_date": each.start_date.strftime("%Y-%m-%d"),
                "end_date": each.end_date.strftime("%Y-%m-%d"),
                "time_slots": time_slots
            }
            bookings_list.append(user_bookings)
        return HttpResponse(json.dumps(bookings_list,indent=4), status=200)
