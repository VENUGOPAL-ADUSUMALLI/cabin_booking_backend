import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class TimeSlotsDTO:
    slot: datetime.time
    availability: bool


@dataclass
class CabinTimeSlotsAvailabilityDTO:
    cabin_id: str
    time_slots: List[TimeSlotsDTO]
@dataclass
class StartEndDateTimeDTO:
    start_date_time : datetime
    end_date_time : datetime
