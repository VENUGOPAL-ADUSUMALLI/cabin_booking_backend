# from datetime import time
#
#
# def get_fixed_times_slots():
#     time_slots = []
#     for each_hours in (9, 12):
#         time_slots.append(time(each_hours, 0))
#     for each_hours in (12, 24):
#         time_slots.append(time(each_hours, 0))
#     for slots in time_slots:
#         return slots.strftime("%I,%M %P")
#
SLOT_BOOKING_START_TIME = 9
SLOT_BOOKING_END_TIME = 24