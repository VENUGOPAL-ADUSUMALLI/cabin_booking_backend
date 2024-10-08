import json

from django.http import HttpResponse


class DeleteUserBookingsResponse:
    @staticmethod
    def invalid_booking_exception()-> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": "400",
                "error_message": "Invalid Booking ID"
            }
            , indent=4), status=400)

    @staticmethod
    def slot_delete_success_response()-> HttpResponse:
        return HttpResponse(json.dumps(
            {
                "error_code": "200",
                "error_message": "Your slot has been deleted"
            }
            , indent=4), status=200)
