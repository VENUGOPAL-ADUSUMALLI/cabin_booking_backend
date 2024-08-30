import logging
from collections import defaultdict
from os import access

from oauth2_provider.models import Application
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from django.utils import timezone
from datetime import timedelta
import uuid

from cabin_booking.databases.user_db import UserDB
from cabin_booking_backend.asgi import application

email = "venugopal@gamil.com"
user = UserDB.get_user_id(email)
app = Application.objects.create(
    name="cabin_booking",
    client_type=Application.CLIENT_CONFIDENTIAL,
    authrization_grant_type=Application.GRANT_PASSWORD,
    user= user
)
APP = Application.objects.get(name="cabin_booking")
expires = timezone.now()+ timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

access_token = AccessToken.objects.create(
    user = user,
    scope = 'read write',
    expires = expires,
    token = uuid.uuid4().hex,
    application = APP
)
refresh_token = RefreshToken.objects.create(
    user = user,
    token = uuid.uuid4().hex,
    application = APP,
    access_token= access_token
)