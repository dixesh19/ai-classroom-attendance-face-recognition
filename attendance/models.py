from django.db import models

class Student(models.Model):
    register_number = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=120)
    department = models.CharField(max_length=120, blank=True)
    year = models.PositiveSmallIntegerField(default=1)
    section = models.CharField(max_length=20, blank=True)
    face_image = models.ImageField(upload_to="student_faces/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.register_number} - {self.name}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Absent")
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance_per_day",
            )
        ]
        ordering = ["student__register_number"]

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
