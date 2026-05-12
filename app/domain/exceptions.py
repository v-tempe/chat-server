class DomainException(Exception):
    """Базовое исключение доменного слоя"""
    pass

class UserNotFoundError(DomainException):
    pass

class ChatNotFoundError(DomainException):
    pass

class EmptyMessageError(DomainException):
    pass

class MessageTooLongError(DomainException):
    pass

class UnauthorizedError(DomainException):
    pass
