from dataclasses import dataclass


@dataclass
class UserDTO:
    token: str


@dataclass
class LoginResponseDTO:
    access_token: str
    refresh_token: str

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        }


@dataclass
class SignupResponseDTO:
    access_token: str
    refresh_token: str
    def to_dict(self):
        return {
            "access_token" : self.access_token,
            "refresh_token" : self.refresh_token
        }


@dataclass
class ProfileDTO:
    email: str
    password: str
    username: str
    first_name: str
    last_name: str
    team_name: str
    contact_number: str

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'team_name': self.team_name,
            "contact_number": self.contact_number

        }
