# core/urls.py
from django.urls import path
from .views import (
    RegisterPatientView, GetPatientDetailsView, StorePatientMedicalRecordsView,
    OrganizePatientDataView, ProcessAudioRecordsView, GetPatientRecordsView
)

urlpatterns = [
    path('register_patient/', RegisterPatientView.as_view(), name='register_patient'),
    path('get_patient_details/', GetPatientDetailsView.as_view(), name='get_patient_details'),
    path('store_patient_medical_records/', StorePatientMedicalRecordsView.as_view(), name='store_patient_medical_records'),
    path('organize_patient_data/', OrganizePatientDataView.as_view(), name='organize_patient_data'),
    path('process_audio_records/', ProcessAudioRecordsView.as_view(), name='process_audio_records'),
    path('get_patient_records/', GetPatientRecordsView.as_view(), name='get_patient_records'),
]
