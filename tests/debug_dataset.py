import cv2
import face_recognition
import os

dataset = "dataset"

total = 0
failed = 0

for person in os.listdir(dataset):
    folder = os.path.join(dataset, person)

    for img in os.listdir(folder):
        path = os.path.join(folder, img)

        image = cv2.imread(path)
        if image is None:
            print("❌ unreadable:", path)
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)

        if len(faces) == 0:
            print("❌ NO FACE:", path)
            failed += 1
        else:
            print("✅ OK:", path)
            total += 1

print("\nTOTAL OK:", total)
print("FAILED:", failed)
