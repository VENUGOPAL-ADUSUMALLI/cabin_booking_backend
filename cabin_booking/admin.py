from django.contrib import admin


# Register your models here.
from .models import User
admin.site.register(User)
from .models import Cabin
admin.site.register(Cabin)
from .models import Booking
admin.site.register(Booking)
from .models import Floor
admin.site.register(Floor)
from .models import CabinBooking
admin.site.register(CabinBooking)
from .models import BookingSlot
admin.site.register(BookingSlot)