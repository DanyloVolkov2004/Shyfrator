class InvalidCipherException(Exception):
    pass
class ShortPasswordException(Exception):
    pass
class IdenticalSourceException(Exception):
    pass
class InvalidHeaderSignException(Exception):
    pass
class InvalidHeaderInfoException(Exception):
    pass
class AuthenticationFailException(Exception):
    pass