import cv2


class RectangleDetector:
    """矩形領域を検出するクラス.
    """
    def __init__(self, blur_depth=5):
        self.blur_depth = blur_depth
    
    def _preprocess(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (self.blur_depth, self.blur_depth), 0)
        
        return blurred
    
    def detect_rectangle_contours(self, image, th_min=50, th_max=150):
        edged = cv2.Canny(self._preprocess(image), th_min, th_max)
        contours, _ = cv2.findContours(
            edged,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        
        return contours
    
    def detect_largest_rectangle(self, image, th_min=50, th_max=150):
        max_area = 0
        max_rect = None

        for cnt in self.detect_rectangle_contours(image, th_min, th_max):
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            if area > max_area:
                max_area = area
                max_rect = (x, y, x+w, y+h)
                
        return max_rect
    