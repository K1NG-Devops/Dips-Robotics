# Generated by Django 4.2 on 2024-05-02 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Assignments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("due_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("first_name", models.CharField(default="", max_length=100)),
                ("last_name", models.CharField(default="", max_length=100)),
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("age", models.IntegerField()),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Other", "Ohter"),
                        ],
                        max_length=10,
                    ),
                ),
                ("grade", models.CharField(max_length=50)),
                ("enrollment_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("hire_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Timetable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=200)),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("status", models.BooleanField(default=False)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="staff.student"
                    ),
                ),
            ],
        ),
    ]
