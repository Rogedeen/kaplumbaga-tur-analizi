import cv2
import numpy as np
from typing import Union
from src.image_processing.interfaces import IImagePreprocessor, IFaceDetector, DetectionResult, BoundingBox
from src.image_processing.config import ImageProcessingConfig
from src.image_processing.exceptions import DetectionError, InvalidImageError

class ImageProcessingPipeline:
    def __init__(self, preprocessor: IImagePreprocessor, detector: IFaceDetector, config: ImageProcessingConfig):
        self.preprocessor = preprocessor
        self.detector = detector
        self.config = config

    def process_image(self, image_path: str) -> DetectionResult:
        """
        Görüntü yolunu alarak tam bir tespit (detection) boru hattı işletir.
        Görüntüyü yükler, doğrular, yüz tespiti yapar, yüzü kırpar (padding ile) 
        ve sonraki ajanlar için modeli normalize eder.
        
        Args:
            image_path (str): İşlenecek görüntünün dosya yolu.
            
        Returns:
            DetectionResult: Tespit sonucu, kırpılmış/normalize edilmiş görüntü ve güven skoru.
        """
        try:
            # 1. Ön Doğrulama (Load and validate)
            image = cv2.imread(image_path)
            if image is None:
                return DetectionResult(
                    success=False, bbox=None, confidence=0.0, cropped_image=None,
                    error_message=f"Could not read image from {image_path}"
                )
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.preprocessor.validate(image)
            
            # 2. Yeniden Boyutlandırma (Resize for detection)
            detection_image = self.preprocessor.resize_for_detection(image)
            
            # 3. Yüz/Baş Tespiti (Detection)
            bbox, confidence, mask = self.detector.detect(detection_image)
            
            if bbox is None or confidence < self.config.confidence_threshold:
                return DetectionResult(
                    success=False, bbox=None, confidence=confidence, cropped_image=None,
                    error_message=f"Face detection failed or confidence ({confidence:.2f}) below threshold ({self.config.confidence_threshold:.2f})."
                )
                
            # Need to map bbox back to original image scale if we resized
            # But the requirement says "resize for detection, crop, pad, then normalize".
            # For simplicity, if we resized, we can just crop from the resized image,
            # or we map the bbox back. Let's map it back to original for best quality.
            h_orig, w_orig = image.shape[:2]
            h_det, w_det = detection_image.shape[:2]
            scale_x = w_orig / w_det
            scale_y = h_orig / h_det
            
            orig_bbox = BoundingBox(
                x=int(bbox.x * scale_x),
                y=int(bbox.y * scale_y),
                w=int(bbox.w * scale_x),
                h=int(bbox.h * scale_y)
            )
            
            # Arka planı filtrele (Segmentation Maskesi)
            if mask is not None:
                mask_orig = cv2.resize(mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)
                image_to_crop = np.zeros_like(image)
                for c in range(3):
                    image_to_crop[:, :, c] = image[:, :, c] * mask_orig
            else:
                image_to_crop = image
            
            # 4. Kırpma + Padding
            cropped_image = self._crop_with_padding(image_to_crop, orig_bbox, self.config.padding_percent)
            
            # 5. Normalizasyon
            normalized_image = self.preprocessor.normalize_for_model(cropped_image)
            
            return DetectionResult(
                success=True,
                bbox=orig_bbox,
                confidence=confidence,
                cropped_image=normalized_image,
                error_message=None
            )
            
        except InvalidImageError as e:
            return DetectionResult(
                success=False, bbox=None, confidence=0.0, cropped_image=None,
                error_message=str(e)
            )
        except Exception as e:
            return DetectionResult(
                success=False, bbox=None, confidence=0.0, cropped_image=None,
                error_message=f"Unexpected error: {str(e)}"
            )

    def _crop_with_padding(self, image: np.ndarray, bbox: BoundingBox, padding_percent: float) -> np.ndarray:
        h_img, w_img = image.shape[:2]
        
        pad_w = int(bbox.w * padding_percent)
        pad_h = int(bbox.h * padding_percent)
        
        x1 = max(0, bbox.x - pad_w)
        y1 = max(0, bbox.y - pad_h)
        x2 = min(w_img, bbox.x + bbox.w + pad_w)
        y2 = min(h_img, bbox.y + bbox.h + pad_h)
        
        return image[y1:y2, x1:x2].copy()
