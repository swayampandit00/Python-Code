import cv2

# ----------------------------
# Load Face Detector
# ----------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ----------------------------
# Load Trained Model
# ----------------------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./models/face_model.yml")

print("Model Loaded")

# ----------------------------
# Load Labels (ID -> Name)
# models/labels.txt example:
# 0:Rahul
# 1:Aman
# ----------------------------
people = {}

with open("./models/labels.txt", "r") as f:
    for line in f.readlines():
        label, name = line.strip().split(":")
        people[int(label)] = name

print("Labels Loaded")

# ----------------------------
# Start Webcam
# ----------------------------
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    # detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        1.3,
        5
    )

    for (x, y, w, h) in faces:

        # face region
        face_roi = gray[y:y+h, x:x+w]

        # predict person
        label, confidence = recognizer.predict(
            face_roi
        )

        # confidence check
        # lower = better match
        if confidence < 80:
            name = people[label]
        else:
            name = "Unknown"

        # draw box
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0,255,0),
            2
        )

        # show name
        cv2.putText(
            frame,
            f"{name} ({int(confidence)})",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    # show webcam
    cv2.imshow(
        "Live Face Recognition",
        frame
    )

    # press q to exit
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()