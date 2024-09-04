class InvalidUserException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class InvalidPasswordException(Exception):
    pass


class InvalidEmailException(Exception):
    pass

class UniqueConstraintException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
