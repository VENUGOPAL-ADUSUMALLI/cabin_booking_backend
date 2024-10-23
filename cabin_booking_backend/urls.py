"""
URL configuration for cabin_booking_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from cabin_booking.views import get_login_interactor_view, get_signup_interactor_view, get_user_profile_api_view, \
    get_update_password_view, get_cabin_details_view, get_cabin_wise_slots_view, get_cabin_confirm_slot_view, \
    get_user_booked_slots_view, update_user_profile_view, get_user_my_bookings_view, refresh_access_token_view, \
    user_logout_view, delete_user_bookings_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_account/login/v1', get_login_interactor_view),
    path('user_account/signup/v1', get_signup_interactor_view),
    path('user/profile/v1', get_user_profile_api_view),
    path("user_accounts/update_password/v1", get_update_password_view),
    path('get/cabin_details/v1', get_cabin_details_view),
    path('get/cabin_slots/v1', get_cabin_wise_slots_view),
    path('confirm_slots/v1', get_cabin_confirm_slot_view),
    path('user/booked_slots/v1', get_user_booked_slots_view),
    path('user/profile_update/v1', update_user_profile_view),
    path("user/my_bookings/v1", get_user_my_bookings_view),
    path('user_account/logout/v1', user_logout_view),
    path('user_account/refresh_access_tokens/v1', refresh_access_token_view),
    path('delete/user/bookings/v1', delete_user_bookings_view)
]
