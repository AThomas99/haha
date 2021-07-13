from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from time import strftime, gmtime
from django.db.models.base import Model
from django.utils import timezone
from ckeditor.fields import RichTextField


class AccountManager(BaseUserManager):
    def _create_user(self, email=None, password=None, is_superuser=False, is_staff=False, is_active=False):
        if email is None:
            raise ValueError("users must have an email")
        if password is None:
            raise ValueError("users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **kwargs):
        user = self._create_user( email, password, is_staff=False, is_superuser=False, is_active=False)
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        # user.user_role = 'normal user'
        user.date_joined = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # user.last_login = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.save(using=self._db)
        return user

    def create_staffuser(self, email=None, password=None, **kwargs):
        user = self._create_user(
            email, password, is_staff=True, is_superuser=False, is_active=False)
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        # user.user_role = 'staff user'
        user.date_joined = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # user.last_login = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self._create_user(
            email, password, is_superuser=True, is_staff=True, is_active=True)
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        # user.user_role = 'admin user'
        user.date_joined = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # user.last_login = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    date_joined     = models.DateTimeField(default=timezone.now)
    phone_number    = models.CharField(unique=True, max_length=15)
    profile_picture = models.ImageField(upload_to='users/%Y/%m/%d',default='default/user.png',blank=True)

    # User roles
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    has_patient_basic_info_access = models.BooleanField(default=False)
    has_patient_vital_access = models.BooleanField(default=False)
    
    is_reception    = models.BooleanField(default=False)
    is_nurse        = models.BooleanField(default=False)
    is_doctor       = models.BooleanField(default=False)
    is_technician   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    users = AccountManager()
    objects = AccountManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    users = models.Manager()

# Reception Model
# class Reception(models.Model):

#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     joined_at = models.DateField(auto_now=True)

#     reception = models.Manager()
#     objects = AccountManager()

#     class Meta:
#         verbose_name = "Reception"
#         verbose_name_plural = "Reception"

#     def __str__(self):
#         return self.name

# # Nurse Model
# class Nurse(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     joined_at = models.DateField(auto_now=True)

#     nurse = models.Manager()
#     objects = AccountManager()

#     class Meta:
#         verbose_name = "Nurse"
#         verbose_name_plural = "Nurse"

#     def __str__(self):
#         return self.name

# # Laboratory Technician model
# class LabTechnician(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     joined_at = models.DateField(auto_now=True)

#     lab_technician = models.Manager()

#     class Meta:
#         verbose_name = "Lab Technician"
#         verbose_name_plural = "Lab Technicians"

#     def __str__(self):
#         return self.name

# # Doctor model
# class Doctor(models.Model):
#     SPECIALITIES = (
#         ('Pediatrician' , 'Pediatrician'),
#         ('Gynecologist' , 'Gynecologist'),
#         ('Cardiologist' , 'Cardiologist'),
#         ('Surgeon' , 'Surgeon'), 
#         ('Ophthalmologist' , 'Ophthalmologist'), # Eye
#         ('Dermatologist' , 'Dermatologist'), # A dermatologist is a medical doctor who specializes in treating skin, hair, and nails.
#     )

#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=250, blank=True, null=True)
#     last_name = models.CharField(max_length=250, blank=True, null=True)
#     telno = models.CharField(max_length=13, blank=True, null=True)
#     speciality = models.CharField( max_length=200, choices=SPECIALITIES, blank=True, null=True)
#     description = RichTextField()
#     joined_at = models.DateField(auto_now=True)

#     class Meta:
#         verbose_name = "Doctor"
#         verbose_name_plural = "Doctors"
    
#     doctor = models.Manager()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# Patient model
class Patient(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    PATIENT_STATUS = (
        ('Registered' , 'Registered'),
        ('Admitted' , 'Admitted'),
        ('Discharged' , 'Discharged'),
        ('Outpatient' , 'Outpatient'),
    )

    # Staff Members
    doctor = models.ForeignKey(Account, related_name='doctor_patient',  null=True, blank=True, on_delete=models.SET_NULL)
    lab_technician = models.ForeignKey(Account, related_name= 'patient_lab',null=True, blank=True, on_delete=models.SET_NULL)
    # doctor = models.ForeignKey(Reception,  null=True, blank=True, on_delete=models.SET_NULL)

    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number   = models.CharField(unique=True, max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER, blank=False, null=False)
    birth_date = models.DateField(auto_now=True)
    age = models.IntegerField(null=False, blank=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    registered = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    patient_status = models.CharField(max_length=250, default="Registered" ,choices=PATIENT_STATUS, blank=False, null=False)


    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    patient = models.Manager()
    objects = AccountManager()


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Patient Emergency model
class PatientEmergency(models.Model):
    
    patient = models.OneToOneField(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    patient_relation = models.CharField(max_length=250, null=True, blank=True)
    patient_family_name = models.CharField(max_length=250, null=True, blank=True)
    patient_family_number = models.CharField(unique=True, max_length=15)

    class Meta:
        verbose_name = "Patient Emergiency"
        verbose_name_plural = "Patient Emergencies"

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name}"

# Patient vitals model
class PatientVitals(models.Model):

    PATIENT_STATUS = (
        ('Registered' , 'Registered'),
        ('Treatment' , 'Treatment'),
        ('Admitted' , 'Admitted'),
        ('Discharged' , 'Discharged'),
        ('Outpatient' , 'Outpatient'),
    )
    
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    body_temperature = models.CharField(max_length=10, null=False, blank=False)
    body_pressure = models.CharField(max_length=10, null=False, blank=False)
    pulse_rate = models.CharField(max_length=10, null=False, blank=False)
    respiration_rate = models.CharField(max_length=10, null=False, blank=False)
    body_height = models.CharField(max_length=10, null=False, blank=False)
    body_weight = models.CharField(max_length=10, null=False, blank=False)

    class Meta:
        verbose_name = "Vital"
        verbose_name_plural = "Vitals"


    def __str__(self):
        return f"{self.patient.first_name}"

# Appointment model
class Appointment(models.Model):
    APPOINTMENT_TIME = (
        ('09:00 AM', '09:00 AM'),
        ('09:40 AM', '09:40 AM'),
        ('10:00 AM', '10:00 AM'),
        ('10:40 AM', '10:40 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:40 AM', '11:40 AM'),
        ('12:00 AM', '12:00 AM'),
        ('12:40 AM', '12:40 AM'),
        ('13:00 AM', '13:00 AM'),
        ('13:40 AM', '13:40 AM'),
        ('14:00 AM', '14:00 AM'),
    )
    APPOINTMENT_STATUS = (
        ('unassigned', 'unassigned'),
        ('assigned', 'assigned'),
    )
    patient_requested = models.OneToOneField(Patient, related_name='patient_appointment', null=True, blank=True, on_delete=models.SET_NULL)
    doctor_assigned = models.ForeignKey(Account, related_name='doctor_assigned', null=True, blank=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(unique=True, max_length=15, null=False, blank=False)
    appointment_time = models.CharField(choices=APPOINTMENT_TIME, max_length=8)
    created_on = models.DateTimeField(default=timezone.now, blank=True)
    appointment_status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS, default='unassigned')
    note = RichTextField()

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.patient_requested.first_name} {self.patient_requested.last_name}"

# Prescription model
class Presciption(models.Model):
    doctor = models.ForeignKey(Account, related_name='doctor_prescription', null=True, blank=True, on_delete=models.SET_NULL)
    patient = models.OneToOneField(Patient,related_name='patient_prescription', on_delete=models.CASCADE)
    patient_description = RichTextField()
    patient_instruction = models.CharField(max_length=250) # Gives the patient instructions on how to take the medication
    presciption_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name}"

class ClinicProgram(models.Model):
    program_name = models.CharField(max_length=50, blank=False, null=False)
    program_description = RichTextField()
    program_date_creation = models.DateTimeField(auto_now=True)
    program_duration = models.TimeField(auto_now=False, auto_now_add=False)
    doctor_available = models.ForeignKey(Account, related_name='doctor_clinic_program', null=True, blank=True, on_delete=models.SET_NULL)

    # Create form and link on clinical services