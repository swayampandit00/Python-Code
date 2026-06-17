import cv2
import os
import numpy as np

# ----------------------------
# Step 1: Get person name
# ----------------------------
person_name = input("Enter Person Name: ")

dataset_path = "./dataset"
person_folder = os.path.join(dataset_path, person_name)
model_folder = "./models"

# auto create folders
os.makedirs(person_folder, exist_ok=True)
os.makedirs(model_folder, exist_ok=True)

# ----------------------------
# Step 2: Load face detector
# ----------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ----------------------------
# Step 3: Capture live photos
# ----------------------------
cap = cv2.VideoCapture(0)

count = 0
max_photos = 50

print("Camera Started...")
print("Look at camera. Collecting face images...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        # face crop
        face_img = gray[y:y+h, x:x+w]

        # save image
        file_name = os.path.join(person_folder, f"{count}.jpg")
        cv2.imwrite(file_name, face_img)

        count += 1

        cv2.rectangle(frame,
                      (x, y),
                      (x+w, y+h),
                      (0,255,0),
                      2)

        cv2.putText(frame,
                    f"Captured: {count}",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)

    cv2.imshow("Collecting Face Data", frame)

    if count >= max_photos:
        break

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Face collection complete")

# ----------------------------
# Step 4: Train Model
# ----------------------------
faces_data = []
labels = []
people = []

# scan dataset folders
all_people = os.listdir(dataset_path)

for label, person in enumerate(all_people):

    people.append(person)

    path = os.path.join(dataset_path, person)

    for img_name in os.listdir(path):

        img_path = os.path.join(path, img_name)

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        faces_data.append(img)
        labels.append(label)

# create recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# train
recognizer.train(
    faces_data,
    np.array(labels)
)

# save model
model_path = os.path.join(model_folder, "face_model.yml")
recognizer.save(model_path)

# save label mapping
with open("./models/labels.txt", "w") as f:
    for i, name in enumerate(people):
        f.write(f"{i}:{name}\n")

print("Model Training Complete")
print("Created -> models/face_model.yml")
print("Created -> models/labels.txt")