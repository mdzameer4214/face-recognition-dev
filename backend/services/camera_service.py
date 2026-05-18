import cv2

from backend.core.config import CAMERA_ID


class CameraService:

    def __init__(self):

        self.camera = cv2.VideoCapture(CAMERA_ID)

    def read_frame(self):

        return self.camera.read()

    def release(self):

        self.camera.release()