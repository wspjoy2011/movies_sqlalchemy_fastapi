class AccountsException(Exception):
    """Base exception for the accounts' application."""
    pass


class UserAlreadyExists(AccountsException):
    """Exception raised when a user with the given details already exists."""
    pass


class UserProfileAlreadyExists(AccountsException):
    """Exception raised when a user already has a profile."""

    def __init__(self, message="User already has profile"):
        self.message = message
        super().__init__(self.message)


class ActivationError(AccountsException):
    """Exception raised when account activation fails."""
    pass


class InvalidCredentialsError(AccountsException):
    """Exception raised when credentials are invalid."""

    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(AccountsException):
    """Exception raised when a token has expired."""

    def __init__(self, message="Token has expired"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(AccountsException):
    """Exception raised when a token is invalid."""

    def __init__(self, message="Invalid token"):
        self.message = message
        super().__init__(self.message)
