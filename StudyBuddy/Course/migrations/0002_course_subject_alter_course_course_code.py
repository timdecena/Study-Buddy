# Generated by Django 5.1.1 on 2024-11-05 17:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
        ('Subject', '0002_alter_subject_subject_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Subject.subject'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=50),
        ),
    ]