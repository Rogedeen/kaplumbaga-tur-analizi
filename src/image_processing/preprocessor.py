import cv2
import numpy as np
from src.image_processing.interfaces import IImagePreprocessor
from src.image_processing.config import ImageProcessingConfig
from src.image_processing.exceptions import InvalidImageError

class DefaultImagePreprocessor(IImagePreprocessor):
    def __init__(self, config: ImageProcessingConfig):
        self.config = config

    def validate(self, image: np.ndarray) -> bool:
        """
        Validates if the provided image is readable, has valid dimensions,
        and meets the minimum resolution requirements specified in the config.
        """
        if image is None or not isinstance(image, np.ndarray):
            raise InvalidImageError("Image is not a valid numpy array.")
        if len(image.shape) < 2:
            raise InvalidImageError("Image has invalid dimensions.")
        
        h, w = image.shape[:2]
        if h < self.config.min_height or w < self.config.min_width:
            raise InvalidImageError(f"Image resolution ({w}x{h}) is below minimum required ({self.config.min_width}x{self.config.min_height}).")
        
        return True

    def resize_for_detection(self, image: np.ndarray) -> np.ndarray:
        """
        Resizes the given image for the detection model while maintaining aspect ratio,
        ensuring its maximum dimension does not exceed the configured max_size.
        """
        h, w = image.shape[:2]
        max_dim = max(h, w)
        if max_dim > self.config.max_size:
            scale = self.config.max_size / max_dim
            new_w, new_h = int(w * scale), int(h * scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return image

    def normalize_for_model(self, image: np.ndarray) -> np.ndarray:
        """
        Resizes the cropped image to the target size and normalizes pixel values
        using the ImageNet mean and standard deviation from the configuration.
        """
        # Resize to target size for the model
        image = cv2.resize(image, self.config.target_size, interpolation=cv2.INTER_AREA)
        
        # Convert to float and scale to [0, 1]
        image_float = image.astype(np.float32) / 255.0
        
        # ImageNet mean and std for transfer learning normalization
        mean = np.array(self.config.imagenet_mean, dtype=np.float32)
        std = np.array(self.config.imagenet_std, dtype=np.float32)
        
        # If image is grayscale, convert to RGB-like 3 channels
        if len(image_float.shape) == 2:
            image_float = cv2.cvtColor(image_float, cv2.COLOR_GRAY2RGB)
            
        normalized = (image_float - mean) / std
        return normalized
