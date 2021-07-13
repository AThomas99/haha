from django.forms.widgets import PasswordInput
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test

from app.forms import (
    PatientForm, 
    PatientEmergencyForm, 
    PatientVitalsForm, 
    AppointmentForm, 
    LoginForm, 
    RegisterForm,
) 
from app.models import *

# Decorator function
def is_user_staff(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    # a hack to check if the user is as staff member
    # to prevent them from visiting administrator dashboard
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# Homepage for reception
def home_for_receptionist(request):
    context = {
        "patient_basic_form": PatientForm(),
        "patient_emergency_form": PatientEmergencyForm(),
        "patient": Patient.objects.all(),
        "all_patients": Patient.objects.filter(patient_status="Registered"),
        "doctors": Account.users.filter(is_doctor=True),
        "status": "Registered"
    }
    return render(request, 'patient.html', context=context)

# Homepage for nurse
def home_for_nurse(request):
    context = {
        "patient_vital_form": PatientVitalsForm(),
        "patient": Patient.objects.all(),
        "all_patients": Patient.objects.filter(patient_status="Registered"),
        "status": "Registered",
    }
    return render(request, 'nurse.html', context=context)

# Homepage for doctor
def home_for_doctor(request):
    context = {
        "patient_basic_form": PatientForm(),
        "patient_vital_form": PatientVitalsForm(),
        "patient_appointment": AppointmentForm(),
        "patient": Patient.objects.all(),
        "appointment": Appointment.objects.all(),
        "all_patients": Patient.objects.filter(patient_status="Registered"),
        "all_appointments": Appointment.objects.filter(patient_status="Registered", doctor_assigned__id=request.user.id),
        "status": "Registered"
    }
    return render(request, 'nurse.html', context=context)

# User login function
def login_user(request):
    form_data = LoginForm(request.POST)
    if form_data.is_valid():
        email = form_data.data['email']
        password = form_data.data['password']

        # get user with the provided email and check against the
        # provided password
        user = Account.users.get(email=email)
        is_auth = user.check_password(password)
        if is_auth:
            login(request, user, backend='app.backends.AccountAuth')

        return redirect('/')

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            reception = Account.users.filter(is_reception=True)
            context = {
                'reception': reception,
                'registration_form': RegisterForm(),
                'profile_page': False,
                'media_url': settings.MEDIA_URL
            }
            return render(request, 'reception.html', context)
        if request.user.is_nurse:
            return home_for_nurse(request)
        if request.user.is_doctor:
            return home_for_doctor(request)
        if request.user.is_reception:
            return home_for_receptionist(request)

    context = {
        'login_form': LoginForm()
    }

    return render(request, 'login.html', context)

@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def disable_user(request, user_id):
    user = Account.users.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
@is_user_staff(login_url='/')
def enable_user(request, user_id):
    user = Account.users.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect(request.META.get('HTTP_REFERER'))

# Register reception function
@login_required(login_url='/')
@is_user_staff(login_url='/')
def register_reception(request):
    form_data = RegisterForm(request.POST)
    if form_data.is_valid():
        user = form_data.save(commit=False)
        user.is_reception = True
        user.set_password(form_data.data['password1'])
        user.is_active = True

        # this is made explicit because somehow phone numbers
        # are saved on both email field and phone number field
        user.email = form_data.data['email']
        user.set_password(form_data.data['password2'])
        user.save()
    return redirect(to='/')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def reception_profile(request, id):
    user = Account.users.get(id=id)
    # categories = Service.objects.all()

    context = {
        'reception': user,
        'profile_page': True,
        # 'categories': categories
    }
    return render(request, 'reception.html', context)

# Nurse Functionalities
@login_required(login_url='/')
@is_user_staff(login_url='/')
def get_nurse(request):
        if request.user.is_staff:
            nurse = Account.users.filter(is_nurse=True)
            context = {
                'nurse': nurse,
                'registration_form': RegisterForm(),
                'profile_page': False,
                'media_url': settings.MEDIA_URL
            }
            return render(request, 'nurse.html', context)
        return redirect('/')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def register_nurse(request):
    form_data = RegisterForm(request.POST)
    if form_data.is_valid():
        user = form_data.save(commit=False)
        user.is_nurse = True
        user.set_password(form_data.data['password1'])

        user.is_active = True

        # this is made explicit because somehow phone numbers
        # are saved on both email field and phone number field
        user.email = form_data.data['email']
        user.set_password(form_data.data['password2'])
        user.save()
    return redirect(to='/nurse//list')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def nurse_profile(request, id):
    user = Account.users.get(id=id)
    # categories = Service.objects.all()

    context = {
        'nurse': user,
        'profile_page': True,
        # 'categories': categories
    }
    return render(request, 'nurse.html', context)


# Doctor Functionalities
@login_required(login_url='/')
@is_user_staff(login_url='/')
def get_doctor(request):
        if request.user.is_staff:
            doctor = Account.users.filter(is_doctor=True)
            context = {
                'doctor': doctor,
                'registration_form': RegisterForm(),
                'profile_page': False,
                'media_url': settings.MEDIA_URL
            }
            return render(request, 'doctor.html', context)
        return redirect('/')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def register_doctor(request):
    form_data = RegisterForm(request.POST)
    if form_data.is_valid():
        user = form_data.save(commit=False)
        user.is_doctor = True
        user.set_password(form_data.data['password1'])

        user.is_active = True

        # this is made explicit because somehow phone numbers
        # are saved on both email field and phone number field
        user.email = form_data.data['email']
        user.set_password(form_data.data['password2'])
        user.save()
    return redirect(to='/doctor/list')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def doctor_profile(request, id):
    user = Account.users.get(id=id)
    # categories = Service.objects.all()

    context = {
        'doctor': user,
        'profile_page': True,
        # 'categories': categories
    }
    return render(request, 'doctor.html', context)

# Laboratory Technician Functionalities
@login_required(login_url='/')
@is_user_staff(login_url='/')
def get_technician(request):
        if request.user.is_staff:
            technician = Account.users.filter(is_technician=True)
            context = {
                'technician': technician,
                'registration_form': RegisterForm(),
                'profile_page': False,
                'media_url': settings.MEDIA_URL
            }
            return render(request, 'technician.html', context)
        return redirect('/')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def register_technician(request):
    form_data = RegisterForm(request.POST)
    if form_data.is_valid():
        user = form_data.save(commit=False)
        user.is_technician = True
        user.set_password(form_data.data['password1'])

        user.is_active = True

        # this is made explicit because somehow phone numbers
        # are saved on both email field and phone number field
        user.email = form_data.data['email']
        user.set_password(form_data.data['password2'])
        user.save()
    return redirect(to='/technician/list')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def technician_profile(request, id):
    user = Account.users.get(id=id)
    # categories = Service.objects.all()

    context = {
        'technician': user,
        'profile_page': True,
        # 'categories': categories
    }
    return render(request, 'technician.html', context)

@login_required(login_url='/')
# @is_user_staff(login_url='/')
def register_patient(request):
    form_data = PatientForm(request.POST)

    if form_data.is_valid():
        user = form_data.save(commit=False)
        doctor = Account.users.get(id=form_data.data['doctor'])
        user.doctor = doctor
        user.save()

    else:
        print('Form is invalid')


    return redirect(to='/patient/list')

@login_required(login_url='/')
@is_user_staff(login_url='/')
def get_patient(request):
        if request.user.is_reception:
            patient = Patient.users.filter(id=id)
            doctor = Account.objects.all().filter(is_doctor=True)
            context = {
                'patient': patient,
                'doctor': doctor,
                'registration_form': PatientForm(),
                'profile_page': False,
                # 'media_url': settings.MEDIA_URL
            }
            return render(request, 'patient.html', context)
        return redirect('/')