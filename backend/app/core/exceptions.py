from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    """Raised when login credentials are invalid"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InactiveUserException(HTTPException):
    """Raised when user account is deactivated"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated. Please contact support.",
        )


class NotFoundException(HTTPException):
    """Raised when a resource is not found"""
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )


class AlreadyExistsException(HTTPException):
    """Raised when trying to create a duplicate resource"""
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists",
        )


class UnauthorizedException(HTTPException):
    """Raised when user doesn't have permission"""
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )