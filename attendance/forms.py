from django import forms
from .models import Student, Attendance

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "register_number",
            "name",
            "department",
            "year",
            "section",
            "face_image",
        ]
        widgets = {
            "register_number": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10}),
            "section": forms.TextInput(attrs={"class": "form-control"}),
            "face_image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
        }

    def clean_face_image(self):
        image = self.cleaned_data["face_image"]
        if image.size > 8 * 1024 * 1024:
            raise forms.ValidationError("Image must be 8 MB or smaller.")
        if image.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise forms.ValidationError("Upload a JPG, PNG or WEBP image.")
        return image

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
        }
