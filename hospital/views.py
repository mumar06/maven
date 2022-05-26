from django.shortcuts import render, redirect
from .forms import *
from .models import Department, Doctor, Schedule, Appointment
from django.contrib.auth.decorators import login_required
from .email import send_welcome_email
from .email import send_emergency_email
from django.conf import settings
from django.views.generic.base import TemplateView
from json import dumps
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from .models import *

def index(request):
    return render(request, 'patient/index.html')

def blogs_view(request):
    blogs = Blogs.objects.all()
    context = {
        'blogs': blogs
    }
    return render(request, 'patient/blogs.html', context=context)

def newBlog_view(request):
    if request.method == 'POST':
        id = Doctor.objects.filter(email=request.user.email).values('first_name', 'last_name')
        form = BlogForm(request.POST)
        print(form.errors)
        if form.is_valid():
            instance = Blogs()
            instance.title = form.data.get('title')
            instance.description = form.data.get('description')
            instance.blog = form.data.get('blog')
            instance.author = f"Dr.{id[0].get('first_name')} {id[0].get('last_name')}"
            instance.save()
    form = BlogForm()
    return render(request, 'admin/new-blog.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            obj = Doctor()
            obj.first_name = form.data.get('first_name').capitalize()
            obj.last_name = form.data.get('last_name').capitalize()
            obj.email = form.data.get('email')
            obj.phone_number = form.data.get('phone_number')
            obj.details = form.data.get('details')
            obj.doctor_image = request.FILES['image']
            obj.departments = Department.objects.get(id=form.data.get('department'))
            obj.save()
            instance = Doctor.objects.filter(email = form.data.get('email')).first()
            email = instance.id
            User.objects.filter(id=user.id).update(first_name=user.first_name.capitalize(), last_name=user.last_name.capitalize())
            return redirect('update_doctor', pk=email)
    else:
        form = UserForm()
    return render(request, 'user/registration.html', {'form': form})


@login_required(login_url='/accounts/login/')
def all_departments(request):
    departments = Department.objects.all()
    return render(request, 'admin/all-departments.html', context={"departments": departments})

def new_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-departments')
    else:
        form = DepartmentForm()
        return render(request, 'admin/new-department.html',{'form': form})

def update_department(request,pk):
    dep = Department.objects.get(pk = pk)

    if request.method == "POST":
        form = UpdateDepartmentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Department.objects.filter(id = pk).update(name = name, description = description)

            return redirect("all-departments")
    else:
        form = UpdateDepartmentForm()
    return render(request, "admin/update-department.html", context={"form": form, "department":dep})

def department_delete(request,pk):
    department = Department.objects.get(pk=pk)
    department.delete()

    return redirect('all-departments')


# Doctor View Function
def doctor_profile(request):
    id = Doctor.objects.filter(email=request.user.email).values('id')
    return redirect('update_doctor',pk=id[0].get('id'))

def all_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/all-doctors.html', context={"doctors": doctors})

def new_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('doctors')
    else:
        form = DoctorForm()
        return render(request, "admin/new-doctor.html", context={"form":form})


def update_doctor(request,pk):
    doc = Doctor.objects.get(pk = pk)
    if request.method == "POST":
        form = UpdateDoctorForm(request.POST)
        print(form.errors)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            details = form.cleaned_data['details']
            Doctor.update_doctor(pk, first_name, last_name, email,phone_number,details)
            return redirect("doctors")
    else:
        form = UpdateDoctorForm()
    return render(request, "admin/update-doctor.html", context={"form": form, "doctor":doc})


def doctor_delete(request,pk):
    doctor = Doctor.objects.get(pk=pk)
    doctor.delete()
    return redirect('doctors')

def search_doc(request):
    if request.method=="GET":
        search_term=request.GET.get("doctor-search")
        searched_doc=Doctor.objects.get(first_name=search_term)
        schedules = Schedule.objects.filter(doctor=searched_doc.id)
        for ap in schedules:
            if ap.status == "taken":
                appointment = []
                appointment.append(Appointment.objects.get(schedules_id=ap.id))
                print(ap.id)
        return render(request, 'admin/doctor-search.html',context={"searched_doc":searched_doc,"appointment":appointment})
    else:
        return redirect('all-doctors')


def doctor_emergency(request,pk):
    appointments = Appointment.objects.get(pk=pk)
    send_emergency_email(appointments.first_name,appointments.last_name,appointments.schedules,appointments.email)
    searched_doc=Doctor.objects.get(id=appointments.schedules.doctor.id)
    schedules = Schedule.objects.filter(doctor=searched_doc.id)
    for ap in schedules:
        if ap.status == "taken":
            appointment = []
            appointment.append(Appointment.objects.get(schedules_id=ap.id))
            print(ap.id)
        message = "Email to {} {} Was Successfully Sent".format(appointments.first_name,appointments.last_name)
        return render(request, 'admin/doctor-search.html',context={"searched_doc":searched_doc,"appointment":appointment, "message": message})
    else:
        return redirect('all-doctors')


def all_schedules(request):
    id = Doctor.objects.filter(email=request.user.email).values('id')
    schedules = Schedule.objects.filter(doctor_id=id[0].get('id')).all()
    return render(request, 'admin/all-schedules.html', {"schedules": schedules})

def new_schedule(request):
    id = Doctor.objects.filter(email=request.user.email).values('id')
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('schedules')
    else:
        form = ScheduleForm(initial={'doctor':id[0].get('id')})
    return render(request, 'admin/new-schedule.html', {'form': form})

def update_schedule(request, pk):
    schedule = Schedule.objects.get(pk = pk)
    if request.method == 'POST':
        form = UpdateScheduleForm(request.POST)
        print(form.errors)
        if form.is_valid():
            app_date = form.cleaned_data['app_date']
            app_day = form.cleaned_data['app_day']
            app_hour = form.cleaned_data['app_hour']
            Schedule.objects.filter(id = pk).update(app_date = app_date, app_day = app_day, app_hour = app_hour)
            return redirect('schedules')
    else:
        form = UpdateScheduleForm()
        return render(request, 'admin/update-schedule.html', {'form': form, "schedule": schedule})


def schedule_delete(request,pk):
    schedule = Schedule.objects.get(pk=pk)
    schedule.delete()

    return redirect('schedules')


# User View Function


def user_departments(request):
    departments= Department.objects.all()
    return render(request, 'patient/all-departments.html' , context={"departments": departments})

def department_detail(request,id):
    single_department = Department.objects.get(pk= id)
    doctors = Doctor.objects.filter(departments=id)
    return render(request,'patient/department_detail.html',{"single_department":single_department,"doctors":doctors})


def user_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'patient/all-doctors.html', context={"doctors": doctors})


def doctor_detail(request,id):
    single_doctor = Doctor.objects.get(pk= id)
    schedules = Schedule.get_schedule_by_doctor(id)
    return render(request,'patient/doctor_detail.html',{"single_doctor":single_doctor, "schedules":schedules})


def search_doctor(request):
    if request.method=="GET":
        search_term=request.GET.get("searched")
        search_term = search_term.capitalize()
        searched_doct=Doctor.objects.filter(first_name=search_term).all()
        message="{}".format(search_term)
        return render(request, 'patient/doctor-search.html',context={"searched_doct":searched_doct, "message":message})
    else:
        message="You haven't searched for any doctor"
        return render(request, 'patient/doctor-search.html',context={"message":message})


def make_appointment(request,schedule_id):
    if request.method=='POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            schedule = Schedule.objects.get(pk=schedule_id)
            doctor = Doctor.objects.get(id=schedule.doctor_id)
            new_appointment = Appointment(first_name = first_name, last_name = last_name, address=address, email = email, phone_number=phone_number, schedules = schedule, doctor = doctor)
            new_appointment.save()
            Schedule.taken_schedule(schedule_id)
            send_welcome_email(first_name,last_name,schedule,email)
            return render(request, 'patient/appointment-success.html', {"appointment":new_appointment})
    else:
        form = AppointmentForm()
        return render(request, 'patient/appointment.html', {"form":form, "schedule_id":schedule_id})


def all_unchecked_appointments(request):
    id = Doctor.objects.filter(email=request.user.email).values('id')
    appointments= Appointment.all_unchecked_appointment(id=id[0].get('id'))
    print(appointments)
    return render(request, 'admin/all-appointments.html' , context={"appointments": appointments})

def all_checkedin_appointments(request):
    id = Doctor.objects.filter(email=request.user.email).values('id')
    appointments= Appointment.all_checkedin_appointment(id=id[0].get('id'))
    return render(request, 'admin/all-checkedin-appointments.html' , context={"appointments": appointments})

def checkin(request,id):
    Appointment.checkedin_appointment(id)
    return redirect('checkedin')


class HomePageView(TemplateView):
    template_name = 'patient/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.RAVE_PUBLIC_KEY
        return context
