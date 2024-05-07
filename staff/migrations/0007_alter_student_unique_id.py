# Generated by Django 4.2 on 2024-05-05 07:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0006_staff_qr_code_alter_staff_unique_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="unique_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]