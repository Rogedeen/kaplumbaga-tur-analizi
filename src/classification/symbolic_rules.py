import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional, Callable

class SymbolicFeatureExtractor:
    """
    Hierarchical Elimination Engine (Dichotomous Key Architecture).
    Implements a modular, lazy-evaluation structure where features are analyzed on-demand.
    """
    
    def __init__(self):
        # HSV Color Ranges (H: 0-180, S: 0-255, V: 0-255)
        self.color_ranges = {
            "red": [
                (np.array([0, 150, 50]), np.array([10, 255, 255])),
                (np.array([160, 150, 50]), np.array([180, 255, 255]))
            ],
            "yellow": (np.array([22, 100, 100]), np.array([35, 255, 255])),
            "orange": (np.array([10, 150, 100]), np.array([22, 255, 255])),
        }
        
        # Feature registry for on-demand calls
        self._feature_methods: Dict[str, Callable[[np.ndarray], float]] = {
            "red_stripe": lambda img: self._get_color_score(img, "red"),
            "yellow_pattern": lambda img: self._get_color_score(img, "yellow"),
            "beak_sharpness": self._calculate_beak_sharpness,
            "texture_complexity": self._calculate_texture_complexity,
            "parallel_lines": self._calculate_parallel_lines,
            "head_width_ratio": self._calculate_head_width_ratio # Added for Level 3A
        }

    def analyze(self, feature_name: str, face_image: np.ndarray) -> float:
        """
        Performs a specific analysis based on the feature name requested.
        Lazy evaluation: only the required logic runs.
        """
        if face_image is None or face_image.size == 0:
            return 0.0

        # Ensure image is in correct format (uint8, 3 channels)
        face_image = self._ensure_uint8(face_image)
        if len(face_image.shape) == 2:
            face_image = cv2.cvtColor(face_image, cv2.COLOR_GRAY2BGR)

        method = self._feature_methods.get(feature_name)
        if not method:
            raise ValueError(f"Feature '{feature_name}' is not registered in the engine.")

        return method(face_image)

    def _ensure_uint8(self, image: np.ndarray) -> np.ndarray:
        """Ensures the image is 8-bit unsigned integer."""
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        return image

    def _get_color_score(self, image: np.ndarray, color_name: str) -> float:
        """Calculates the ratio of pixels matching a color range, normalized."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        if color_name == "red":
            mask1 = cv2.inRange(hsv, self.color_ranges["red"][0][0], self.color_ranges["red"][0][1])
            mask2 = cv2.inRange(hsv, self.color_ranges["red"][1][0], self.color_ranges["red"][1][1])
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower, upper = self.color_ranges[color_name]
            mask = cv2.inRange(hsv, lower, upper)
            
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        pixel_count = np.sum(mask > 0)
        total_pixels = image.shape[0] * image.shape[1]
        
        score = (pixel_count / total_pixels) / 0.05
        return float(np.clip(score, 0.0, 1.0))

    def _calculate_beak_sharpness(self, image: np.ndarray) -> float:
        """Estimates the pointiness of the front profile."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return 0.0
            
        cnt = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(cnt)
        
        area = cv2.contourArea(cnt)
        hull_area = cv2.contourArea(hull)
        
        if hull_area == 0: return 0.0
        
        solidity = area / hull_area
        score = 1.0 - solidity
        return float(np.clip(score * 2, 0.0, 1.0))

    def _calculate_texture_complexity(self, image: np.ndarray) -> float:
        """Measures edge density as a proxy for spot/scale complexity."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / (image.shape[0] * image.shape[1])
        return float(np.clip(edge_density * 10, 0.0, 1.0))

    def _calculate_parallel_lines(self, image: np.ndarray) -> float:
        """Detects parallel lines using Hough Line Transform."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 50)
        
        if lines is None:
            return 0.0
            
        angles = []
        for line in lines:
            rho, theta = line[0]
            angles.append(theta)
            
        if not angles:
            return 0.0
            
        hist, _ = np.histogram(angles, bins=18, range=(0, np.pi))
        max_parallel = np.max(hist)
        
        score = max_parallel / 5.0
        return float(np.clip(score, 0.0, 1.0))

    def _calculate_head_width_ratio(self, image: np.ndarray) -> float:
        """
        Calculates the ratio of head width to image height.
        Useful for Level 3A (Massive Head) identification like Caretta caretta.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0.0
            
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        
        # In a cropped face image, a very wide bounding box relative to height indicates a massive head.
        ratio = w / h
        # Typical turtle head ratio is 1.0-1.2. Caretta caretta is higher.
        score = (ratio - 0.8) / 0.7
        return float(np.clip(score, 0.0, 1.0))
