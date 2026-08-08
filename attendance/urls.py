from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(
        template_name="attendance/login.html"
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("students/", views.students, name="students"),
    path("students/register/", views.register_student, name="register_student"),
    path("students/<int:student_id>/delete/", views.delete_student, name="delete_student"),
    path("attendance/take/", views.take_attendance, name="take_attendance"),
    path("attendance/process/", views.process_attendance, name="process_attendance"),
    path("attendance/correct/<int:attendance_id>/", views.correct_attendance, name="correct_attendance"),
    path("attendance/export/", views.export_csv, name="export_csv"),
]
