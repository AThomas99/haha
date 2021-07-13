from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import fields
from .models import *

Registered = 'Registered'
Admitted = 'Admitted'
Discharged = 'Discharged'
Outpatient = 'Outpatient'


PATIENT_STATUS = [
    (Registered, "Registered"),
    (Admitted, "Admitted"),
    (Discharged, "Discharged"),
    (Outpatient, 'Outpatient')
]

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)
    # userRole = forms.ChoiceField(required=True, choices=STATUS)

    class Meta:
        model = Account
        fields = (
            'first_name', 'last_name','email', 'phone_number'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Account.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class UserAdminCreationForm(forms.ModelForm):
    """
        A form for creating new users. Includes all the required
        fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'phone_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')


class PasswordReset(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ('email',)


class Newpassword(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ()

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


# Patient forms
# class PatientForm(forms.ModelForm):
#     CHOICES = [('M','Male'),('F','Female')]
#     gender  = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=CHOICES))
#     patient_status = forms.ChoiceField(choices=PATIENT_STATUS)
#     class Meta:
#         model = Patient
#         fields = (
#             'first_name',
#             'last_name',
#             'gender',
#             'age',
#             'phone_number',
#             'doctor',
#             'patient_status',
#             )

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient 
        fields = (
            'first_name',
            'last_name',
            'gender',
            'age',
            'phone_number',
        )

class PatientEmergencyForm(forms.ModelForm):
    class Meta:
        model = PatientEmergency
        fields = (
            'patient_relation',
            'patient_family_name',
            'patient_family_number',
            )

class PatientVitalsForm(forms.ModelForm):

    class Meta:
        model = PatientVitals
        fields = (
            'body_temperature',
            'body_pressure',
            'pulse_rate',
            'respiration_rate',
            'body_height',
            'body_weight',
        )

# Appointment forms
class AppointmentForm(forms.ModelForm):
    APPOINTMENT_STATUS = (
        ('unassigned', 'unassigned'),
        ('assigned', 'assigned'),
    )

    APPOINTMENT_TIME = [
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
        ]
    appointment_time = forms.CharField(label='Appointment Time', widget=forms.RadioSelect(choices=APPOINTMENT_TIME))
    appointment_status = forms.ChoiceField(required=True, choices=APPOINTMENT_STATUS)
    class Meta:
        model = Appointment
        fields = (
            'phone_number',
            'doctor_assigned',
            'appointment_time',
            'created_on',
        )

# Prescription form
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Presciption
        fields = (
            'patient_description',
            'patient_instruction',
            
        )