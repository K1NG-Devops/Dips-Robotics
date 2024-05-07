from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
import uuid

class Student(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    id = models.IntegerField(primary_key=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'),('Other','Other')))
    grade = models.CharField(max_length=50)
    enrollment_date = models.DateField()
    profile_picture_url = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    contact = models.CharField(max_length=100, default='')
    email = models.EmailField(blank=True, null=True)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_code = models.ImageField(upload_to='student_qrcodes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(uuid.uuid4())
        if not self.qr_code:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.unique_id)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            filename = f'{self.id}.jpeg'
            filebuffer = File(buffer, name=filename)
            self.qr_code.save(filename, filebuffer, save=False)
        super().save(*args, **kwargs)

class Staff(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    id = models.IntegerField(primary_key=True)
    teaching_subject = models.CharField(max_length=100, default='')
    teaching_grade = models.CharField(max_length=50, default='')
    practioner_license = models.CharField(max_length=100, default='')
    hire_date = models.DateField()
    unique_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    qr_code = models.ImageField(upload_to='staff_qrcodes/', null=True, blank=True)
    contact = models.CharField(max_length=100, default='')
    email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(uuid.uuid4())
        if not self.qr_code:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.unique_id)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            filename = f'{self.unique_id}.jpeg'
            filebuffer = File(buffer, name=filename)
            self.qr_code.save(filename, filebuffer, save=False)
        super().save(*args, **kwargs)

class Assignments(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()

class Timetable(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateField()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False) # False means absent, True means present