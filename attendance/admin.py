from django.contrib import admin
from .models import Student, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("register_number", "name", "department", "year", "section")
    search_fields = ("register_number", "name", "department")
    list_filter = ("department", "year", "section")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "status", "marked_at")
    list_filter = ("date", "status")
    search_fields = ("student__register_number", "student__name")
    date_hierarchy = "date"
