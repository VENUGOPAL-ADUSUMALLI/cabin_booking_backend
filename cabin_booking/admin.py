from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import *


class UserModelDisplay(UserAdmin):
    list_display = ['username', 'user_id', "email"
        , 'first_name', "last_name", "team_name"]
    search_fields = ["user_id", "email"]
    list_per_page = 25


class FloorModelDisplay(admin.ModelAdmin):
    list_display = ["id", "order", "name"]
    search_fields = ["id", "name"]
    list_per_page = 25


class CabinModelDisplay(admin.ModelAdmin):
    list_display = ["id", "floor__id", "name", "description", "type"]
    search_fields = ["id", "name"]
    list_per_page = 25


class BookingModelDisplay(admin.ModelAdmin):
    list_display = ["id", "user", "purpose","created_time"]
    search_fields = ["id", "user__id"]
    list_per_page = 25


class CabinBookingModelDisplay(admin.ModelAdmin):
    list_display = ["id", "cabin", "booking__id"]
    search_fields = ["id", "cabin", "booking__id"]
    list_per_page = 25


class BookingSlotModelDisplay(admin.ModelAdmin):
    list_display = ["id", "start_date_time", "end_date_time", "cabin_booking__id"]
    search_fields = ["id", "start_date_time", "end_date_time","cabin_booking__id"]


admin.site.register(User, UserModelDisplay)
admin.site.register(Floor, FloorModelDisplay)
admin.site.register(Cabin, CabinModelDisplay)
admin.site.register(Booking, BookingModelDisplay)
admin.site.register(CabinBooking, CabinBookingModelDisplay)
admin.site.register(BookingSlot, BookingSlotModelDisplay)
