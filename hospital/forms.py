from django import forms
from .models import Hospital, Doctor, Schedule, Department, Appointment
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserForm(UserCreationForm):


    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
    details = forms.CharField()
    image = forms.ImageField(required=True)
    department = forms.ChoiceField(required=True, choices =  ([('','-----------')] + list(Department.objects.values_list('id','name'))))
    class Meta():
        model = User
        fields = ['username','password1','password2','first_name','last_name','email']
        exclude = ['last_login','staff_status','groups',
                    'user_permissions', 'password','is_superuser','is_staff','is_active']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name","description", "department_image")
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control mb-4"}),
            "description":TinyMCE(attrs={'cols': 116, 'rows': 15}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        exclude = ['status']

class UpdateDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name","description")

class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['doctor_image', 'departments']


class UpdateScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ['doctor', 'status']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['doctor','schedules', 'status']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        exclude = ['name','author']