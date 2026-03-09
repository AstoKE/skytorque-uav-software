import cv2
import numpy as np


class TargetDetector:
    def __init__(self, min_area=500):
        self.min_area = min_area

        self.lower_red_1 = np.array([0, 120, 70])
        self.upper_red_1 = np.array([10, 255, 255])

        self.lower_red_2 = np.array([170, 120, 70])
        self.upper_red_2 = np.array([180, 255, 255])

    def detect(self, frame):
        if frame is None:
            return None

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, self.lower_red_1, self.upper_red_1)
        mask2 = cv2.inRange(hsv, self.lower_red_2, self.upper_red_2)
        mask = cv2.bitwise_or(mask1, mask2)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area < self.min_area:
            return None

        x, y, w, h = cv2.boundingRect(largest)
        cx = x + w / 2
        cy = y + h / 2

        frame_h, frame_w = frame.shape[:2]
        err_x = cx - (frame_w / 2)
        err_y = cy - (frame_h / 2)

        return {
            "cx": cx,
            "cy": cy,
            "area": area,
            "bbox": (x, y, w, h),
            "error_x": err_x,
            "error_y": err_y,
            "frame_width": frame_w,
            "frame_height": frame_h,
            "mask": mask,
        }