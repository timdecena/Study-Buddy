# Generated by Django 5.1.1 on 2024-11-06 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_name', models.CharField(max_length=100)),
                ('schedule_date', models.DateField()),
                ('time_start', models.IntegerField()),
            ],
        ),
    ]