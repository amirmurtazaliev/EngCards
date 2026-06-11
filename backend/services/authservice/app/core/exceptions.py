class DomainError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class UserAlreadyExistsError(DomainError):
    pass

class InvalidCredentialsError(DomainError):
    pass

class UserNotFoundError(DomainError):
    pass

class VerificationCodeError(DomainError):
    pass

class VerificationCodeExpiredError(VerificationCodeError):
    pass

class VerificationCodeInvalidError(VerificationCodeError):
    pass


class NotificationServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotificationServiceTimeoutError(NotificationServiceError):
    pass


class NotificationServiceUnavailableError(NotificationServiceError):
    pass