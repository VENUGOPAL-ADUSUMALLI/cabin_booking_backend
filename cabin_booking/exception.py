class InvalidUserException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class InvalidPasswordException(Exception):
    pass


class InvalidEmailException(Exception):
    pass


class UniqueConstraintException(Exception):
    pass


class SomethingWentWrongException(Exception):
    pass


class InvalidCabinIDException(Exception):
    pass


class InvalidUsernameException(Exception):
    pass


class InvalidUserDetailsException(Exception):
    pass


class NoBookingsException(Exception):
    pass


class InvalidRefreshTokenException(Exception):
    pass


class RefreshTokenExpiredException(Exception):
    pass


class InvalidAccessTokenException(Exception):
    pass


class InvalidDateRangeException(Exception):
    pass


class InvalidDetailsException(Exception):
    pass


class InvalidBookingIDException(Exception):
    pass
