class NumericError(Exception):
    """
    A class for generating an error if converting a string to a number
     does not support the type [int, float].
    """
    def __init__(self, message = None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class OperationError(ValueError):
    """
    A class for generating an error if the operator value is incorrect.
    """
    def __init__(self, message = None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)