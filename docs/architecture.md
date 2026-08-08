# System Architecture

```text
Teacher
   |
   v
Django Web Dashboard
   |
   +---- Student Registration
   |
   +---- Classroom Photo / Webcam
                |
                v
        OpenCV Face Detection
                |
                v
          LBPH Recognition
                |
                v
        Present / Absent Logic
                |
                v
          SQLite Database
                |
                +---- Dashboard
                |
                +---- Manual Correction
                |
                +---- CSV Export
```

## Processing pipeline

1. Capture classroom image.
2. Convert image to grayscale.
3. Detect faces with Haar Cascade.
4. Compare each face with registered LBPH face samples.
5. Recognized students become Present.
6. All other registered students become Absent.
7. Teacher can manually correct results.
8. Export the selected day's attendance as CSV.
