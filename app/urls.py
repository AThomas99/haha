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
    # path('register/patient', views.register_patient, name='register_patient'),
    
    # Reception routes
    path('register/reception', views.register_reception, name='register_reception'),
    path('reception/profile/<int:id>', views.reception_profile, name='reception_profile'),

    # Nurse routes
    path('register/nurse', views.register_nurse, name='register_nurse'),
    path('nurse/profile/<int:id>', views.nurse_profile, name='nurse_profile'),
    path('nurse/list', views.get_nurse, name='nurse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
