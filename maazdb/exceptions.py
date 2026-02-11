class MaazDBError(Exception):
    """Base class for all MaazDB exceptions."""
    pass

class ConnectionError(MaazDBError):
    """Raised when connection to server fails."""
    pass

class AuthError(MaazDBError):
    """Raised when authentication fails."""
    pass

class ProtocolError(MaazDBError):
    """Raised when the server sends unexpected data."""
    pass