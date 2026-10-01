import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io

def preprocess_image(image: Image.Image) -> Image.Image:
    """Enhance image quality for better AI analysis."""
    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize if too large (keep aspect ratio)
    max_size = 1024
    w, h = image.size
    if w > max_size or h > max_size:
        ratio = min(max_size / w, max_size / h)
        image = image.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    # Mild enhancement
    image = ImageEnhance.Contrast(image).enhance(1.1)
    image = ImageEnhance.Sharpness(image).enhance(1.2)
    image = ImageEnhance.Brightness(image).enhance(1.05)

    return image

def detect_face_opencv(image: Image.Image):
    """Use OpenCV to detect and crop face region."""
    img_array = np.array(image)
    gray      = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))

    if len(faces) == 0:
        return None, image  # no face found, return original

    # Take largest face
    x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]

    # Add padding around face
    pad    = int(max(w, h) * 0.3)
    x1     = max(0, x - pad)
    y1     = max(0, y - pad)
    x2     = min(img_array.shape[1], x + w + pad)
    y2     = min(img_array.shape[0], y + h + pad)

    face_crop = Image.fromarray(img_array[y1:y2, x1:x2])
    return (x, y, w, h), face_crop

def draw_face_box(image: Image.Image, face_coords):
    """Draw bounding box on detected face for display."""
    if face_coords is None:
        return image

    img_array = np.array(image.copy())
    x, y, w, h = face_coords

    # Draw purple box
    cv2.rectangle(img_array, (x, y), (x + w, y + h), (147, 51, 234), 3)

    # Label
    cv2.putText(img_array, "Face Detected", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (147, 51, 234), 2)

    return Image.fromarray(img_array)

def get_dominant_colors(image: Image.Image, n_colors: int = 5):
    """Extract dominant colors from image using k-means."""
    img_array = np.array(image.resize((150, 150))).reshape(-1, 3)
    img_array = img_array.astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(img_array, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = centers.astype(int)
    counts  = np.bincount(labels.flatten())
    sorted_colors = [centers[i] for i in np.argsort(counts)[::-1]]

    return [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in sorted_colors]
