import numpy as np
from typing import Optional, Tuple
from src.image_processing.interfaces import IFaceDetector, BoundingBox
from src.image_processing.config import ImageProcessingConfig

class SegmentationFaceDetector(IFaceDetector):
    """
    Implements the recommended MobileNet+U-Net or YOLO-seg segmentation approach 
    for sea turtle face detection as per the Research Agent's recommendations.
    """
    def __init__(self, config: ImageProcessingConfig, model_path: Optional[str] = None):
        self.config = config
        self.model_path = model_path if model_path is not None else self.config.default_model_path
        self._load_model()

    def _load_model(self):
        # If no model path is provided, we run in mock mode
        self.is_mock = self.model_path is None or self.model_path == ""

    def detect(self, image: np.ndarray) -> Tuple[Optional[BoundingBox], float, Optional[np.ndarray]]:
        """
        Detects the sea turtle face region in the provided image using YOLO-seg.
        Returns the bounding box, the confidence score, and the segmentation mask.
        """
        if self.is_mock:
            # Mock detection for testing purposes: returns a central bounding box
            h, w = image.shape[:2]
            cx, cy = w // 2, h // 2
            bw, bh = int(w * 0.4), int(h * 0.4)
            bbox = BoundingBox(
                x=max(0, cx - bw // 2),
                y=max(0, cy - bh // 2),
                w=bw,
                h=bh
            )
            # Create a mock mask
            mask = np.zeros((h, w), dtype=np.uint8)
            mask[bbox.y:bbox.y+bbox.h, bbox.x:bbox.x+bbox.w] = 1
            return bbox, 0.95, mask
        else:
            try:
                from ultralytics import YOLO
                import torch
            except ImportError:
                raise ImportError("ultralytics paketi yüklü değil. 'pip install ultralytics' çalıştırın.")

            if not hasattr(self, 'model'):
                self.model = YOLO(self.model_path)
            
            # Run inference with optimized parameters for underwater noise and small targets
            # imgsz=640 and agnostic_nms=True help with varying scales and overlapping detections
            results = self.model(
                image, 
                conf=0.1, # Sensitivity increased, we will filter by best confidence
                imgsz=640, 
                agnostic_nms=True,
                verbose=False
            )
            
            if not results or len(results) == 0 or len(results[0].boxes) == 0:
                return None, 0.0, None
                
            # Get the highest confidence detection (of any class, since we're specialized for turtles)
            # We filter for confidence >= threshold after we get the best one
            best_idx = torch.argmax(results[0].boxes.conf).item()
            confidence = results[0].boxes.conf[best_idx].item()
            
            if confidence < self.config.confidence_threshold:
                return None, confidence, None

            best_box = results[0].boxes[best_idx]
            
            # Parse bounding box
            x1, y1, x2, y2 = best_box.xyxy[0].cpu().numpy()
            bbox = BoundingBox(
                x=int(x1),
                y=int(y1),
                w=int(x2 - x1),
                h=int(y2 - y1)
            )
            
            # Get segmentation mask if available
            mask_np = None
            if results[0].masks is not None:
                mask_data = results[0].masks.data[best_idx].cpu().numpy()
                import cv2
                # Resize mask to original image size for pixel-perfect alignment
                mask_np = cv2.resize(mask_data, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LINEAR)
                mask_np = (mask_np > 0.5).astype(np.uint8)
            
            return bbox, confidence, mask_np
