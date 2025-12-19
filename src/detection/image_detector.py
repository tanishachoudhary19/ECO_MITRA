from ultralytics import YOLO
import os

class ImageDetector:
    def __init__(self, model_path='models/yolov8n.pt'):
        """
        Initializes the YOLOv8 model.
        Args:
            model_path (str): Path to the YOLO model weights.
        """
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            raise RuntimeError(f"Error loading YOLO model from {model_path}: {e}")

    def detect(self, image_path, conf=0.5):
        """
        Detects objects in the provided image.

        Args:
            image_path (str): The path to the image file.
            conf (float): Confidence threshold for detection.

        Returns:
            list: A list of detected object names (unique).
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image {image_path} not found!")

            results = self.model.predict(source=image_path, conf=conf)
            if not results:
                return []

            detected_items = []
            for r in results:
                class_names = self.model.names
                for c in r.boxes.cls:
                    detected_items.append(class_names[int(c)])

            return list(set(detected_items))  # Remove duplicates
        except Exception as e:
            raise RuntimeError(f"Error detecting objects in {image_path}: {e}")


# Example usage (for testing this module alone)
if __name__ == "__main__":
    detector = ImageDetector()
    test_img = "data/images/test_image.jpg"
    try:
        detected_objects = detector.detect(test_img)
        print("Detected objects:", detected_objects)
    except Exception as e:
        print("Detection failed:", e)
