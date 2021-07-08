from django.contrib import admin
from django.contrib import admin
from app.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.forms import (UserAdminCreationForm, UserAdminChangeForm)

@admin.register(Account)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    exclude = ['last_login', 'groups',]
    list_display = [
        'first_name', 'last_name', 'phone_number','is_staff', 'is_superuser', 'is_active', 'is_reception',
        'is_nurse', 'is_doctor', 'is_technician'
    ]
    list_filter = ('last_login', )

    fieldsets = (
        ('Login Credentials', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Information', {
            'fields': ('first_name', 'last_name', 'phone_number',)
        }),
        ('User roles', { 'fields': (
            'is_reception', 
            'is_nurse',
            'is_doctor',
            'is_technician',
            )})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')}),
    )

    search_fields = ('email',)
    ordering = ('last_login',)

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_filter = ('user',)

@admin.register(Reception)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    list_filter = ('joined_at',)

@admin.register(Nurse)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', )
    list_filter = ('joined_at',)

@admin.register(Doctor)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'speciality',)
    list_filter = ('joined_at',)

@admin.register(LabTechnician)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    list_filter = ('joined_at',)

@admin.register(Patient)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'phone_number', 'patient_status',)
    list_filter = ('registered',)

@admin.register(PatientEmergency)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'patient_relation',
        'patient_family_name',
        'patient_family_number',
        )

@admin.register(PatientVitals)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'body_temperature',
        'body_height',
        'body_weight', 
        )

@admin.register(Appointment)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'appointment_time', 'patient_requested',)
    list_filter = ('created_on', 'appointment_time',)

@admin.register(Presciption)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('patient_instruction', 'presciption_date',)
    list_filter = ('presciption_date',)

