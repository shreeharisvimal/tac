import uuid
from django.db import models

class PatientInfo(models.Model):
    patient_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    place = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PatientRecord(models.Model):
    record_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    patient = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)
    patient_vitals = models.JSONField()
    medical_history = models.JSONField()
    current_condition = models.TextField()
    prescribed_medicines = models.JSONField()
    lab_tests = models.JSONField()
    followup_date = models.DateField()
    doctor_details = models.JSONField()
    hospital_details = models.JSONField()
    insurance_details = models.JSONField()
    additional_notes = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
