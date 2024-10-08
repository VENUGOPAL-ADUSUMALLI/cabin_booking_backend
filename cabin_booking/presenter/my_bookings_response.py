import json

from django.http import HttpResponse


class MyBookingsResponse:
    @staticmethod
    def invalid_user_exception() -> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Invalid User"
            },
            indent=4), status=400)

    @staticmethod
    def my_bookings_success_response(user_bookings_dto) -> HttpResponse:
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
        return HttpResponse(json.dumps(bookings_list, indent=4), status=200)

    @staticmethod
    def no_bookings_exception() -> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "No Bookings"
            },
            indent=4), status=400)
