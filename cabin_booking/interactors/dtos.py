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
