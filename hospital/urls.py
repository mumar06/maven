from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    path('',views.index,name = 'index'),
    path('blogs/',views.blogs_view,name = 'blogs'),
    path('new_blogs/',views.newBlog_view,name = 'new-blog'),
    path('admin/doctor-profile',views.doctor_profile, name = 'doctor-profile'),
    path('admin/all-departments',views.all_departments, name = 'all-departments'),
    path('admin/new-department',views.new_department, name = 'new_department'),
    path('admin/doctors',views.all_doctors, name = 'doctors'),
    path('admin/new-doctor',views.new_doctor, name = 'new_doctor'),
    path('admin/schedules',views.all_schedules, name = 'schedules'),
    path('admin/new-schedule',views.new_schedule, name = 'new_schedule'),
    path('admin/department_delete/<int:pk>',views.department_delete, name = 'department_delete'),
    path('admin/doctor_delete/<int:pk>',views.doctor_delete, name = 'doctor_delete'),
    path('admin/update_department/<int:pk>',views.update_department, name = 'update_department'),
    path('admin/update_doctor/<int:pk>',views.update_doctor, name = 'update_doctor'),
    path('admin/update_schedule/<int:pk>',views.update_schedule, name = 'update_schedule'),
    path('admin/schedule_delete/<int:pk>',views.schedule_delete, name = 'schedule_delete'),
    path('admin/unchecked',views.all_unchecked_appointments, name = 'unchecked'),
    path('admin/checkedin',views.all_checkedin_appointments, name = 'checkedin'),
    path('admin/checkin/<int:id>', views.checkin, name='checkin'),
    path('user_departments',views.user_departments, name = 'user_departments'),
    path('user_doctors',views.user_doctors, name = 'user_doctors'),
    path('department_detail/<int:id>', views.department_detail, name='department_detail'),
    path('doctor_detail/<int:id>', views.doctor_detail, name='doctor_detail'),
    path('searched', views.search_doctor, name='searched'),
    path('appointment/<int:schedule_id>', views.make_appointment, name='appointment'),
    path('admin/doctor-search', views.search_doc, name='doctor-search'),
    path('admin/emergency/doctor_emergency', views.doctor_emergency, name='emergency'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
