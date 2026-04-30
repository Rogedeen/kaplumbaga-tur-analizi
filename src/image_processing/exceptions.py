class DetectionError(Exception):
    """Exception raised when face detection fails."""
    pass

class InvalidImageError(Exception):
    """Exception raised when the input image is invalid or unreadable."""
    pass
