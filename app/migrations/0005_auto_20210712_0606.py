# Generated by Django 3.2.5 on 2021-07-12 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210712_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='doctor_is_cardiologist',
        ),
        migrations.RemoveField(
            model_name='account',
            name='doctor_is_generaldoctor',
        ),
        migrations.RemoveField(
            model_name='account',
            name='doctor_is_gynecologist',
        ),
        migrations.RemoveField(
            model_name='account',
            name='doctor_is_pediatrician',
        ),
    ]
