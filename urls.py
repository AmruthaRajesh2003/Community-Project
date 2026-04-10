from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('register/citizen/', views.register_citizen_view, name='register_citizen'),
    path('register/health-worker/', views.register_health_worker_view, name='register_health_worker'),
    path('login/', views.login_view, name='login'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('dashboard/health-worker/', views.health_worker_dashboard, name='health_worker_dashboard'),
    path('dashboard/citizen/', views.citizen_dashboard, name='citizen_dashboard'),

    # PatientRecord CRUD
    path('patient-records/create/', views.create_patient_record, name='create_patient_record'),
    path('patient-records/<int:pk>/', views.get_patient_record, name='get_patient_record'),
    path('patient-records/<int:pk>/update/', views.update_patient_record, name='update_patient_record'),
    path('patient-records/<int:pk>/delete/', views.delete_patient_record, name='delete_patient_record'),

    # Citizen data
    path('citizen/<int:pk>/', views.get_citizen_data, name='get_citizen_data'),

    # DiseaseReport CRUD
    path('disease-reports/create/', views.create_disease_report, name='create_disease_report'),
    path('disease-reports/<int:pk>/update/', views.update_disease_report, name='update_disease_report'),
    path('disease-reports/<int:pk>/delete/', views.delete_disease_report, name='delete_disease_report'),

    # HealthEvent CRUD
    path('health-events/create/', views.create_health_event, name='create_health_event'),
    path('health-events/<int:pk>/update/', views.update_health_event, name='update_health_event'),
    path('health-events/<int:pk>/delete/', views.delete_health_event, name='delete_health_event'),

    # Profile edit
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),

    # Community alerts
    path('community-alerts/create/', views.create_community_alert, name='create_community_alert'),

    # Workflow URLs
    path('disease-reports/<int:pk>/verify/', views.verify_disease_report, name='verify_disease_report'),
    path('disease-reports/<int:pk>/approve/', views.approve_disease_report, name='approve_disease_report'),
]
