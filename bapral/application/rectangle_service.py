import cv2
import numpy as np

from bapral.domain.rectangle import RectangleDetector
from bapral.domain.template_match import TemplateMatcher


class RectangleService:
    def __init__(self, blur_depth=5, template_dir="templates"):
        self.detector = RectangleDetector(blur_depth)
        self.matcher = TemplateMatcher(template_dir=template_dir)
        
    def process_image(self, image_bytes):
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        rect = self.detector.detect_largest_rectangle(image)
        if rect:
            x1, y1, x2, y2 = rect
            region = image[y1:y2, x1:x2]
            
            h, w = region.shape[:2]
            r_image = region[:, (w//2):]
            l_image = region[:, :(w//2)]
            
            own_labels = self.matcher.match_templates(l_image)
            opp_labels = self.matcher.match_templates(r_image)
            
            return rect, own_labels, opp_labels
        else:
            None, [], []