# Generated by Django 4.2 on 2024-05-07 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0013_staff_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="contact",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="student",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="student",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="student_profile_pictures/"
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="profile_picture_url",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
