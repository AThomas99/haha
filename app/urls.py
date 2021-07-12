from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    # User authentication
    path('login/user', views.login_user, name='login_user'),
    path('logout/user', views.logout_user, name='logout_user'),
    # Enable / Disable users
    path('disable/user/<int:user_id>', views.disable_user, name='disable_user'),
    path('enable/user/<int:user_id>', views.enable_user, name='enable_user'),

   # Patient routes
    path('register/patient', views.register_patient, name='register_patient'),
    #path('technician/profile/<int:id>', views.technician_profile, name='technician_profile'),
    path('patient/list', views.get_patient, name='patient'),
    
    # Reception routes
    path('register/reception', views.register_reception, name='register_reception'),
    path('reception/profile/<int:id>', views.reception_profile, name='reception_profile'),

    # Nurse routes
    path('register/nurse', views.register_nurse, name='register_nurse'),
    path('nurse/profile/<int:id>', views.nurse_profile, name='nurse_profile'),
    path('nurse/list', views.get_nurse, name='nurse'),
    
    # Doctor routes
    path('register/doctor', views.register_doctor, name='register_doctor'),
    path('doctor/profile/<int:id>', views.doctor_profile, name='doctor_profile'),
    path('doctor/list', views.get_doctor, name='doctor'),
    
    # Technician routes
    path('register/technician', views.register_technician, name='register_technician'),
    path('technician/profile/<int:id>', views.technician_profile, name='technician_profile'),
    path('technician/list', views.get_technician, name='technician'),

    # Clinic Programs
    # path('clinical_programs/list', views.get_clinical_programs, name='clinical_program'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
