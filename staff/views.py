from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .forms import StudentRegistrationForm, StaffRegistrationForm
from .models import Student, Attendance, Staff
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import json

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json

@csrf_exempt
def scan_qr(request):
    if request.method == 'POST':
        # Determine if the request is JSON
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                student_id = data.get('student_id')
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON', 'status': 'error'}, status=400)
        else:
            student_id = request.POST.get('student_id')

        if not student_id:
            return JsonResponse({'message': 'Student ID not provided', 'status': 'error'}, status=400)

        try:
            student = Student.objects.get(id=student_id)
            # Update attendance
            Attendance.objects.create(student=student, status=True)
            # Optionally update student information here if needed
            # student.some_field = new_value
            # student.save()
            return JsonResponse({'message': 'Attendance recorded', 'status': 'success'})
        except Student.DoesNotExist:
            return JsonResponse({'message': 'Student not found', 'status': 'error'}, status=404)

    return JsonResponse({'message': 'Invalid request method', 'status': 'error'}, status=405)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')

def is_admin(user):
    if user.is_authenticated and user.is_superuser:
        return True
    else:
        return False

@login_required
def admin_page_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'admin_page.html')
    else:
        return HttpResponseForbidden()
    
def register_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            if Staff.objects.filter(first_name=form.cleaned_data['first_name'], 
                                    last_name=form.cleaned_data['last_name']).exists():
                messages.error(request, 'Staff already exists!')
            else:
                form.save()
                messages.success(request, 'Staff registered successfully!')
                return redirect('staff_list')  # Redirect after POST
    else:
        form = StaffRegistrationForm()  # Initialize a blank form for GET

    return render(request, 'register_staff.html', {'form': form})

@login_required    
def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff': staff})

def edit_staff(request, staff_id):
    try:
        staff = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:
        messages.error(request, "Staff not found.")
        return redirect('staff_list')

    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff details updated successfully.")
            return redirect('staff_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StaffRegistrationForm(instance=staff)

    return render(request, 'edit_staff.html', {'form': form})

def update_staff(request, id):
    staff = Staff.objects.get(id=id)
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff details updated successfully.")
            return redirect('staff_profile', id=staff.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StaffRegistrationForm(instance=staff)
    return render(request, 'edit_staff.html', {'form': form})

def delete_staff(request, id):
    try:
        staff = Staff.objects.get(id=id)
        staff.delete()
        messages.success(request, "Staff deleted successfully.")
    except Staff.DoesNotExist:
        messages.error(request, "Staff not found.")
    return redirect('staff_list')
    
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)  # Include request.FILES to handle file data
        if form.is_valid():
            # Check if student already exists
            if Student.objects.filter(first_name=form.cleaned_data['first_name'], 
                                      last_name=form.cleaned_data['last_name']).exists():
                messages.error(request, 'Student already exists!')
            else:
                student = form.save(commit=False)  # Use commit=False to modify the student before saving
                profile_picture = request.FILES.get('profile_picture')  # Get the file from request.FILES, not request.POST
                if profile_picture:
                    fs = FileSystemStorage()
                    filename = fs.save(profile_picture.name, profile_picture)
                    student.profile_picture_url = fs.url(filename)
                student.save()  # Save the student after all modifications
                messages.success(request, 'Registration successful!')
                return redirect('student_list')  # Redirect to a list of students or a success page
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = StudentRegistrationForm()  # Initialize a blank form for GET requests

    return render(request, 'register_student.html', {'form': form})
    
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

def custom_403(request, *args, **argv):
    logger.error("Access denied")
    messages.error(request, "You do not have permission to access this page.")
    return render(request, '403.html', {}, status=403)

from django.core.files.storage import FileSystemStorage

def student_profile(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST' and request.FILES.get('newProfilePic'):
        profile_pic = request.FILES['newProfilePic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        uploaded_file_url = fs.url(filename)
        
        student.profile_picture_url = uploaded_file_url
        student.save()
        
        messages.success(request, 'Profile picture updated successfully!')
        return redirect('student_profile', id=student.id)
    
    return render(request, 'student_profile.html', {'student': student})

def update_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student details updated successfully.")
            return redirect('student_profile', id=student.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentRegistrationForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})

def delete_student(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        messages.success(request, "Student deleted successfully.")
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
    return redirect('student_list')


def staff_profile(request, id):
    staff = Staff.objects.get(id=id)
    return render(request, 'staff_profile.html', {'staff': staff})


def profile_picture(request, id):
    student = Student.objects.get(id=id)
    return render(request, 'profile_picture.html', {'student': student})

def profile_picture_upload(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        profile_pic = request.FILES.get('newProfilePic')
        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            uploaded_file_url = fs.url(filename)
            student.profile_picture_url = uploaded_file_url
            student.save()
            messages.success(request, "Profile picture updated successfully.")
            return redirect('student_profile', id=student.id)  # Ensure consistent use of 'id'
        else:
            messages.error(request, "Please upload a valid image.")
    return render(request, 'profile_picture.html', {'student': student})

def student_profile_edit(request, id):
    student = Student.objects.get(id=id)
    return render(request, 'student_profile_edit.html', {'student': student})

def staff_profile_edit(request, id):
    staff = Staff.objects.get(id=id)
    return render(request, 'staff_profile_edit.html', {'staff': staff})

