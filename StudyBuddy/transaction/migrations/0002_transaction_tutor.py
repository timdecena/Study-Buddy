# Generated by Django 5.1.1 on 2024-11-06 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
        ('tutors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutors.tutor'),
        ),
    ]
