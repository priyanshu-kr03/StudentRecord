# Generated by Django 5.1.1 on 2024-09-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
