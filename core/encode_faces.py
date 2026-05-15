import face_recognition
import os
import pickle

DATASET_PATH = "dataset"

known_encodings = []
known_names = []

print("[INFO] Loading faces...")

for person_name in os.listdir(DATASET_PATH):

    person_path = os.path.join(
        DATASET_PATH,
        person_name
    )

    if not os.path.isdir(person_path):
        continue

    for image_name in os.listdir(person_path):

        image_path = os.path.join(
            person_path,
            image_name
        )

        print(f"[INFO] Processing {image_path}")

        try:

            image = face_recognition.load_image_file(
                image_path
            )

            face_locations = face_recognition.face_locations(
                image
            )

            # ONLY ACCEPT IMAGES WITH EXACTLY ONE FACE
            if len(face_locations) != 1:

                print(
                    f"[SKIPPED] {image_name} "
                    f"contains {len(face_locations)} faces"
                )

                continue

            face_encoding = face_recognition.face_encodings(
                image,
                face_locations
            )[0]

            known_encodings.append(face_encoding)

            known_names.append(
                person_name.capitalize()
            )

        except Exception as e:

            print(f"[ERROR] {image_path}")
            print(e)

os.makedirs(
    "encodings",
    exist_ok=True
)

with open(
    "encodings/face_encodings.pkl",
    "wb"
) as file:

    pickle.dump(
        {
            "encodings": known_encodings,
            "names": known_names
        },
        file
    )

print("[INFO] Encoding Complete")
print("[INFO] Encodings saved successfully")
