import pickle
import face_recognition
import numpy as np

from backend.core.config import ENCODINGS_PATH
from backend.core.config import TOLERANCE


class FaceRecognitionService:

    def __init__(self):

        self.data = self.load_encodings()

    def load_encodings(self):

        print("[AI] Loading encodings...")

        with open(ENCODINGS_PATH, "rb") as file:

            data = pickle.load(file)

        print("[AI] Encodings loaded")

        return data

    def recognize_face(self, encoding):

        matches = face_recognition.compare_faces(
            self.data["encodings"],
            encoding,
            tolerance=TOLERANCE
        )

        distances = face_recognition.face_distance(
            self.data["encodings"],
            encoding
        )

        name = "Unknown"

        confidence = 0

        if len(distances) > 0:

            best_match = np.argmin(distances)

            confidence = round(
                (1 - distances[best_match]) * 100,
                2
            )

            if matches[best_match]:

                name = self.data["names"][best_match]

        return {
            "name": name,
            "confidence": confidence
        }