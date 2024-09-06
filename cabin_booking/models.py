from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.core.exceptions import ValidationError

from cabin_booking.constants.enums import CabinChoicesEnum


class CreateUpdateTimeDetails(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser,CreateUpdateTimeDetails):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    team_name = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)
    is_password_reset = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} from {self.team_name} team"


class Floor(CreateUpdateTimeDetails):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"


def Validate_cabin_type(cabin_type):
    if cabin_type not in CabinChoicesEnum.__members__:
        raise ValidationError("Please select valid cabins")


class Cabin(CreateUpdateTimeDetails):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, validators=[Validate_cabin_type],null=True,blank=True)
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.floor} {self.name} "


class Booking(CreateUpdateTimeDetails):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cabins = models.ManyToManyField(Cabin, through='CabinBooking')
    purpose = models.TextField()

    def __str__(self):
        return f"{self.user} Booked {self.cabins}"


class CabinBooking(CreateUpdateTimeDetails):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cabin', 'booking')


class BookingSlot(CreateUpdateTimeDetails):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    cabin_booking = models.ForeignKey(CabinBooking, on_delete=models.CASCADE)
