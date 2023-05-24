"""exceptions"""


class ServiceError(BaseException):...

class UserDoesNotExisted(ServiceError):...

class UserAlreadyExisted(ServiceError):...

class PileDoesNotExisted(ServiceError):...

class IllegalUpdateAttemption(ServiceError):...

class OutOfRecycleResource(ServiceError):...

class OutOfSpace(ServiceError):...

class AlreadyRequested(ServiceError):...

class MappingNotExisted(ServiceError):...