import csv
from datetime import date

import cv2
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .face_engine import annotate_image, load_image_from_uploaded_file, recognize_image
from .forms import AttendanceForm, StudentForm
from .models import Attendance, Student

@login_required
def dashboard(request):
    selected_date = request.GET.get("date") or date.today().isoformat()
    records = Attendance.objects.filter(date=selected_date).select_related("student")
    present = records.filter(status="Present").count()
    absent = records.filter(status="Absent").count()
    total = Student.objects.count()
    percentage = round((present / total) * 100, 2) if total else 0

    return render(request, "attendance/dashboard.html", {
        "records": records,
        "selected_date": selected_date,
        "present": present,
        "absent": absent,
        "total": total,
        "percentage": percentage,
    })

@login_required
def students(request):
    return render(request, "attendance/students.html", {
        "students": Student.objects.all()
    })

@login_required
def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"{student.name} registered successfully.")
            return redirect("students")
    else:
        form = StudentForm()

    return render(request, "attendance/register_student.html", {"form": form})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        name = student.name
        student.delete()
        messages.success(request, f"{name} deleted.")
    return redirect("students")

@login_required
def take_attendance(request):
    return render(request, "attendance/take_attendance.html")

@login_required
def process_attendance(request):
    if request.method != "POST":
        return redirect("take_attendance")

    image_file = request.FILES.get("classroom_image")
    if not image_file:
        messages.error(request, "Please upload or capture an image.")
        return redirect("take_attendance")

    if image_file.size > 8 * 1024 * 1024:
        messages.error(request, "Image must be 8 MB or smaller.")
        return redirect("take_attendance")

    try:
        image = load_image_from_uploaded_file(image_file)
        results, detected_count = recognize_image(image)
    except Exception as exc:
        messages.error(request, str(exc))
        return redirect("take_attendance")

    recognized_ids = {
        item["student_id"] for item in results if item["student_id"] is not None
    }

    today = date.today()
    with transaction.atomic():
        for student in Student.objects.all():
            status = "Present" if student.id in recognized_ids else "Absent"
            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={"status": status},
            )

    annotated = annotate_image(image, results)
    output_name = "processed_attendance.jpg"
    output_path = str(__import__("django.conf").conf.settings.MEDIA_ROOT / output_name)
    cv2.imwrite(output_path, annotated)

    messages.success(
        request,
        f"Attendance processed. Detected {detected_count} face(s); "
        f"recognized {len(recognized_ids)} student(s)."
    )

    return redirect("dashboard")

@login_required
def correct_attendance(request, attendance_id):
    record = get_object_or_404(Attendance, id=attendance_id)
    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated.")
            return redirect("dashboard")
    else:
        form = AttendanceForm(instance=record)

    return render(request, "attendance/correct_attendance.html", {
        "form": form,
        "record": record,
    })

@login_required
def export_csv(request):
    selected_date = request.GET.get("date") or date.today().isoformat()
    records = Attendance.objects.filter(date=selected_date).select_related("student")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="attendance_{selected_date}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        "Date",
        "Register Number",
        "Student Name",
        "Department",
        "Year",
        "Section",
        "Status",
    ])

    for record in records:
        writer.writerow([
            record.date,
            record.student.register_number,
            record.student.name,
            record.student.department,
            record.student.year,
            record.student.section,
            record.status,
        ])

    return response
