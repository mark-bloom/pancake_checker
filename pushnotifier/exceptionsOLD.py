# define Python user-defined exceptions
class MalformedRequestError(BaseException):
    "the request is malformed, i.e. missing content"
    pass

class DeviceNotFoundError(BaseException):
    "a device couldn't be found"
    pass
    
class UserNotFoundError(BaseException):
    "user couldn't be found (incorrect username/password)"
    pass
    
class IncorrectCredentialsError(BaseException):
    "credentials are incorrect"
    pass

class UnauthorizedError(BaseException):
    "package name or api key is incorrect"
    pass
    
class PayloadTooLargeError(BaseException):
    "your image is too big (> 5 MB)"
    pass
    
class UnsupportedMediaTypeError(BaseException):
    "you passed an invalid file type or the device(s) you tried to send this image to can\'t receive images)"
    pass
    
class UnknownError(BaseException):
    "an unknown error occured! please contact the author of this module!"
    pass