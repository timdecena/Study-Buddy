# Generated by Django 5.1.1 on 2024-11-26 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_session_course_session_student_session_tutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='time_start',
            field=models.TimeField(),
        ),
    ]
