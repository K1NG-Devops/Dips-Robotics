from django.urls import path
from . import views
from .views import scan_qr, register_student, admin_page_view, student_list, student_profile, staff_list, staff_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('students/', views.student_list, name='students'),
    path('scan_qr/', scan_qr, name='scan_qr'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('student-register/', register_student, name='register_student'),
    path('admin_page/', admin_page_view, name='admin_page'),
    path('custom_403/', views.custom_403, name='custom_403'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('student_list/', views.student_list, name='student_list'),
    path('student_profile/<int:id>/', views.student_profile, name='student_profile'),
    path('staff_profile/<int:id>/', views.staff_profile, name='staff_profile'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('delte_teacher/<int:id>/', views.delete_staff, name='delete_teacher'),
    path('')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)