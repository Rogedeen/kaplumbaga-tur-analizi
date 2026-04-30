class FeatureExtractionError(Exception):
    """Base class for exceptions in feature extraction module."""
    pass

class ModelLoadError(FeatureExtractionError):
    """Exception raised when model fails to load."""
    pass

class ExtractionError(FeatureExtractionError):
    """Exception raised when feature extraction fails."""
    pass
