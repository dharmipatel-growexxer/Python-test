class InvalidInputException(Exception):
    """Raised when input is invalid (e.g., mobile, amount, password)"""
    pass

class InsufficientBalanceException(Exception):
    """Raised when withdrawal amount exceeds balance"""
    pass    

class InvalidLoginException(Exception):
    """Raised when login credentials are invalid"""
    pass