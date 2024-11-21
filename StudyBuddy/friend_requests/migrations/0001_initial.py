# Generated by Django 5.1.1 on 2024-11-21 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0005_student_password_student_username'),
        ('tutors', '0002_tutor_password_tutor_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=10)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('receiver_student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_requests_student', to='students.student')),
                ('receiver_tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_requests_tutor', to='tutors.tutor')),
                ('sender_student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.student')),
                ('sender_tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutors.tutor')),
            ],
        ),
    ]
