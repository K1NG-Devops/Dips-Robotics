# Generated by Django 4.2 on 2024-05-07 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0015_alter_student_unique_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
        ),
    ]