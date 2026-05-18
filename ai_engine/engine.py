import cv2
import face_recognition

from datetime import datetime

from backend.core.config import FRAME_RESIZE
from backend.core.config import ATTENDANCE_DELAY

from backend.services.camera_service import CameraService
from backend.services.face_service import FaceRecognitionService
from backend.services.attendance_service import AttendanceService


class FaceRecognitionEngine:

    def __init__(self):

        self.camera_service = CameraService()

        self.face_service = FaceRecognitionService()

        self.attendance_service = AttendanceService()

        self.last_seen = {}

    def process(self):

        print("[SYSTEM] Face Recognition Engine Started")

        while True:

            ret, frame = self.camera_service.read_frame()

            if not ret:
                break

            small_frame = cv2.resize(
                frame,
                (0, 0),
                fx=FRAME_RESIZE,
                fy=FRAME_RESIZE
            )

            rgb_small = cv2.cvtColor(
                small_frame,
                cv2.COLOR_BGR2RGB
            )

            boxes = face_recognition.face_locations(
                rgb_small
            )

            encodings = face_recognition.face_encodings(
                rgb_small,
                boxes
            )

            for encoding, box in zip(encodings, boxes):

                result = self.face_service.recognize_face(
                    encoding
                )

                name = result["name"]

                confidence = result["confidence"]

                color = (0, 255, 0)

                if name != "Unknown":

                    if name not in self.last_seen:

                        self.attendance_service.mark_attendance(
                            name
                        )

                        self.last_seen[name] = datetime.now()

                    else:

                        seconds = (
                            datetime.now() -
                            self.last_seen[name]
                        ).seconds

                        if seconds > ATTENDANCE_DELAY:

                            self.attendance_service.mark_attendance(
                                name
                            )

                            self.last_seen[name] = datetime.now()

                else:

                    color = (0, 0, 255)

                top, right, bottom, left = box

                scale = int(1 / FRAME_RESIZE)

                top *= scale
                right *= scale
                bottom *= scale
                left *= scale

                label = f"{name} ({confidence}%)"

                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    color,
                    2
                )

                cv2.rectangle(
                    frame,
                    (left, bottom - 35),
                    (right, bottom),
                    color,
                    cv2.FILLED
                )

                cv2.putText(
                    frame,
                    label,
                    (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

            cv2.imshow(
                "Enterprise Face Recognition System",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.camera_service.release()

        cv2.destroyAllWindows()