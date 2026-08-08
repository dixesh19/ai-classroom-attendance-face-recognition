from pathlib import Path
import cv2
import numpy as np
from django.conf import settings
from .models import Student

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def load_image_from_uploaded_file(uploaded_file):
    data = uploaded_file.read()
    array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not read the image.")
    return image

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cascade = cv2.CascadeClassifier(CASCADE_PATH)
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
    )
    return gray, faces

def create_recognizer():
    if not hasattr(cv2, "face"):
        raise RuntimeError(
            "OpenCV face module is missing. Install opencv-contrib-python "
            "and remove opencv-python if both are installed."
        )
    return cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8,
    )

def train_recognizer():
    students = list(Student.objects.all())
    images = []
    labels = []
    valid_students = []

    for student in students:
        if not student.face_image:
            continue
        try:
            path = student.face_image.path
            image = cv2.imread(path)
            if image is None:
                continue
            gray, faces = detect_faces(image)
            if len(faces) == 0:
                continue

            x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))
            images.append(face)
            labels.append(len(valid_students))
            valid_students.append(student)
        except (OSError, ValueError):
            continue

    if not images:
        return None, []

    recognizer = create_recognizer()
    recognizer.train(images, np.array(labels))
    return recognizer, valid_students

def recognize_image(image, threshold=75):
    recognizer, students = train_recognizer()
    gray, faces = detect_faces(image)

    results = []
    if recognizer is None:
        return results, len(faces)

    for x, y, w, h in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        label, confidence = recognizer.predict(face)

        if 0 <= label < len(students) and confidence <= threshold:
            student = students[label]
            results.append({
                "student_id": student.id,
                "register_number": student.register_number,
                "name": student.name,
                "confidence": round(float(confidence), 2),
                "box": [int(x), int(y), int(w), int(h)],
            })
        else:
            results.append({
                "student_id": None,
                "register_number": "UNKNOWN",
                "name": "Unknown",
                "confidence": round(float(confidence), 2),
                "box": [int(x), int(y), int(w), int(h)],
            })

    return results, len(faces)

def annotate_image(image, results):
    output = image.copy()
    for item in results:
        x, y, w, h = item["box"]
        name = item["name"]
        color = (0, 200, 0) if item["student_id"] else (0, 0, 255)
        cv2.rectangle(output, (x, y), (x+w, y+h), color, 2)
        cv2.putText(
            output,
            name,
            (x, max(20, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            color,
            2,
        )
    return output
