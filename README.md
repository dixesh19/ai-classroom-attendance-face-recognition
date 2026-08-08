# AI-Based Classroom Attendance from Face Recognition

A Django web application that registers students, captures face images, recognizes students from classroom photos or webcam frames, marks attendance, lets teachers correct records, and exports CSV reports.

## Features

- Teacher login/logout
- Student registration with face image
- OpenCV Haar Cascade face detection
- OpenCV LBPH face recognition
- Classroom photo upload
- Browser webcam capture/live recognition
- Automatic Present/Absent calculation
- Manual attendance correction
- Attendance dashboard
- CSV export
- SQLite database for development
- Admin interface

## Technology

- Python
- Django
- OpenCV
- NumPy
- Pillow
- SQLite

## Important privacy note

Do not upload real student face images, biometric encodings, or personal student data to a public GitHub repository. The `media/` directory and registered face dataset are ignored by Git. Use consented data and follow your institution's privacy rules.

## Setup

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/ai-classroom-attendance-face-recognition.git
cd ai-classroom-attendance-face-recognition
```

### 2. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Migrate database

```bash
python manage.py migrate
```

### 5. Create teacher/admin

```bash
python manage.py createsuperuser
```

Enter username, email and password.

### 6. Run

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## How to use

1. Login using the superuser account.
2. Open **Register Student**.
3. Enter register number, name, department, year and section.
4. Upload a clear front-facing image.
5. Open **Take Attendance**.
6. Upload a classroom photo or use webcam capture.
7. The system detects faces and compares them with registered students.
8. Review the generated attendance list.
9. Correct any record if required.
10. Export the report as CSV.

## Recognition notes

LBPH is suitable for a classroom prototype and demonstration, but it is not a state-of-the-art face recognition system. Accuracy depends strongly on lighting, pose, camera quality, face size and registration images.

For a production system, use a properly evaluated modern face-embedding model, liveness detection, access controls, encryption, audit logging and institution-approved biometric data handling.

## Project structure

```text
ai-classroom-attendance-face-recognition/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── face_attendance/
├── attendance/
│   ├── face_engine.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   └── static/
├── dataset/
└── media/
```
