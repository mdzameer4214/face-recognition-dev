from ai_engine.engine import FaceRecognitionEngine

from backend.database.init_db import initialize_database


if __name__ == "__main__":

    initialize_database()

    engine = FaceRecognitionEngine()

    engine.process()