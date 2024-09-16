from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User
admin.site.register(User)
from .models import Cabin, User

admin.site.register(Cabin)
from .models import Booking

admin.site.register(Booking)
from .models import Floor

admin.site.register(Floor)
from .models import CabinBooking

admin.site.register(CabinBooking)
from .models import BookingSlot

admin.site.register(BookingSlot)

#
# class UserAdmin(UserAdmin):
#     list_display = ['username', 'user_id', 'is_staff', 'is_superuser',
#                     'is_active', 'date_joined', 'first_name', "last_name"]
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email',
#                                       'contact_number',)}),
#         ('Permissions', {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     search_fields = ["user_id__exact", "phone_number__exact"]
#     list_per_page = 25
#
#
# admin.site.register(User, UserAdmin)
