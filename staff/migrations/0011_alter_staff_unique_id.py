# Generated by Django 4.2 on 2024-05-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0010_staff_contact_staff_qr_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="unique_id",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
