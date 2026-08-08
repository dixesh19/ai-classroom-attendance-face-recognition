from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("register_number", models.CharField(max_length=30, unique=True)),
                ("name", models.CharField(max_length=120)),
                ("department", models.CharField(blank=True, max_length=120)),
                ("year", models.PositiveSmallIntegerField(default=1)),
                ("section", models.CharField(blank=True, max_length=20)),
                ("face_image", models.ImageField(upload_to="student_faces/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("status", models.CharField(choices=[("Present", "Present"), ("Absent", "Absent")], default="Absent", max_length=10)),
                ("marked_at", models.DateTimeField(auto_now=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_records", to="attendance.student")),
            ],
            options={
                "ordering": ["student__register_number"],
            },
        ),
        migrations.AddConstraint(
            model_name="attendance",
            constraint=models.UniqueConstraint(fields=("student", "date"), name="unique_student_attendance_per_day"),
        ),
    ]
}
