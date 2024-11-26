class UserAlreadyExists(Exception):
    pass


class UserProfileAlreadyExists(Exception):
    def __init__(self, message="User already has profile"):
        self.message = message
        super().__init__(self.message)


class ActivationError(Exception):
    pass


class InvalidCredentialsError(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(Exception):
    def __init__(self, message="Token has expired"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(Exception):
    def __init__(self, message="Invalid token"):
        self.message = message
        super().__init__(self.message)

