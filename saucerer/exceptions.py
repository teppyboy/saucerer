class SaucererError(Exception):
    """Base class for all Saucerer exceptions"""

    pass


class UploadError(SaucererError):
    """Base class for all upload error"""

    pass


class ParseError(SaucererError):
    """Base class for all web parsing error"""

    pass
