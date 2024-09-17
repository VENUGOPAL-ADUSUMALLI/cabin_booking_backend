from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class UserDTO:
    token: str


@dataclass
class LoginResponseDTO:
    access_token: str
    refresh_token: str


@dataclass
class SignupResponseDTO:
    access_token: str
    refresh_token: str


@dataclass
class ProfileDTO:
    email: str
    username: str
    first_name: str
    last_name: str
    team_name: str
    contact_number: str
    purpose: str = ""


@dataclass
class UserPasswordUpdateDTO:
    user_id: str


@dataclass
class CabinDetailsDTO:
    cabin_id: str
    name: str
    cabin_type: str
    description: str


@dataclass
class FloorWiseCabinDetailsDTO:
    floor: str
    cabin: list[CabinDetailsDTO]

@dataclass
class AvailabilityDTO:
    availability: bool


@dataclass
class CabinTimeSlotsDTO:
    cabin_id: str
    time_slots: List[datetime.time]