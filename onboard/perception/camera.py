import cv2


class Camera:
    def __init__(self, device=0, width=640, height=480):
        self.cap = cv2.VideoCapture(device)

        if not self.cap.isOpened():
            raise RuntimeError(f"Kamera açılamadı. device={device}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()