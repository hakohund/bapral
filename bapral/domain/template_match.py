import os

import numpy as np
import cv2
from PIL import Image


class TemplateMatcher:
    """テンプレートマッチングを行うクラス.
    """
    
    def __init__(self, template_dir):
        self.templates = []
        self.labels = []
        
        for filename in os.listdir(template_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img = np.array(
                    Image.open(os.path.join(template_dir, filename)),
                    dtype=np.uint8,
                )
                template = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                label = os.path.splitext(filename)[0]
                
                self.templates.append(template)
                self.labels.append(label)
                
    def match_templates(self, region, threshold=0.8):
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        matches = []
        
        for template, label in zip(self.templates, self.labels):
            res = cv2.matchTemplate(
                gray,
                template,
                cv2.TM_CCOEFF_NORMED,
            )
            loc = np.where(res >= threshold)
            w, h = template.shape[::-1]
            
            for pt in zip(*loc[::-1]):
                matches.append((pt[0], pt[1], pt[0]+w, pt[1]+h, label))
                
        seen = set()
        filtered = []
        for m in matches:
            if m[0] not in seen:
                do_append = True
                for s in seen:
                    if abs(s-m[0]) < 10:
                        do_append = False
                if do_append:
                    filtered.append(m)
                    seen.add(m[0])
                
        filtered.sort(key=lambda x: x[0])
        return [m[4] for m in filtered]