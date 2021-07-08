# Generated by Django 3.1.5 on 2021-07-06 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'verbose_name': 'Appointment', 'verbose_name_plural': 'Appointments'},
        ),
        migrations.AlterModelOptions(
            name='patientemergency',
            options={'verbose_name': 'Patient Emergiency', 'verbose_name_plural': 'Patient Emergencies'},
        ),
        migrations.AlterModelOptions(
            name='presciption',
            options={'verbose_name': 'Prescription', 'verbose_name_plural': 'Prescriptions'},
        ),
        migrations.AlterField(
            model_name='patient',
            name='patient_status',
            field=models.CharField(choices=[('Registered', 'Registered'), ('Treatment', 'Treatment'), ('Admitted', 'Admitted'), ('Discharged', 'Discharged'), ('Outpatient', 'Outpatient')], default='Registered', max_length=250),
        ),
    ]